"""Requests used to support the namex API

TODO: Fill in a larger description once the API is defined for V1
"""
from flask import request, jsonify, g, current_app, get_flashed_messages
from flask_restplus import Namespace, Resource, fields, cors
from flask_jwt_oidc import AuthError

from namex.utils.logging import setup_logging
setup_logging() ## important to do this first

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func, text
from sqlalchemy.inspection import inspect

from namex import jwt, nro, services
from namex.exceptions import BusinessException
from namex.models import db, ValidationError
from namex.models import Request as RequestDAO, RequestsSchema, RequestsHeaderSchema, RequestsSearchSchema
from namex.models import Name, NameSchema, PartnerNameSystemSchema
from namex.models import User, State, Comment, NameCommentSchema, Event
from namex.models import ApplicantSchema
from namex.models import DecisionReason

from namex.services import ServicesError, MessageServices, EventRecorder

from namex.services.name_request import check_ownership, get_or_create_user_by_jwt, valid_state_transition, convert_to_ascii
from namex.utils.util import cors_preflight
from namex.analytics import SolrQueries, RestrictedWords, VALID_ANALYSIS as ANALYTICS_VALID_ANALYSIS
from namex.services.nro import NROServicesError
from namex.services.name_request.auto_analyse.protected_name_analysis import ProtectedNameAnalysisService

import datetime
from datetime import datetime as dt
import json
import urllib
import sys
from http import HTTPStatus

# Register a local namespace for the requests
api = Namespace('nameRequests', description='Name Request System - Core API for reviewing a Name Request')

# Marshmallow schemas
request_schema = RequestsSchema(many=False)
request_schemas = RequestsSchema(many=True)
request_header_schema = RequestsHeaderSchema(many=False)
request_search_schemas = RequestsSearchSchema(many=True)

names_schema = NameSchema(many=False)
names_schemas = NameSchema(many=True)
nwpta_schema = PartnerNameSystemSchema(many=False)
name_comment_schema = NameCommentSchema(many=False)

applicant_schema = ApplicantSchema(many=False)


@api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


# noinspection PyUnresolvedReferences
@cors_preflight("GET")
@api.route('/echo', methods=['GET', 'OPTIONS'])
class Echo(Resource):
    """Helper method to echo back all your JWT token info
    """
    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def get(*args, **kwargs):
        try:
            return jsonify(g.jwt_oidc_token_info), 200
        except Exception as err:
            return {"error": "{}".format(err)}, 500


#################### QUEUES #######################
@cors_preflight("GET")
@api.route('/queues/@me/oldest', methods=['GET','OPTIONS'])
class RequestsQueue(Resource):
    """Acting like a QUEUE this gets the next NR (just the NR number)
    and assigns it to your auth id, and marks it as INPROGRESS
    """
    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_roles([User.APPROVER])
    def get():
        """ Gets the oldest nr num, that is in DRAFT status
        It then marks the NR as INPROGRESS, and assigns it to the User as found in the JWT
        It also moves control of the Request from NRO so that NameX fully owns it

        :Authorization: (JWT): valid JWT with the User.APPROVER role

        :return: (str) (dict) (https status): 500, 404, or NR NUM, or NR NUM and a system alert in the dict
        """

        # GET existing or CREATE new user based on the JWT info
        try:
            user = get_or_create_user_by_jwt(g.jwt_oidc_token_info)
        except ServicesError as se:
            return jsonify(message='unable to get ot create user, aborting operation'), 500
        except Exception as unmanaged_error:
            current_app.logger.error(unmanaged_error.with_traceback(None))
            return jsonify(message='internal server error'), 500

        # get the next NR assigned to the User
        try:
            nr, new_assignment = RequestDAO.get_queued_oldest(user)
        except BusinessException as be:
            return jsonify(message='There are no more requests in the {} Queue'.format(State.DRAFT)), 404
        except Exception as unmanaged_error:
            current_app.logger.error(unmanaged_error.with_traceback(None))
            return jsonify(message='internal server error'), 500
        current_app.logger.debug('got the nr:{} and its a new assignment?{}'.format(nr.nrNum, new_assignment))

        # if no NR returned
        if 'nr' not in locals() or not nr:
            return jsonify(message='No more NRs in Queue to process'), 200

        # if it's an NR already INPROGRESS and assigned to the user
        if nr and not new_assignment:
            return jsonify(nameRequest='{}'.format(nr.nrNum)), 200

        # if it's a new assignment, then LOGICALLY lock the record in NRO
        # if we fail to do that, send back the NR and the errors for user-intervention
        if new_assignment:
            warnings = nro.move_control_of_request_from_nro(nr, user)

        if 'warnings' in locals() and warnings:
            return jsonify(nameRequest='{}'.format(nr.nrNum), warnings=warnings), 206

        EventRecorder.record(user, Event.GET, nr, {})

        return jsonify(nameRequest='{}'.format(nr.nrNum)), 200


