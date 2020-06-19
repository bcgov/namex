import json
import urllib

from flask import current_app, _app_ctx_stack
from datetime import datetime
import cx_Oracle

from namex.models import State, Request, User, Event
from namex.services.nro import NROServicesError
from namex.services import EventRecorder
from namex.services.nro.add_nr import new_nr
from namex.services.nro.change_nr import update_nr, _get_event_id, _create_nro_transaction
from namex.services.nro.consume_nr import consume_nr

from .exceptions import NROServicesError
from .utils import nro_examiner_name
from .request_utils import add_nr_header, add_comments, add_nwpta, add_names, add_applicant, \
    get_nr_header, get_nr_submitter, get_nr_requester, get_exam_comments, get_nwpta, get_names


class NROServices(object):
    """Provides services to change the legacy NRO Database
       For ease of use, following the style of a Flask Extension
    """

    def __init__(self, app=None):
        """initializer, supports setting the app context on instantiation"""
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """setup for the extension
        :param app: Flask app
        :return: naked
        """
        self.app = app
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        # the oracle session pool will clean up after itself
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'nro_oracle_pool'):
            ctx.nro_oracle_pool.close()

    def _create_pool(self):
        """create the cx_oracle connection pool from the Flask Config Environment

        :return: an instance of the OCI Session Pool
        """
        # this uses the builtin session / connection pooling provided by
        # the Oracle OCI driver
        # setting threaded =True wraps the underlying calls in a Mutex
        # so we don't have to that here


        def InitSession(conn, requestedTag):
            cursor = conn.cursor()
            cursor.execute("alter session set TIME_ZONE = 'America/Vancouver'")

        return cx_Oracle.SessionPool(user=current_app.config.get('NRO_USER'),
                                     password=current_app.config.get('NRO_PASSWORD'),
                                     dsn='{0}:{1}/{2}'.format(current_app.config.get('NRO_HOST'),
                                                              current_app.config.get('NRO_PORT'),
                                                              current_app.config.get('NRO_DB_NAME')),
                                     min=1,
                                     max=10,
                                     increment=1,
                                     connectiontype=cx_Oracle.Connection,
                                     threaded=True,
                                     getmode=cx_Oracle.SPOOL_ATTRVAL_NOWAIT,
                                     waitTimeout=1500,
                                     timeout=3600,
                                     sessionCallback=InitSession)

    @property
    def connection(self):
        """connection property of the NROService
        If this is running in a Flask context,
        then either get the existing connection pool or create a new one
        and then return an acquired session
        :return: cx_Oracle.connection type
        """
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'nro_oracle_pool'):
                ctx._nro_oracle_pool = self._create_pool()
            return ctx._nro_oracle_pool.acquire()

    def get_last_update_timestamp(self, nro_request_id):
        """Gets a datetime object that holds the last time and part of the NRO Request was modified

        :param nro_request_id: NRO request.request_id for the request we want to enquire about \
                               it DOES NOT use the nr_num, as that requires yet another %^&$# join and runs a \
                               couple of orders of magnitude slower. (really nice db design - NOT)
        :return: (datetime) the last time that any part of the request was altered
        :raise: (NROServicesError) with the error information set
        """

        try:
            cursor = self.connection.cursor()

            cursor.execute("""
                SELECT SYS_EXTRACT_UTC (cast(last_update as timestamp)) as last_update
                FROM req_instance_max_event
                WHERE request_id = :req_id"""
                ,req_id=nro_request_id)

            row = cursor.fetchone()

            if row:
                return row[0]

            return None

        except Exception as err:
            current_app.logger.error(err.with_traceback(None))
            raise NROServicesError({"code": "unable_to_get_timestamp",
                                    "description": "Unable to get the last timestamp for the NR in NRO"}, 500)

    def get_current_request_state(self, nro_nr_num):
        """Gets a datetime object that holds the last time and part of the NRO Request was modified

        :param nro_request_id: NRO request.request_id for the request we want to enquire about \
                               it DOES NOT use the nr_num, as that requires yet another %^&$# join and runs a \
                               couple of orders of magnitude slower. (really nice db design - NOT)
        :return: (datetime) the last time that any part of the request was altered
        :raise: (NROServicesError) with the error information set
        """

        try:
            cursor = self.connection.cursor()

            cursor.execute("""
                          select rs.STATE_TYPE_CD
                            from request_state rs
                            join request r on rs.request_id=r.request_id
                           where r.nr_num=:req_num
                             and rs.end_event_id is NULL"""
                    ,req_num=nro_nr_num)

            row = cursor.fetchone()

            if row:
                return row[0]

            return None

        except Exception as err:
            current_app.logger.error(err.with_traceback(None))
            raise NROServicesError({"code": "unable_to_get_request_state",
                                    "description": "Unable to get the current state of the NRO Request"}, 500)

    def set_request_status_to_h(self, nr_num, examiner_username ):
        """Sets the status of the Request in NRO to "H"

        :param nr_num: (str) the name request number, of the format "NR 9999999"
        :param examiner_username: (str) any valid string will work, but it should be the username from Keycloak
        :return: naked
        :raise: (NROServicesError) with the error information set
        """

        try:
            con = self.connection
            con.begin() # explicit transaction in case we need to do other things than just call the stored proc
            try:
                cursor = con.cursor()

                # set the fqpn if the schema is required, which is set y the deployer/configurator
                # if the environment variable is missing from the Flask Config, then skip setting it.
                if current_app.config.get('NRO_SCHEMA'):
                    func_name = '{}.nro_datapump_pkg.name_examination_func'.format(current_app.config.get('NRO_SCHEMA'))
                else:
                    func_name = 'nro_datapump_pkg.name_examination_func'

                func_vars = [nr_num,           # p_nr_number
                            'H',               # p_status
                            '',               # p_expiry_date - mandatory, but ignored by the proc
                            '',               # p_consent_flag- mandatory, but ignored by the proc
                            nro_examiner_name(examiner_username), # p_examiner_id
                            ]

                # Call the name_examination function to save complete decision data for a single NR
                # and get a return if all data was saved
                ret = cursor.callfunc(func_name, str, func_vars)
                if ret is not None:
                    current_app.logger.error('name_examination_func failed, return message: {}'.format(ret))
                    raise NROServicesError({"code": "unable_to_set_state", "description": ret}, 500)

                con.commit()

            except cx_Oracle.DatabaseError as exc:
                error, = exc.args
                current_app.logger.error("NR#:", nr_num, "Oracle-Error-Code:", error.code)
                if con:
                    con.rollback()
                raise NROServicesError({"code": "unable_to_set_state",
                        "description": "Unable to set the state of the NR in NRO"}, 500)
            except Exception as err:
                current_app.logger.error("NR#:", nr_num, err.with_traceback(None))
                if con:
                    con.rollback()
                raise NROServicesError({"code": "unable_to_set_state",
                                        "description": "Unable to set the state of the NR in NRO"}, 500)

        except Exception as err:
            # something went wrong, roll it all back
            current_app.logger.error("NR#:", nr_num, err.with_traceback(None))
            raise NROServicesError({"code": "unable_to_set_state",
                                    "description": "Unable to set the state of the NR in NRO"}, 500)

        return None

    def move_control_of_request_from_nro(self, nr, user, closed_nr=False):
        """ HIGHLY DESTRUCTIVE CALL

        This will move the loci of control of a request from NRO to NameX
        In doing so it'll update the NameX record if it is out of sync with the NRO info
        with the CURRENT NRO information OVER-WRITING the NameX info
        It will set the NameX lastUpdate to NOW

        SAFETY checks:
        This WON'T do anything if the NRO record is not in Draft
        This WON'T do anything if the NameX record is not in Draft
        This WON'T do anything if the NameX lastUpdate is newer than the NameX.nroLastUpdate field

        :param nr:
        :param user:
        :param closed_nr: boolean
        :return:
        """
        warnings = []

        if not (nr and user):
            warnings.append({'type': 'warn',
                             'code': 'unable_to_move_control_from_nro',
                             'message': 'NameRequest and User must be provided to attempt to move control from NRO.'
                             })
            return warnings

        # save the current state, as we'll need to set it back to this before returning
        nr_saved_state = nr.stateCd
        # get the last modification timestamp before we alter the record
        try:
            nro_last_ts = self.get_last_update_timestamp(nr.requestId)
        except (NROServicesError, Exception) as err:
            nro_last_ts = None
            warnings.append({'type': 'warn',
                             'code': 'unable_to_get_last_nro_ts',
                             'message': 'Unable to get last time the NR was updated in NRO'
            })
        if not closed_nr:
            current_app.logger.debug('set state to h')
            try:
                self.set_request_status_to_h(nr.nrNum, user.username)
            except (NROServicesError, Exception) as err:
                warnings.append({'type': 'warn',
                                 'code': 'unable_to_set_NR_status_in_NRO_to_H',
                                 'message': 'Unable to set the NR in NRO to HOLD. '
                                            'Please contact support to alert them of this issue'
                                            ' and provide the Request #.'
                                 })

            current_app.logger.debug('get state')
            try:
                nro_req_state = self.get_current_request_state(nr.nrNum)
            except (NROServicesError, Exception) as err:
                nro_req_state = None

            if nro_req_state is not 'H':
                warnings.append({'type': 'warn',
                                 'code': 'unable_to_verify_NR_state_of_H',
                                 'message': 'Unable to get the current state of the NRO Request'
                                 })
                current_app.logger.debug('nro state not set to H, nro-package call must have silently failed - ugh')

        current_app.logger.debug('update records')
        current_app.logger.debug('nro_last_ts: {}'.format(nro_last_ts))
        current_app.logger.debug('nr.nroLastUpdate: {}'.format(nr.nroLastUpdate))
        if 'nro_last_ts' in locals() and nro_last_ts != nr.nroLastUpdate:
            current_app.logger.debug('nro updated since namex was last updated')
            try:
                # mark the NR as being updated
                nr.stateCd = State.NRO_UPDATING
                nr.save_to_db()

                nrf = self.fetch_nro_request_and_copy_to_namex_request(user, nr_number=nr.nrNum, name_request=nr)
                if nrf:
                    nr = nrf
                nr.stateCd = nr_saved_state
                nr.save_to_db()
                EventRecorder.record(user, Event.UPDATE_FROM_NRO, nr, {})

            except Exception as missed_error:
                warnings.append({'type': 'warn',
                                 'code': 'unable_to_update_request_from_NRO',
                                 'message': 'Unable to update the Request from the NRO system,'
                                            ' please manually verify record is up to date before'
                                            ' approving/rejecting.'
                                 })
                current_app.logger.error(missed_error.with_traceback(None))
            finally:
                # set the NR back to its initial state
                nr.stateCd = nr_saved_state
                nr.save_to_db()

        return warnings if len(warnings)>0 else None

    def change_nr(self, nr, change_flags):

        warnings = []

        # save the current state, as we'll need to set it back to this before returning
        nr_saved_state = nr.stateCd

        try:

            con = self.connection
            con.begin()  # explicit transaction in case we need to do other things than just call the stored proc

            cursor = con.cursor()
            update_nr(nr, cursor, change_flags)

            con.commit()

            return None

        except Exception as err:
            warnings.append({'type': 'warn',
                             'code': 'unable_to_update_request_changes_in_NRO',
                             'message': 'Unable to update the Request details in NRO,'
                                        ' please manually verify record is up to date in NRO before'
                                        ' continuing.'
                             })
            current_app.logger.error(err.with_traceback(None))

        finally:
            # set the NR back to its initial state
            # nr.stateCd = State.INPROGRESS
            nr.stateCd = nr_saved_state
            nr.save_to_db()

        return warnings if len(warnings)>0 else None

    def consume_nr(self, nr, username, corp_num):

        warnings = []

        # save the current state, as we'll need to set it back to this before returning
        nr_saved_state = nr.stateCd

        try:

            con = self.connection
            con.begin()  # explicit transaction in case we need to do other things than just call the stored proc

            cursor = con.cursor()
            consume_nr(nr, username, corp_num, cursor)

            con.commit()

            return None

        except Exception as err:
            warnings.append({'type': 'warn',
                             'code': 'unable_to_consume_request_in_NRO',
                             'message': 'Unable to consume the Request in NRO,'
                                        ' please manually verify record is up to date in NRO before'
                                        ' continuing.'
                             })
            current_app.logger.error(err.with_traceback(None))

        return warnings if len(warnings)>0 else None

    def add_nr(self, nr):
        warnings = []
        try:

            con = self.connection
            con.begin()  # explicit transaction in case we need to do other things than just call the stored proc

            cursor = con.cursor()
            new_nr(nr, cursor)

            con.commit()

            return None

        except Exception as err:
            warnings.append({'type': 'warn',
                             'code': 'unable_to_create_request in_NRO',
                             'message': 'Unable to create the Request records in NRO,'
                                        ' please manually verify record is up to date in NRO before'
                                        ' continuing.'
                             })
            current_app.logger.error(err.with_traceback(None))

        return warnings if len(warnings) > 0 else None

    def cancel_nr(self, nr, examiner_username):
        """Sets the status of the Request in NRO to "C" (Cancelled)

        :param nr: (obj) NR Object
        :param examiner_username: (str) any valid string will work, but it should be the username from Keycloak
        :return: naked
        :raise: (NROServicesError) with the error information set
        """

        try:
            con = self.connection
            con.begin() # explicit transaction in case we need to do other things than just call the stored proc
            try:
                cursor = con.cursor()

                event_id = _get_event_id(cursor)
                current_app.logger.debug('got to cancel_nr() for NR:{}'.format(nr.nrNum))
                current_app.logger.debug('event ID for NR:{}'.format(event_id))
                _create_nro_transaction(cursor, nr, event_id, 'CANCL')

                # get request_state record, with all fields
                cursor.execute("""
                SELECT *
                FROM request_state
                WHERE request_id = :request_id
                AND end_event_id IS NULL
                FOR UPDATE
                """,
                                      request_id=nr.requestId)
                row = cursor.fetchone()
                req_state_id = int(row[0])

                # set the end event for the existing record
                cursor.execute("""
                UPDATE request_state
                SET end_event_id = :event_id
                WHERE request_state_id = :req_state_id
                """,
                                      event_id=event_id,
                                      req_state_id=req_state_id)

                # create new request_state record
                cursor.execute("""
                INSERT INTO request_state (request_state_id, request_id, state_type_cd, 
                    start_event_id, end_event_id, examiner_idir, examiner_comment, state_comment, 
                    batch_id)
                VALUES (request_state_seq.nextval, :request_id, :state, :event_id, NULL, 
                          :examiner_id, NULL, NULL, NULL)
                """,
                                      request_id=nr.requestId,
                                      state='C',
                                      event_id=event_id,
                                      examiner_id=nro_examiner_name(examiner_username)
                                      )

                con.commit()

            except cx_Oracle.DatabaseError as exc:
                err, = exc.args
                current_app.logger.error(err)
                if con:
                    con.rollback()
                raise NROServicesError({"code": "unable_to_set_state",
                        "description": "Unable to set the state of the NR in NRO"}, 500)
            except Exception as err:
                current_app.logger.error(err.with_traceback(None))
                if con:
                    con.rollback()
                raise NROServicesError({"code": "unable_to_set_state",
                        "description": "Unable to set the state of the NR in NRO"}, 500)

        except Exception as err:
            # something went wrong, roll it all back
            current_app.logger.error(err.with_traceback(None))
            if con:
                con.rollback()
            raise NROServicesError({"code": "unable_to_set_state",
                        "description": "Unable to set the state of the NR in NRO"}, 500)

        return None

    def fetch_nro_request_and_copy_to_namex_request(self, user: User, nr_number: str, name_request: Request = None) \
            -> Request:
        """Utility function to gather up and copy a Request from NRO to a NameX Request Object
           The request is NOT persisted in this helper method
        """
        try:
            cursor = self.connection.cursor()

            if name_request:
                nr = name_request
                nr_num = nr.nrNum
            else:
                nr_num = nr_number
                nr = Request.find_by_nr(nr_num)
                if not nr:
                    nr = Request()

            nr_header = get_nr_header(cursor, nr_num)

            if not nr_header:
                current_app.logger.info('Attempting to fetch Request:{} from NRO, but does not exist'.format(nr_num))
                return None
            current_app.logger.debug('fetched nr_header: {}'.format(nr_header))

            # get all the request segments from NRO
            nr_submitter = get_nr_submitter(cursor, nr_header['request_id'])
            nr_applicant = get_nr_requester(cursor, nr_header['request_id'])
            nr_ex_comments = get_exam_comments(cursor, nr_header['request_id'])
            nr_nwpta = get_nwpta(cursor, nr_header['request_id'])
            nr_names = get_names(cursor, nr_header['request_id'])

            current_app.logger.debug('completed all gets')

        except Exception as err:
            current_app.logger.debug('unable to load nr_header: {}'.format(nr_num), err.with_traceback(None))
            return None

        add_nr_header(nr, nr_header, nr_submitter, user)
        current_app.logger.debug('completed header for {}'.format(nr.nrNum))
        if nr_applicant:
            add_applicant(nr, nr_applicant)
            current_app.logger.debug('completed applicants for {}'.format(nr.nrNum))
        if nr_ex_comments:
            add_comments(nr, nr_ex_comments)
            current_app.logger.debug('completed comments for {}'.format(nr.nrNum))
        if nr_nwpta:
            add_nwpta(nr, nr_nwpta)
            current_app.logger.debug('completed nwpta for {}'.format(nr.nrNum))
        if nr_names:
            current_app.logger.debug('nr_names data into add_names():')
            current_app.logger.debug(nr_names)
            add_names(nr, nr_names)
            current_app.logger.debug('completed names for {}'.format(nr.nrNum))

        return nr

