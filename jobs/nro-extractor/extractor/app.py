"""The extractor functionality is managed in this module.

The extractor ships changes from the NamesDB to the NameX services.
"""
import time

from flask import Flask, g, current_app

from config import Config  # pylint: disable=C0411

from namex import db
from namex.constants import PaymentStatusCode
from namex.models import Request, Event, State
from namex.services import EventRecorder, queue
from namex.services.nro import NROServices
from namex.services.nro.request_utils import get_nr_header, get_nr_submitter
from namex.services.nro.utils import ora_row_to_dict

from extractor.utils.logging import setup_logging


setup_logging()

nro = NROServices()


def create_app(config=Config):
    """Return the Flask App, fully configured and ready to go."""
    app = Flask(__name__)
    app.config.from_object(config)

    queue.init_app(app)

    db.init_app(app)
    nro.init_app(app)

    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        ''' Enable Flask to automatically remove database sessions at the
         end of the request or when the application shuts down.
         Ref: http://flask.pocoo.org/docs/patterns/sqlalchemy/
        '''
        if hasattr(g, 'db_nro_session'):
            g.db_nro_session.close()

    return app


def job_result_set(ora_con, max_rows):
    """Return the set of NRs from NamesDB that are of interest."""
    ora_cursor = ora_con.cursor()

    result_set = ora_cursor.execute("""
        SELECT ID, NR_NUM, STATUS, ACTION, SEND_COUNT, SEND_TIME, ERROR_MSG
         FROM (
            SELECT *
            FROM namex.namex_feeder
            WHERE status in ('E', 'P')
            ORDER BY id
            )
            where rownum <= :max_rows
        """
                                , max_rows=max_rows
                                )
    col_names = [row[0] for row in ora_cursor.description]

    return result_set, col_names


def update_feeder_row(ora_con, row_id, status, send_count, error_message):
    """Update the feeder tracking table."""
    try:
        ora_cursor = ora_con.cursor()

        result_set = ora_cursor.execute("""
            update NAMEX.NAMEX_FEEDER set
            STATUS = :status
            ,SEND_COUNT = :send_count
            ,SEND_TIME = sysdate
            ,ERROR_MSG = :error_message
            where id = :id
            """
                                        ,id=row_id
                                        ,status=status
                                        ,send_count=send_count
                                        ,error_message=error_message
                                    )

        print('rows updated',ora_cursor.rowcount)
        if ora_cursor.rowcount > 0:
            return True
    except Exception as err:
        current_app.logger.error('UNABLE TO UPDATE NAMEX_FEEDER :', err.with_traceback(None))

    return False


def job(app, namex_db, nro_connection, user, max_rows=100):
    """Process the NRs that have been updated in the NamesDB.

    Most updates will go away as NRO (the legacy UI for the NamesDB) is decommissioned.

    The following states allow the following changes:

    - all changes allowed: DRAFT, PENDING_PAYMENT

    - no changes allowed: INPROGRESS, REFUND_REQUESTED, REJECTED, EXPIRED, HISTORICAL, COMPLETED

    - set cancelled state: CANCELLED

    - all changes, except for state: HOLD

    - consumed info only: RESERVED, COND_RESERVE, APPROVED, CONDITIONAL
    """
    row_count = 0

    try:
        ora_con = nro_connection
        # get the NRs from Oracle NamesDB of interest
        result, col_names = job_result_set(ora_con, max_rows)

        for r in result:

            row_count += 1

            row = ora_row_to_dict(col_names, r)

            nr_num = row['nr_num']
            nr = Request.find_by_nr(nr_num)
            action = row['action']

            current_app.logger.debug('processing: {}, NameX state: {}, action: {}'
                                     .format(
                nr_num,
                None if (not nr) else nr.stateCd,
                action
            ))

            # NO CHANGES ALLOWED
            if nr and (nr.stateCd in [State.INPROGRESS,
                                      State.REFUND_REQUESTED,
                                      State.REJECTED,
                                      State.EXPIRED,
                                      State.HISTORICAL,
                                      State.COMPLETED]):
                success = update_feeder_row(ora_con
                                            ,row_id=row['id']
                                            ,status='C'
                                            ,send_count=1 + 0 if (row['send_count'] is None) else row['send_count']
                                            ,error_message='Ignored - Request: not processed')
                ora_con.commit()
                # continue to next row
                current_app.logger.info('skipping: {}, NameX state: {}, action: {}'
                                        .format(
                    nr_num,
                    None if (not nr) else nr.stateCd,
                    action
                ))
                continue

            # ignore existing NRs not in a completed state or draft, or in a completed state and not furnished
            if nr and (nr.stateCd not in State.COMPLETED_STATE + [State.DRAFT] or (nr.stateCd in State.COMPLETED_STATE and nr.furnished == 'N')):
                success = update_feeder_row(
                    ora_con,
                    row_id=row['id'],
                    status='C',
                    send_count=1 + 0 if (row['send_count'] is None) else row['send_count'],
                    error_message='Ignored - Request: not processed'
                )
                ora_con.commit()
                continue
            # for any NRs in a completed state or new NRs not existing in NameX
            else:  # pylint: disable=R1724: Unnecessary "else"
                try:
                    # get submitter
                    ora_cursor = ora_con.cursor()
                    nr_header = get_nr_header(ora_cursor, nr_num)
                    nr_submitter = get_nr_submitter(ora_cursor, nr_header['request_id'])
                    # get pending payments
                    pending_payments = []
                    if nr:
                        pending_payments = [x for x in nr.payments.all() if x.payment_status_code == PaymentStatusCode.CREATED.value]
                    # ignore if:
                    # - NR does not exist and NR originated in namex (handles racetime condition for when it is still in the process of saving)
                    # - NR has a pending update from namex (pending payment)
                    if (not nr and nr_submitter and nr_submitter.get('submitter', '') == 'namex') or (nr and len(pending_payments) > 0):
                        success = update_feeder_row(
                            ora_con,
                            row_id=row['id'],
                            status='C',
                            send_count=1 + 0 if (row['send_count'] is None) else row['send_count'],
                            error_message='Ignored - Request: not processed'
                        )
                        ora_con.commit()
                    else:
                        nr = nro.fetch_nro_request_and_copy_to_namex_request(user, nr_number=nr_num, name_request=nr)

                        namex_db.session.add(nr)
                        EventRecorder.record(user, Event.UPDATE_FROM_NRO, nr, nr.json(), save_to_session=True)
                        current_app.logger.debug('EventRecorder should have been saved to by now, although not committed')
                        success = update_feeder_row(ora_con
                                                    , row_id=row['id']
                                                    , status='C'
                                                    , send_count=1 + 0 if (row['send_count'] is None) else row['send_count']
                                                    , error_message=None)

                        if success:
                            ora_con.commit()
                            current_app.logger.debug('Oracle commit done')
                            namex_db.session.commit()
                            current_app.logger.debug('Postgresql commit done')
                        else:
                            raise Exception()

                except Exception as err:
                    current_app.logger.error(err.with_traceback(None))
                    success = update_feeder_row(ora_con
                                                , row_id=row['id']
                                                , status=row['status']
                                                , send_count=1 + 0 if (row['send_count'] is None) else row['send_count']
                                                , error_message=err.with_traceback(None))
                    namex_db.session.rollback()
                    ora_con.commit()
        time.sleep(20)
        return row_count

    except Exception as err:
        current_app.logger.error('Update Failed:', err.with_traceback(None))
        return -1