@cors_preflight('GET, POST')
@api.route('', methods=['GET', 'POST', 'OPTIONS'])
class Requests(Resource):
    a_request = api.model('Request', {'submitter': fields.String('The submitter name'),
                                      'corpType': fields.String('The corporation type'),
                                      'reqType': fields.String('The name request type')
                                      })

    START=0
    ROWS=10

    # search_request_schemas = RequestsSchema(many=True)
        # ,exclude=['id'
        #     ,'applicants'
        #     ,'partnerNS'
        #     ,'requestId'
        #     ,'previousRequestId'])

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def get(*args, **kwargs):
        # validate row & start params
        start = request.args.get('start', Requests.START)
        rows = request.args.get('rows',Requests.ROWS)
        try:
            start = int(start)
            rows = int(rows)
        except Exception as err:
            current_app.logger.info('start or rows not an int, err: {}'.format(err))
            return jsonify({'message': 'paging parameters were not integers'}), 406

        # queue must be a list of states
        queue = request.args.get('queue', None)
        if queue:
            if queue == 'COMPLETED':
                queue = 'APPROVED,CONDITIONAL,REJECTED'
            queue = queue.upper().split(',')
            for q in queue:
                if q not in State.VALID_STATES:
                    return jsonify({'message': '\'{}\' is not a valid queue'.format(queue)}), 406

        # order must be a string of 'column:asc,column:desc'
        order = request.args.get('order', 'submittedDate:desc,stateCd:desc')
        # order=dict((x.split(":")) for x in order.split(',')) // con't pass as a dict as the order is lost

        # create the order by txt, looping through Request Attributes and mapping to column names
        # TODO: this is fragile across joins, fix it up if queries are going to sort across joins
        cols = inspect(RequestDAO).columns
        col_keys = cols.keys()
        sort_by = ''
        order_list = ''
        for k,v in ((x.split(":")) for x in order.split(',')):
            vl = v.lower()
            if (k in col_keys) and (vl == 'asc' or vl == 'desc'):
                if len(sort_by) > 0:
                    sort_by = sort_by + ', '
                    order_list = order_list + ', '
                sort_by = sort_by + '{columns} {direction} NULLS LAST'.format(columns=cols[k], direction=vl)
                order_list = order_list + '{attribute} {direction} NULLS LAST'.format(attribute=k, direction=vl)

        # Assemble the query
        nrNum = request.args.get('nrNum', None)
        activeUser = request.args.get('activeUser', None)
        compName = request.args.get('compName', None)
        priority = request.args.get('ranking', None)
        notification = request.args.get('notification', None)
        submittedInterval = request.args.get('submittedInterval', None)
        lastUpdateInterval = request.args.get('lastUpdateInterval', None)
        current_hour = int(request.args.get('hour', 0))

        q = RequestDAO.query.filter()
        if queue: q = q.filter(RequestDAO.stateCd.in_(queue))

        if nrNum:
            nrNum = nrNum.replace('NR', '').strip()
            nrNum = nrNum.replace('nr', '').strip()
            nrNum = '%'+nrNum+'%'
            q = q.filter(RequestDAO.nrNum.like(nrNum))
        if activeUser:
            q = q.join(RequestDAO.activeUser).filter(User.username.ilike('%'+activeUser+'%'))

        #TODO: fix count on search by compName -- returns count of all names that match
        # -- want it to be all NRs (nrs can have multiple names that match)
        # ---- right now count is adjusted on the frontend in method 'populateTable'
        if compName:
            q = q.join(RequestDAO.names).filter(Name.name.ilike('%' + compName + '%'))

        if priority == 'Standard':
            q = q.filter(RequestDAO.priorityCd != 'Y')
        elif priority == 'Priority':
            q = q.filter(RequestDAO.priorityCd != 'N')

        if notification == 'Notified':
            q = q.filter(RequestDAO.furnished != 'N')
        elif notification == 'Not Notified':
            q = q.filter(RequestDAO.furnished != 'Y')

        if submittedInterval == 'Today':
            q = q.filter(RequestDAO.submittedDate > text(
                'NOW() - INTERVAL \'{hour_offset} HOURS\''.format(hour_offset=current_hour)))
        elif submittedInterval == '7 days':
            q = q.filter(RequestDAO.submittedDate > text(
                'NOW() - INTERVAL \'{hour_offset} HOURS\''.format(hour_offset=current_hour+24*6)))
        elif submittedInterval == '30 days':
            q = q.filter(RequestDAO.submittedDate > text(
                'NOW() - INTERVAL \'{hour_offset} HOURS\''.format(hour_offset=current_hour+24*29)))
        elif submittedInterval == '90 days':
            q = q.filter(RequestDAO.submittedDate > text(
                'NOW() - INTERVAL \'{hour_offset} HOURS\''.format(hour_offset=current_hour+24*89)))
        elif submittedInterval == '1 year':
            q = q.filter(RequestDAO.submittedDate > text('NOW() - INTERVAL \'1 YEARS\''))
        elif submittedInterval == '3 years':
            q = q.filter(RequestDAO.submittedDate > text('NOW() - INTERVAL \'3 YEARS\''))
        elif submittedInterval == '5 years':
            q = q.filter(RequestDAO.submittedDate > text('NOW() - INTERVAL \'5 YEARS\''))

        if lastUpdateInterval == 'Today':
            q = q.filter(RequestDAO.lastUpdate > text(
                '(now() at time zone \'utc\') - INTERVAL \'{hour_offset} HOURS\''.format(hour_offset=current_hour)))
        if lastUpdateInterval == 'Yesterday':
            today_offset = current_hour
            yesterday_offset = today_offset+24
            q = q.filter(RequestDAO.lastUpdate < text(
                '(now() at time zone \'utc\') - INTERVAL \'{today_offset} HOURS\''.format(today_offset=today_offset)))
            q = q.filter(RequestDAO.lastUpdate > text(
                '(now() at time zone \'utc\') - INTERVAL \'{yesterday_offset} HOURS\''.format(yesterday_offset=yesterday_offset)))
        elif lastUpdateInterval == '2 days':
            q = q.filter(RequestDAO.lastUpdate > text(
                '(now() at time zone \'utc\') - INTERVAL \'{hour_offset} HOURS\''.format(hour_offset=current_hour+24)))
        elif lastUpdateInterval == '7 days':
            q = q.filter(RequestDAO.lastUpdate > text(
                '(now() at time zone \'utc\') - INTERVAL \'{hour_offset} HOURS\''.format(hour_offset=current_hour + 24*6)))
        elif lastUpdateInterval == '30 days':
            q = q.filter(RequestDAO.lastUpdate > text(
                '(now() at time zone \'utc\') - INTERVAL \'{hour_offset} HOURS\''.format(hour_offset=current_hour + 24*29)))

        q = q.order_by(text(sort_by))

        # get a count of the full set size, this ignore the offset & limit settings
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = db.session.execute(count_q).scalar()

        # Add the paging
        q = q.offset(start)
        q = q.limit(rows)

        # create the response
        rep = {'response':{'start':start,
                           'rows': rows,
                           'numFound': count,
                           'numPriorities': 0,
                           'numUpdatedToday': 0,
                           'queue': queue,
                           'order': order_list
                           },
               'nameRequests': request_search_schemas.dump(q.all())
               }

        return jsonify(rep), 200
        return jsonify(rep), 200

    # @api.errorhandler(AuthError)
    # def handle_auth_error(ex):
    #     response = jsonify(ex.error)
    #     response.status_code = ex.status_code
        # return response, 401
        # return {}, 401

    # noinspection PyUnusedLocal,PyUnusedLocal
    @api.expect(a_request)
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def post(self, *args, **kwargs):

        current_app.logger.info('Someone is trying to post a new request')
        return jsonify({'message': 'Not Implemented'}), 501


# noinspection PyUnresolvedReferences
@cors_preflight("GET, PATCH, PUT, DELETE")
@api.route('/<string:nr>', methods=['GET', 'PATCH', 'PUT', 'DELETE', 'OPTIONS'])
class Request(Resource):

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.has_one_of_roles([User.APPROVER, User.EDITOR, User.VIEWONLY, User.SYSTEM])
    def get(nr):

        # return jsonify(request_schema.dump(RequestDAO.query.filter_by(nr=nr.upper()).first_or_404()))
        return jsonify(RequestDAO.query.filter_by(nrNum =nr.upper()).first_or_404().json())

    @staticmethod
    # @cors.crossdomain(origin='*')
    @jwt.requires_roles([User.APPROVER, User.EDITOR])
    def delete(nr):

        return '', 501 # not implemented
        # nrd = RequestDAO.find_by_nr(nr)
        # even if not found we still return a 204, which is expected spec behaviour
        # if nrd:
        #     nrd.stateCd = State.CANCELLED
        #     nrd.save_to_db()
        #
        # return '', 204

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.has_one_of_roles([User.APPROVER, User.EDITOR, User.SYSTEM])
    def patch(nr, *args, **kwargs):
        """  Patches the NR. Currently only handles STATE (with optional comment) and Previous State.

        :param nr (str): NameRequest Number in the format of 'NR 000000000'
        :param args:  __futures__
        :param kwargs: __futures__
        :return: 200 - success; 40X for errors

        :HEADER: Valid JWT Bearer Token for a valid REALM
        :JWT Scopes: - USER.APPROVER, USER.EDITOR

        APPROVERS: Can change from almost any state, other than CANCELLED, EXPIRED and ( COMPLETED not yet furnished )
        EDITOR: Can't change to a COMPLETED state (ACCEPTED, REJECTED, CONDITION)
        SYSTEM: Can consume a Name Request.
        """

        # do the cheap check first before the more expensive ones
        #check states
        json_input = request.get_json()
        if not json_input:
            return jsonify({'message': 'No input data provided'}), 400

        # find NR
        try:
            user = get_or_create_user_by_jwt(g.jwt_oidc_token_info)
            nrd = RequestDAO.find_by_nr(nr)
            if not nrd:
                return jsonify({"message": "Request:{} not found".format(nr)}), 404
            start_state = nrd.stateCd
        except NoResultFound as nrf:
            # not an error we need to track in the log
            return jsonify({"message": "Request:{} not found".format(nr)}), 404
        except Exception as err:
            current_app.logger.error("Error when patching NR:{0} Err:{1}".format(nr, err))
            return jsonify({"message": "NR had an internal error"}), 404

        try:

            consume = json_input.get('consume', None)
            state = json_input.get('state', None)

            if consume:
                try:
                    corp_num = consume['corpNum']
                    #@TODO add corpnum validation
                except KeyError:
                    return jsonify({"message": "corpNum is required"}), HTTPStatus.BAD_REQUEST

                current_app.logger.debug(f'system consuming a NR, in nrd.stateCd:{nrd.stateCd} by: {jwt.validate_roles([User.APPROVER])}')
                if nrd.stateCd not in (State.APPROVED, State.CONDITIONAL) \
                    or not jwt.validate_roles([User.SYSTEM]):
                    return jsonify({"message": "either not authorized or not in a valid state to consume"}), HTTPStatus.UNAUTHORIZED
                
                warnings = nro.consume_nr(nrd, user.username, corp_num)

            ### STATE ###
            # all these checks to get removed to marshmallow
            elif state:

                if state not in State.VALID_STATES:
                    return jsonify({"message": "not a valid state"}), 406

                if not nrd:
                    return jsonify({"message": "Request:{} not found".format(nr)}), 404

                if not services.name_request.valid_state_transition(user, nrd, state):
                    return jsonify(message='you are not authorized to make these changes'), 401

                # if the user has an existing (different) INPROGRESS NR, revert to previous state (default to HOLD)
                existing_nr = RequestDAO.get_inprogress(user)
                if existing_nr:
                    if existing_nr.previousStateCd:
                        existing_nr.stateCd = existing_nr.previousStateCd
                        existing_nr.previousStateCd = None
                    else:
                        existing_nr.stateCd = State.HOLD
                    existing_nr.save_to_db()

                # if the NR is in DRAFT then LOGICALLY lock the record in NRO
                # if we fail to do that, send back the NR and the errors for user-intervention
                if nrd.stateCd == State.DRAFT:
                    warnings = nro.move_control_of_request_from_nro(nrd, user)

                # if we're changing to DRAFT, update NRO status to "D" in NRO
                if state == State.DRAFT:
                    change_flags = {
                        'is_changed__request': False,
                        'is_changed__previous_request': False,
                        'is_changed__applicant': False,
                        'is_changed__address': False,
                        'is_changed__name1': False,
                        'is_changed__name2': False,
                        'is_changed__name3': False,
                        'is_changed__nwpta_ab': False,
                        'is_changed__nwpta_sk': False,
                        'is_changed__request_state': True,
                        'is_changed_consent': False
                    }

                    warnings = nro.change_nr(nrd, change_flags)
                    if warnings:
                        MessageServices.add_message(MessageServices.ERROR,
                                                    'change_request_in_NRO', warnings)

                nrd.stateCd = state
                nrd.userId = user.id

                if state == State.CANCELLED:
                    nro.cancel_nr(nrd, user.username)

                # if our state wasn't INPROGRESS and it is now, ensure the furnished flag is N
                if (start_state in locals()
                        and start_state != State.INPROGRESS
                        and nrd.stateCd == State.INPROGRESS):
                    # set / reset the furnished flag to N
                    nrd.furnished = 'N'

                # if we're changing to a completed or cancelled state, clear reset flag on NR record
                if state in State.COMPLETED_STATE + [State.CANCELLED]:
                    nrd.hasBeenReset = False
                    if nrd.stateCd == State.CONDITIONAL and nrd.consentFlag is None:
                        nrd.consentFlag = 'Y'


                ### COMMENTS ###
                # we only add new comments, we do not change existing comments
                # - we can find new comments in json as those with no ID

                if json_input.get('comments', None):

                    for in_comment in json_input['comments']:
                        is_new_comment = False
                        try:
                            if in_comment['id'] is None or in_comment['id'] == 0:
                                is_new_comment = True
                        except KeyError:
                            is_new_comment = True
                        if is_new_comment and in_comment['comment'] is not None:
                            new_comment = Comment()
                            new_comment.comment = convert_to_ascii(in_comment['comment'])
                            new_comment.examiner = user
                            new_comment.nrId = nrd.id

                ### END comments ###


                ### PREVIOUS STATE ###
                #- None (null) is a valid value for Previous State
                if 'previousStateCd' in json_input.keys():
                    nrd.previousStateCd = json_input.get('previousStateCd', None)

                # save record
                nrd.save_to_db()
            EventRecorder.record(user, Event.PATCH, nrd, json_input)

        except Exception as err:
            current_app.logger.debug(err.with_traceback(None))
            return jsonify(message='Internal server error'), 500

        if 'warnings' in locals() and warnings:
            return jsonify(message='Request:{} - patched'.format(nr), warnings=warnings), 206
        return jsonify(message='Request:{} - patched'.format(nr)), 200

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.has_one_of_roles([User.APPROVER, User.EDITOR])
    def put(nr, *args, **kwargs):

        # do the cheap check first before the more expensive ones
        json_input = request.get_json()
        if not json_input:
            return jsonify(message='No input data provided'), 400
        current_app.logger.debug(json_input)

        nr_num = json_input.get('nrNum', None)
        if nr_num and nr_num != nr:
            return jsonify(message='Data contains a different NR# than this resource'), 400

        state = json_input.get('state', None)
        if not state:
            return jsonify({"message": "state not set"}), 406

        if state not in State.VALID_STATES:
            return jsonify({"message": "not a valid state"}), 406

        try:
            user = get_or_create_user_by_jwt(g.jwt_oidc_token_info)
            nrd = RequestDAO.find_by_nr(nr)
            if not nrd:
                return jsonify({"message": "Request:{} not found".format(nr)}), 404
            orig_nrd = nrd.json()
        except NoResultFound as nrf:
            # not an error we need to track in the log
            return jsonify({"message": "Request:{} not found".format(nr)}), 404
        except Exception as err:
            current_app.logger.error("Error when patching NR:{0} Err:{1}".format(nr, err))
            return jsonify({"message": "NR had an internal error"}), 404

        if not services.name_request.valid_state_transition(user, nrd, state):
            return jsonify(message='you are not authorized to make these changes'), 401

        name_choice_exists = {1: False, 2: False, 3: False}
        for name in json_input.get('names', None):
            if name['name'] and name['name'] is not '':
                name_choice_exists[name['choice']] = True
        if not name_choice_exists[1]:
            return jsonify(message='Data does not include a name choice 1'), 400
        if not name_choice_exists[2] and name_choice_exists[3]:
            return jsonify(message='Data contains a name choice 3 without a name choice 2'), 400

        try:
            existing_nr = RequestDAO.get_inprogress(user)
            if existing_nr:
                existing_nr.stateCd = State.HOLD
                existing_nr.save_to_db()

            # convert Expiration Date to correct format
            if json_input.get('expirationDate', None):
                json_input['expirationDate'] = str(datetime.datetime.strptime(
                    str(json_input['expirationDate'][5:]), '%d %b %Y %H:%M:%S %Z'))

            # convert Submitted Date to correct format
            if json_input.get('submittedDate', None):
                json_input['submittedDate'] = str(datetime.datetime.strptime(
                    str(json_input['submittedDate'][5:]), '%d %b %Y %H:%M:%S %Z'))


            if json_input.get('consent_dt', None):
                json_input['consent_dt'] = str(datetime.datetime.strptime(
                    str(json_input['consent_dt'][5:]), '%d %b %Y %H:%M:%S %Z'))

            # convert NWPTA dates to correct format
            if json_input.get('nwpta', None):
                for region in json_input['nwpta']:
                    try:
                        if region['partnerNameDate'] == '':
                            region['partnerNameDate'] = None
                        if region['partnerNameDate']:
                            region['partnerNameDate'] = str(datetime.datetime.strptime(
                                str(region['partnerNameDate']), '%d-%m-%Y'))
                    except ValueError:
                        pass
                        # pass on this error and catch it when trying to add to record, to be returned

            # ## If the current state is DRAFT, the transfer control from NRO to NAMEX
            # if the NR is in DRAFT then LOGICALLY lock the record in NRO
            # if we fail to do that, send back the NR and the errors for user-intervention
            if nrd.stateCd == State.DRAFT:
                warnings = nro.move_control_of_request_from_nro(nrd, user)
                if warnings:
                    MessageServices.add_message(MessageServices.WARN, 'nro_lock', warnings)


            ### REQUEST HEADER ###

            # update request header

            errors = request_header_schema.validate(json_input, partial=True)
            if errors:
                # return jsonify(errors), 400
                MessageServices.add_message(MessageServices.ERROR, 'request_validation', errors)

            # if reset is set to true then this nr will be set to H + name_examination proc will be called in oracle
            reset = False
            if nrd.furnished == RequestDAO.REQUEST_FURNISHED and json_input.get('furnished', None) == 'N':
                reset = True

            request_header_schema.load(json_input, instance=nrd, partial=True)
            nrd.additionalInfo = convert_to_ascii(json_input.get('additionalInfo', None))
            nrd.furnished = json_input.get('furnished', 'N')
            nrd.natureBusinessInfo = convert_to_ascii(json_input.get('natureBusinessInfo', None))
            nrd.stateCd = state
            nrd.userId = user.id
            nrd.consentFlag = json_input.get('consentFlag',None)
            nrd.consent_dt = json_input.get('consent_dt',None)

            if reset:
                # set the flag indicating that the NR has been reset
                nrd.hasBeenReset = True

                # add a generated comment re. this NR being reset
                json_input['comments'].append({'comment': 'This NR was RESET.'})

            try:
                previousNr = json_input['previousNr']
                nrd.previousRequestId = RequestDAO.find_by_nr(previousNr).requestId
            except AttributeError:
                nrd.previousRequestId = None
            except KeyError:
                nrd.previousRequestId = None

            # if we're changing to a completed or cancelled state, clear reset flag on NR record
            if state in State.COMPLETED_STATE + [State.CANCELLED]:
                nrd.hasBeenReset = False


            # check if any of the Oracle db fields have changed, so we can send them back
            is_changed__request = False
            is_changed__previous_request = False
            is_changed__request_state = False
            is_changed_consent = False
            if nrd.requestTypeCd != orig_nrd['requestTypeCd']: is_changed__request = True
            if nrd.expirationDate != orig_nrd['expirationDate']: is_changed__request = True
            if nrd.xproJurisdiction != orig_nrd['xproJurisdiction']: is_changed__request = True
            if nrd.additionalInfo != orig_nrd['additionalInfo']: is_changed__request = True
            if nrd.natureBusinessInfo != orig_nrd['natureBusinessInfo']: is_changed__request = True
            if nrd.previousRequestId != orig_nrd['previousRequestId']: is_changed__previous_request = True
            if nrd.stateCd != orig_nrd['state']: is_changed__request_state = True
            if nrd.consentFlag != orig_nrd['consentFlag'] : is_changed_consent = True

            #Need this for a re-open
            if nrd.stateCd != State.CONDITIONAL and is_changed__request_state:
               nrd.consentFlag = None
               nrd.consent_dt = None


            ### END request header ###

            ### APPLICANTS ###
            is_changed__applicant = False
            is_changed__address = False

            applicants_d = nrd.applicants.one_or_none()
            if applicants_d:
                orig_applicant = applicants_d.as_dict()
                appl = json_input.get('applicants', None)
                if appl:
                    errm = applicant_schema.validate(appl, partial=True)
                    if errm:
                        # return jsonify(errm), 400
                        MessageServices.add_message(MessageServices.ERROR, 'applicants_validation', errm)


                    applicant_schema.load(appl, instance=applicants_d, partial=True)

                    # convert data to ascii, removing data that won't save to Oracle
                    applicants_d.lastName = convert_to_ascii(applicants_d.lastName)
                    applicants_d.firstName = convert_to_ascii(applicants_d.firstName)
                    applicants_d.middleName = convert_to_ascii(applicants_d.middleName)
                    applicants_d.phoneNumber = convert_to_ascii(applicants_d.phoneNumber)
                    applicants_d.faxNumber = convert_to_ascii(applicants_d.faxNumber)
                    applicants_d.emailAddress = convert_to_ascii(applicants_d.emailAddress)
                    applicants_d.contact = convert_to_ascii(applicants_d.contact)
                    applicants_d.clientFirstName = convert_to_ascii(applicants_d.clientFirstName)
                    applicants_d.clientLastName = convert_to_ascii(applicants_d.clientLastName)
                    applicants_d.addrLine1 = convert_to_ascii(applicants_d.addrLine1)
                    applicants_d.addrLine2 = convert_to_ascii(applicants_d.addrLine2)
                    applicants_d.addrLine3 = convert_to_ascii(applicants_d.addrLine3)
                    applicants_d.city = convert_to_ascii(applicants_d.city)
                    applicants_d.postalCd = convert_to_ascii(applicants_d.postalCd)
                    applicants_d.stateProvinceCd = convert_to_ascii(applicants_d.stateProvinceCd)
                    applicants_d.countryTypeCd = convert_to_ascii(applicants_d.countryTypeCd)

                    # check if any of the Oracle db fields have changed, so we can send them back
                    if applicants_d.lastName != orig_applicant['lastName']: is_changed__applicant = True
                    if applicants_d.firstName != orig_applicant['firstName']: is_changed__applicant = True
                    if applicants_d.middleName != orig_applicant['middleName']: is_changed__applicant = True
                    if applicants_d.phoneNumber != orig_applicant['phoneNumber']: is_changed__applicant = True
                    if applicants_d.faxNumber != orig_applicant['faxNumber']: is_changed__applicant = True
                    if applicants_d.emailAddress != orig_applicant['emailAddress']: is_changed__applicant = True
                    if applicants_d.contact != orig_applicant['contact']: is_changed__applicant = True
                    if applicants_d.clientFirstName != orig_applicant['clientFirstName']: is_changed__applicant = True
                    if applicants_d.clientLastName != orig_applicant['clientLastName']: is_changed__applicant = True
                    if applicants_d.declineNotificationInd != orig_applicant['declineNotificationInd']: is_changed__applicant = True
                    if applicants_d.addrLine1 != orig_applicant['addrLine1']: is_changed__address = True
                    if applicants_d.addrLine2 != orig_applicant['addrLine2']: is_changed__address = True
                    if applicants_d.addrLine3 != orig_applicant['addrLine3']: is_changed__address = True
                    if applicants_d.city != orig_applicant['city']: is_changed__address = True
                    if applicants_d.postalCd != orig_applicant['postalCd']: is_changed__address = True
                    if applicants_d.stateProvinceCd != orig_applicant['stateProvinceCd']: is_changed__address = True
                    if applicants_d.countryTypeCd != orig_applicant['countryTypeCd']: is_changed__address = True

                else:
                    applicants_d.delete_from_db()
                    is_changed__applicant = True
                    is_changed__address = True



            ### END applicants ###

            ### NAMES ###
            # TODO: set consumptionDate not working -- breaks changing name values

            is_changed__name1 = False
            is_changed__name2 = False
            is_changed__name3 = False
            deleted_names = [False] * 3

            if len(nrd.names.all()) == 0:
                new_name_choice = Name()
                new_name_choice.nrId = nrd.id

                # convert data to ascii, removing data that won't save to Oracle
                new_name_choice.name = convert_to_ascii(new_name_choice.name)

                nrd.names.append(new_name_choice)


            for nrd_name in nrd.names.all():

                orig_name = nrd_name.as_dict()

                for in_name in json_input.get('names', []):

                    if len(nrd.names.all()) < in_name['choice']:

                        errors = names_schema.validate(in_name, partial=False)
                        if errors:
                            MessageServices.add_message(MessageServices.ERROR, 'names_validation', errors)
                            # return jsonify(errors), 400

                        new_name_choice = Name()
                        new_name_choice.nrId = nrd.id

                        names_schema.load(in_name, instance=new_name_choice, partial=False)

                        # convert data to ascii, removing data that won't save to Oracle
                        # - also force uppercase
                        new_name_choice.name = convert_to_ascii(new_name_choice.name.upper())

                        nrd.names.append(new_name_choice)

                        if new_name_choice.choice == 2: is_changed__name2 = True
                        if new_name_choice.choice == 3: is_changed__name3 = True

                    elif nrd_name.choice == in_name['choice']:
                        errors = names_schema.validate(in_name, partial=False)
                        if errors:
                            MessageServices.add_message(MessageServices.ERROR, 'names_validation', errors)
                            # return jsonify(errors), 400

                        names_schema.load(in_name, instance=nrd_name, partial=False)

                        # set comments (existing or cleared)
                        if in_name.get('comment', None) is not None:

                            # if there is a comment ID in data, just set it
                            if in_name['comment'].get('id', None) is not None:
                                nrd_name.commentId = in_name['comment'].get('id')

                            # if no comment id, it's a new comment, so add it
                            else:
                                # no business case for this at this point - this code will never run
                                pass

                        else:
                            nrd_name.comment = None

                        # convert data to ascii, removing data that won't save to Oracle
                        # - also force uppercase
                        nrd_name.name = convert_to_ascii(nrd_name.name)
                        if (nrd_name.name is not None): nrd_name.name = nrd_name.name.upper()

                        # check if any of the Oracle db fields have changed, so we can send them back
                        # - this is only for editing a name from the Edit NR section, NOT making a decision
                        if nrd_name.name != orig_name['name']:
                            if nrd_name.choice == 1:
                                is_changed__name1 = True
                                json_input['comments'].append({'comment': 'Name choice 1 changed from {0} to {1}'\
                                                                    .format(orig_name['name'], nrd_name.name)})
                            if nrd_name.choice == 2:
                                is_changed__name2 = True
                                if not nrd_name.name:
                                    deleted_names[nrd_name.choice - 1] = True
                                json_input['comments'].append({'comment': 'Name choice 2 changed from {0} to {1}'\
                                                                    .format(orig_name['name'], nrd_name.name)})
                            if nrd_name.choice == 3:
                                is_changed__name3 = True
                                if not nrd_name.name:
                                    deleted_names[nrd_name.choice - 1] = True
                                json_input['comments'].append({'comment': 'Name choice 3 changed from {0} to {1}'\
                                                                    .format(orig_name['name'], nrd_name.name)})
            ### END names ###

            ### COMMENTS ###

            # we only add new comments, we do not change existing comments
            # - we can find new comments in json as those with no ID
            # - This must come after names section above, to handle comments re. changed names.

            for in_comment in json_input['comments']:
                is_new_comment = False
                try:
                    if in_comment['id'] is None or in_comment['id'] == 0:
                        is_new_comment = True
                except KeyError:
                    is_new_comment = True
                if is_new_comment and in_comment['comment'] is not None:
                    new_comment = Comment()
                    new_comment.comment = convert_to_ascii(in_comment['comment'])
                    new_comment.examiner = user
                    new_comment.nrId = nrd.id

            ### END comments ###

            ### NWPTA ###

            is_changed__nwpta_ab = False
            is_changed__nwpta_sk = False

            for nrd_nwpta in nrd.partnerNS.all():

                orig_nwpta = nrd_nwpta.as_dict()

                for in_nwpta in json_input['nwpta']:
                    if nrd_nwpta.partnerJurisdictionTypeCd == in_nwpta['partnerJurisdictionTypeCd']:

                        errors = nwpta_schema.validate(in_nwpta, partial=False)
                        if errors:
                            MessageServices.add_message(MessageServices.ERROR, 'nwpta_validation', errors)
                            # return jsonify(errors), 400

                        nwpta_schema.load(in_nwpta, instance=nrd_nwpta, partial=False)

                        # convert data to ascii, removing data that won't save to Oracle
                        nrd_nwpta.partnerName = convert_to_ascii(nrd_nwpta.partnerName)
                        nrd_nwpta.partnerNameNumber = convert_to_ascii(nrd_nwpta.partnerNameNumber)


                        # check if any of the Oracle db fields have changed, so we can send them back
                        tmp_is_changed = False
                        if nrd_nwpta.partnerNameTypeCd != orig_nwpta['partnerNameTypeCd']: tmp_is_changed = True
                        if nrd_nwpta.partnerNameNumber != orig_nwpta['partnerNameNumber']: tmp_is_changed = True
                        if nrd_nwpta.partnerNameDate != orig_nwpta['partnerNameDate']: tmp_is_changed = True
                        if nrd_nwpta.partnerName != orig_nwpta['partnerName']: tmp_is_changed = True
                        if tmp_is_changed:
                            if nrd_nwpta.partnerJurisdictionTypeCd == 'AB': is_changed__nwpta_ab = True
                            if nrd_nwpta.partnerJurisdictionTypeCd == 'SK': is_changed__nwpta_sk = True


            ### END nwpta ###

            # if there were errors, abandon changes and return the set of errors
            warning_and_errors = MessageServices.get_all_messages()
            if warning_and_errors:
                for we in warning_and_errors:
                    if we['type'] == MessageServices.ERROR:
                        return jsonify(errors=warning_and_errors), 400


            # update oracle if this nr was reset
            # - first set status to H via name_examination proc, which handles clearing all necessary data and states
            # - then set status to D so it's back in draft in NRO for customer to understand status
            if reset:
                current_app.logger.debug('set state to h for RESET')
                try:
                    nro.set_request_status_to_h(nr, user.username)
                except (NROServicesError, Exception) as err:
                    MessageServices.add_message('error', 'reset_request_in_NRO', err)

                nrd.expirationDate = None
                nrd.consentFlag = None
                nrd.consent_dt = None
                is_changed__request = True
                is_changed_consent = True

                change_flags = {
                    'is_changed__request': is_changed__request,
                    'is_changed__previous_request': False,
                    'is_changed__applicant': False,
                    'is_changed__address': False,
                    'is_changed__name1': False,
                    'is_changed__name2': False,
                    'is_changed__name3': False,
                    'is_changed__nwpta_ab': False,
                    'is_changed__nwpta_sk': False,
                    'is_changed__request_state': is_changed__request_state,
                    'is_changed_consent':  is_changed_consent
                }
                warnings = nro.change_nr(nrd, change_flags)
                if warnings:
                    MessageServices.add_message(MessageServices.ERROR, 'change_request_in_NRO', warnings)

            ### Update NR Details in NRO (not for reset)
            else:
                try:
                    change_flags = {
                        'is_changed__request': is_changed__request,
                        'is_changed__previous_request': is_changed__previous_request,
                        'is_changed__applicant': is_changed__applicant,
                        'is_changed__address': is_changed__address,
                        'is_changed__name1': is_changed__name1,
                        'is_changed__name2': is_changed__name2,
                        'is_changed__name3': is_changed__name3,
                        'is_changed__nwpta_ab': is_changed__nwpta_ab,
                        'is_changed__nwpta_sk': is_changed__nwpta_sk,
                        'is_changed__request_state': is_changed__request_state,
                        'is_changed_consent': is_changed_consent
                    }

                    # if any data has changed from an NR Details edit, update it in Oracle
                    if any(value is True for value in change_flags.values()):
                        warnings = nro.change_nr(nrd, change_flags)
                        if warnings:
                            MessageServices.add_message(MessageServices.ERROR, 'change_request_in_NRO', warnings)
                        else:
                            ### now it's safe to delete any names that were blanked out
                            for nrd_name in nrd.names:
                                if deleted_names[nrd_name.choice - 1]:
                                    nrd_name.delete_from_db()

                except (NROServicesError, Exception) as err:
                    MessageServices.add_message('error', 'change_request_in_NRO', err)

            # if there were errors, return the set of errors
            warning_and_errors = MessageServices.get_all_messages()
            if warning_and_errors:
                for we in warning_and_errors:
                    if we['type'] == MessageServices.ERROR:
                        return jsonify(errors=warning_and_errors), 400

            ### Finally save the entire graph
            nrd.save_to_db()

            EventRecorder.record(user, Event.PUT, nrd, json_input)


        except ValidationError as ve:
            return jsonify(ve.messages), 400

        except NoResultFound as nrf:
            # not an error we need to track in the log
            return jsonify(message='Request:{} not found'.format(nr)), 404

        except Exception as err:
            current_app.logger.error("Error when replacing NR:{0} Err:{1}".format(nr, err))
            return jsonify(message='NR had an internal error'), 500

        # if we're here, messaging only contains warnings
        warning_and_errors = MessageServices.get_all_messages()
        if warning_and_errors:
            current_app.logger.debug(nrd.json(), warning_and_errors)
            return jsonify(nameRequest=nrd.json(), warnings=warning_and_errors), 206

        current_app.logger.debug(nrd.json())
        return jsonify(nrd.json()), 200


@cors_preflight("GET")
@api.route('/<string:nr>/analysis/<int:choice>/<string:analysis_type>', methods=['GET','OPTIONS'])
class RequestsAnalysis(Resource):
    """Acting like a QUEUE this gets the next NR (just the NR number)
    and assigns it to your auth id

        :param nr (str): NameRequest Number in the format of 'NR 000000000'
        :param choice (int): name choice number (1..3)
        :param args: start: number of hits to start from, default is 0
        :param args: names_per_page: number of names to return per page, default is 50
        :param kwargs: __futures__
        :return: 200 - success; 40X for errors
    """
    START = 0
    ROWS = 50

    # @auth_services.requires_auth
    # noinspection PyUnusedLocal,PyUnusedLocal
    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def get(nr, choice, analysis_type, *args, **kwargs):
        start = request.args.get('start', RequestsAnalysis.START)
        rows = request.args.get('rows',RequestsAnalysis.ROWS)

        if analysis_type not in ANALYTICS_VALID_ANALYSIS:
            return jsonify(message='{analysis_type} is not a valid analysis type for that name choice'
                           .format(analysis_type=analysis_type)), 404

        nrd = RequestDAO.find_by_nr(nr)

        if not nrd:
            return jsonify(message='{nr} not found'.format(nr=nr)), 404

        nrd_name = nrd.names.filter_by(choice=choice).one_or_none()

        if not nrd_name:
            return jsonify(message='Name choice:{choice} not found for {nr}'.format(nr=nr, choice=choice)), 404

        if analysis_type in RestrictedWords.RESTRICTED_WORDS:
            results, msg, code = RestrictedWords.get_restricted_words_conditions(nrd_name.name)

        else:
            results, msg, code = SolrQueries.get_results(analysis_type, nrd_name.name, start=start, rows=rows)

        if code:
            return jsonify(message=msg), code
        return jsonify(results), 200

@cors_preflight("GET")
@api.route('/synonymbucket/<string:name>/<string:advanced_search>', methods=['GET','OPTIONS'])
class SynonymBucket(Resource):
    START = 0
    ROWS = 1000

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def get(name, advanced_search, *args, **kwargs):
        start = request.args.get('start', SynonymBucket.START)
        rows = request.args.get('rows', SynonymBucket.ROWS)
        exact_phrase = '' if advanced_search == '*' else advanced_search
        results, msg, code = SolrQueries.get_conflict_results(name.upper(), bucket='synonym', exact_phrase=exact_phrase, start=start, rows=rows)
        if code:
            return jsonify(message=msg), code
        return jsonify(results), 200

@cors_preflight("GET")
@api.route('/cobrsphonetics/<string:name>/<string:advanced_search>', methods=['GET','OPTIONS'])
class CobrsPhoneticBucket(Resource):
    START = 0
    ROWS = 500

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def get(name, advanced_search, *args, **kwargs):
        start = request.args.get('start', CobrsPhoneticBucket.START)
        rows = request.args.get('rows', CobrsPhoneticBucket.ROWS)
        name = '' if name == '*' else name
        exact_phrase = '' if advanced_search == '*' else advanced_search
        results, msg, code = SolrQueries.get_conflict_results(name.upper(), bucket='cobrs_phonetic', exact_phrase=exact_phrase, start=start, rows=rows)
        if code:
            return jsonify(message=msg), code
        return jsonify(results), 200

@cors_preflight("GET")
@api.route('/phonetics/<string:name>/<string:advanced_search>', methods=['GET','OPTIONS'])
class PhoneticBucket(Resource):
    START = 0
    ROWS = 100000

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def get(name, advanced_search,*args, **kwargs):
        start = request.args.get('start', PhoneticBucket.START)
        rows = request.args.get('rows', PhoneticBucket.ROWS)
        name = '' if name == '*' else name
        exact_phrase = '' if advanced_search == '*' else advanced_search
        results, msg, code = SolrQueries.get_conflict_results(name.upper(), bucket='phonetic', exact_phrase=exact_phrase, start=start, rows=rows)
        if code:
            return jsonify(message=msg), code
        return jsonify(results), 200

@cors_preflight("GET, PUT, PATCH")
@api.route('/<string:nr>/names/<int:choice>', methods=['GET', "PUT", "PATCH",'OPTIONS'])
class NRNames(Resource):

    @staticmethod
    def common(nr, choice):
        """:returns: object, code, msg
        """
        if not RequestDAO.validNRFormat(nr):
            return None, None, jsonify({'message': 'NR is not a valid format \'NR 9999999\''}), 400

        nrd = RequestDAO.find_by_nr(nr)
        if not nrd:
            return None, None, jsonify({"message": "{nr} not found".format(nr=nr)}), 404

        name = nrd.names.filter_by(choice=choice).one_or_none()
        if not name:
            return None, None, jsonify({"message": "Choice {choice} for {nr} not found".format(choice=choice, nr=nr)}), 404

        return nrd, name, None, 200

    # noinspection PyUnusedLocal,PyUnusedLocal
    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def get(nr, choice, *args, **kwargs):

        nrd, nrd_name, msg, code = NRNames.common(nr, choice)
        if not nrd:
            return msg, code

        return names_schema.dumps(nrd_name).data, 200

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def put(nr, choice, *args, **kwargs):
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400

        errors = names_schema.validate(json_data, partial=False)
        if errors:
            return jsonify(errors), 400

        errors = name_comment_schema.validate(json_data['comment'], partial=True)
        if errors:
            return jsonify(errors), 400

        nrd, nrd_name, msg, code = NRNames.common(nr, choice)
        if not nrd:
            return msg, code

        user = User.find_by_jwtToken(g.jwt_oidc_token_info)
        if not check_ownership(nrd, user):
            return jsonify({"message": "You must be the active editor and it must be INPROGRESS"}), 403

        names_schema.load(json_data, instance=nrd_name, partial=False)

        if json_data['comment'] is not None and json_data['comment']['comment'] is not None:
            comment_instance = Comment()
            name_comment_schema.load(json_data['comment'], instance=comment_instance, partial=True)
            comment_instance.examinerId = user.id
            comment_instance.nrId = nrd_name.nrId

            comment_instance.save_to_db()
            nrd_name.commentId = comment_instance.id
        else:
            nrd_name.comment = None

        #add clean name for conflict matching in name request
        if(nrd_name.state == 'APPROVED'):
            try:
                service = ProtectedNameAnalysisService()
                np_svc = service.name_processing_service
                np_svc.set_name(nrd_name.name)
                cleaned_name = np_svc.processed_name.upper()
                nrd_name.clean_name = cleaned_name
            except Exception as error:
                current_app.logger.error("Error on clean name processing. CleanedName[0], Error:{1}".format(cleaned_name, error))
                return jsonify({"message": "Error on clean name."}), 500
        else:
            cleaned_name = None
            nrd_name.clean_name = cleaned_name

        # Updating existing key's value
        try:
            json_data.update(clean_name=cleaned_name)
        except Exception as error:
            current_app.logger.error("Error on json update for clean_name. CleanedName[0], Error:{1}".format(cleaned_name, error))
            return jsonify({"message": "Error on clean name."}), 500

        try:
            nrd_name.save_to_db()
        except Exception as error:
            current_app.logger.error("Error on nrd_name update, Error:{0}".format(error))
            return jsonify({"message": "Error on name update, saving to the db."}), 500

        EventRecorder.record(user, Event.PUT, nrd, json_data)

        return jsonify({"message": "Replace {nr} choice:{choice} with {json}".format(nr=nr, choice=choice, json=json_data)}), 200

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def patch(nr, choice, *args, **kwargs):

        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400

        errors = names_schema.validate(json_data, partial=True)
        if errors:
            return jsonify(errors), 400

        nrd, nrd_name, msg, code = NRNames.common(nr, choice)
        if not nrd:
            return msg, code

        user = User.find_by_jwtToken(g.jwt_oidc_token_info)
        if not check_ownership(nrd, user):
            return jsonify({"message": "You must be the active editor and it must be INPROGRESS"}), 403

        names_schema.load(json_data, instance=nrd_name, partial=True)
        nrd_name.save_to_db()

        EventRecorder.record(user, Event.PATCH, nrd, json_data)

        return jsonify({"message": "Patched {nr} - {json}".format(nr=nr, json=json_data)}), 200


# TODO: This should be in it's own file, not in the requests
@cors_preflight("GET")
@api.route('/decisionreasons', methods=['GET', 'OPTIONS'])
class DecisionReasons(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    def get():
        response = []
        for reason in DecisionReason.query.order_by(DecisionReason.name).all():
            response.append(reason.json())
        return jsonify(response), 200

@cors_preflight("GET")
@api.route('/<string:nr>/syncnr', methods=['GET', 'OPTIONS'])
class SyncNR(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.has_one_of_roles([User.APPROVER, User.EDITOR])
    def get(nr):
        try:
            user = get_or_create_user_by_jwt(g.jwt_oidc_token_info)
            nrd = RequestDAO.find_by_nr(nr)
        except NoResultFound as nrf:
            # not an error we need to track in the log
            return jsonify({"message": "Request:{} not found".format(nr)}), 404
        except Exception as err:
            current_app.logger.error("Error when patching NR:{0} Err:{1}".format(nr, err))
            return jsonify({"message": "NR had an internal error"}), 404

        if not nrd:
            return jsonify({"message": "Request:{} not found".format(nr)}), 404

        warnings = nro.move_control_of_request_from_nro(nrd, user, True)

        if warnings:
            resp = RequestDAO.query.filter_by(nrNum=nr.upper()).first_or_404().json()
            resp['warnings'] = warnings
            return jsonify(resp), 206

        return jsonify(RequestDAO.query.filter_by(nrNum=nr.upper()).first_or_404().json())


@cors_preflight("GET")
@api.route('/stats', methods=['GET', 'OPTIONS'])
class Stats(Resource):

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def get(*args, **kwargs):

        # default is last 1 hour, but can be sent as parameter
        timespan = int(request.args.get('timespan', 1))

        # validate row & start params
        start = request.args.get('currentpage', 1)
        rows = request.args.get('perpage', 50)

        try:
            rows = int(rows)
            start = (int(start)-1) * rows
        except Exception as err:
            current_app.logger.info('start or rows not an int, err: {}'.format(err))
            return jsonify({'message': 'paging parameters were not integers'}), 406

        q = RequestDAO.query \
            .filter(RequestDAO.stateCd.in_(State.COMPLETED_STATE))\
            .filter(RequestDAO.lastUpdate >= text('(now() at time zone \'utc\') - INTERVAL \'{delay} HOURS\''.format(delay=timespan))) \
            .order_by(RequestDAO.lastUpdate.desc())

        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = db.session.execute(count_q).scalar()

        q = q.offset(start)
        q = q.limit(rows)

        # current_app.logger.debug(str(q.statement.compile(
        #     dialect=postgresql.dialect(),
        #     compile_kwargs={"literal_binds": True}))
        # )

        requests = q.all()
        rep = {
            'numRecords': count,
            'nameRequests': request_search_schemas.dump(requests)[0]
        }
        return jsonify(rep)

@cors_preflight("POST")
@api.route('/<string:nr>/comments', methods=["POST",'OPTIONS'])
class NRComment(Resource):

    @staticmethod
    def common(nr):
        """:returns: object, code, msg
        """
        if not RequestDAO.validNRFormat(nr):
            return None, jsonify({'message': 'NR is not a valid format \'NR 9999999\''}), 400

        nrd = RequestDAO.find_by_nr(nr)
        if not nrd:
            return None, jsonify({"message": "{nr} not found".format(nr=nr)}), 404


        return nrd, None, 200

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.has_one_of_roles([User.APPROVER, User.EDITOR])
    def post(nr,*args, **kwargs):
        json_data = request.get_json()

        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400

        nrd, msg, code = NRComment.common(nr)

        if not nrd:
            return msg, code

        errors = name_comment_schema.validate(json_data, partial=False)
        if errors:
            return jsonify(errors), 400

        # find NR
        try:
            nrd = RequestDAO.find_by_nr(nr)
            if not nrd:
                return jsonify({"message": "Request:{} not found".format(nr)}), 404

        except NoResultFound as nrf:
            # not an error we need to track in the log
            return jsonify({"message": "Request:{} not found".format(nr)}), 404
        except Exception as err:
            current_app.logger.error("Error when trying to post a comment NR:{0} Err:{1}".format(nr, err))
            return jsonify({"message": "NR had an internal error"}), 404

        nr_id = nrd.id
        user = User.find_by_jwtToken(g.jwt_oidc_token_info)
        if user is None:
            return jsonify({'message': 'No User'}), 404

        if json_data.get('comment') is None:
            return jsonify({"message": "No comment supplied"}),400

        comment_instance = Comment()
        comment_instance.examinerId = user.id
        comment_instance.nrId = nr_id
        comment_instance.comment = convert_to_ascii(json_data.get('comment'))

        comment_instance.save_to_db()

        EventRecorder.record(user, Event.POST, nrd, json_data)
        return jsonify(comment_instance.as_dict()), 200
