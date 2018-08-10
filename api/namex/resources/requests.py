"""Requests used to support the namex API

TODO: Fill in a larger description once the API is defined for V1
"""
from flask import request, jsonify, g, current_app, flash, get_flashed_messages
from flask_restplus import Namespace, Resource, fields, cors
from flask_jwt_oidc import AuthError

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, text, exc
from sqlalchemy.inspection import inspect

from namex import jwt, nro
from namex.models import db, ValidationError
from namex.models import Request as RequestDAO, RequestsSchema, RequestsHeaderSchema
from namex.models import Name, NameSchema, PartnerNameSystemSchema
from namex.models import User, State, Comment
from namex.models import ApplicantSchema
from namex.models import DecisionReason

from namex.nro_services import NROServicesError
from namex.utils.util import cors_preflight
from namex.analytics import SolrQueries, RestrictedWords, VALID_ANALYSIS as ANALYTICS_VALID_ANALYSIS

from datetime import datetime
import json
import urllib

# Register a local namespace for the requests
api = Namespace('nameRequests', description='Name Request System - Core API for reviewing a Name Request')

# Marshmallow schemas
request_schema = RequestsSchema(many=False)
request_schemas = RequestsSchema(many=True)
request_header_schema = RequestsHeaderSchema(many=False)

names_schema = NameSchema(many=False)
names_schemas = NameSchema(many=True)
nwpta_schema = PartnerNameSystemSchema(many=False)

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
    @jwt.requires_auth
    def get():
        """ Gets the oldest nr num, that is in DRAFT status
        It then marks the NR as INPROGRESS, and assigns it to the

        :Authorization: (JWT): valid JWT with the User.APPROVER role

        :return: (str) (dict) (https status): 500, 404, or NR NUM, or NR NUM and a system alert in the dict
        """
        if not jwt.validate_roles([User.APPROVER]):
            return jsonify({"message": "Error: You do not have access to the Name Request queue."}), 403

        try:
            # GET existing or CREATE new user based on the JWT info
            user = User.find_by_jwtToken(g.jwt_oidc_token_info)
            current_app.logger.debug('finding user: {}'.format(g.jwt_oidc_token_info))
            if not user:
                current_app.logger.debug('didnt find user, attempting to create new user from the JWT info')
                user = User.create_from_jwtToken(g.jwt_oidc_token_info)

            # get the next NR assigned to the User
            nr, new_assignment = RequestDAO.get_queued_oldest(user)
            current_app.logger.debug('got the nr:{} and its a new assignment?{}'.format(nr.nrNum, new_assignment))

            flash('{"code": "unable_to_get_request_state",'
                  '"description": "Unable to get the current state of the NRO Request"}'
                  , 'error')
            # if it's a new assignment, then LOGICALLY lock the record in NRO
            if new_assignment:

                # get the last modification timestamp before we alter the record
                # try:
                #     nro_last_ts = nro.get_last_update_timestamp(nr.requestId)
                # except NROServicesError as err:
                #     nro_last_ts = None
                #     flash(err.error, 'error')

                current_app.logger.debug('set state to h')
                try:
                    nro.set_request_status_to_h(nr.nrNum, user.username)
                except NROServicesError as err:
                    flash(err.error, 'error')

                current_app.logger.debug('get state')
                try:
                    nro_req_state = nro.get_current_request_state(nr.nrNum)
                except NROServicesError as err:
                    nro_req_state = None
                    flash(err.error, 'error')
                if 'H' is not nro_req_state:
                    flash('{"code": "unable_to_get_nro_request_state",'
                          '"description": "Unable to get the current state of the NRO Request"}'
                          , 'error')
                    current_app.logger.debug('nro state not set to H, nro-package call must have silently failed - ugh')

                nro_last_ts=None
                current_app.logger.debug('update records')
                if True or 'nro_last_ts' in locals() and nro_last_ts != nr.nroLastUpdate:
                    current_app.logger.debug('nro updated since namex was last updated')
                    try:
                        # mark the NR as being updated
                        nr.stateCd = State.NRO_UPDATING
                        nr.save_to_db()
                        data = {
                            'nameRequest': nr.nrNum
                        }
                        url = current_app.config.get('NRO_EXTRACTOR_URI')

                        nro_req = urllib.request.Request(url,
                                                         data=json.dumps(data).encode('utf8'),
                                                         headers={'content-type': 'application/json'})
                        nro_req.get_method = lambda: 'PUT'
                        nro_response = urllib.request.urlopen(nro_req).read()
                        current_app.logger.debug('response from extractor: {},{}'.format(nro_response, nro_response.state_code))

                    except Exception as err:
                        current_app.logger.error(err.with_traceback(None))
                    finally:
                        # set the NR back to INPROGRESS
                        nr.stateCd = State.INPROGRESS
                        nr.save_to_db()

        except SQLAlchemyError as err:
            # TODO should put some span trace on the error message
            current_app.logger.error(err.with_traceback(None))
            return jsonify({'message': 'An error occurred getting the next Name Request.'}), 500
        except AttributeError as err:
            current_app.logger.error(err)
            return jsonify({'message': 'There are no Name Requests to work on.'}), 404

        return jsonify(nameRequest='{}'.format(nr.nrNum), flash=get_flashed_messages(with_categories=True)), 200


@cors_preflight('GET, POST')
@api.route('', methods=['GET', 'POST', 'OPTIONS'])
class Requests(Resource):
    a_request = api.model('Request', {'submitter': fields.String('The submitter name'),
                                      'corpType': fields.String('The corporation type'),
                                      'reqType': fields.String('The name request type')
                                      })

    START=0
    ROWS=10

    search_request_schemas = RequestsSchema(many=True
        ,exclude=['id'
            ,'applicants'
            ,'partnerNS'
            ,'requestId'
            ,'previousRequestId'])

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
        # priorityCd = request.args.get('priorityCd', None)
        furnished = request.args.get('furnished', None)
        unfurnished = request.args.get('unfurnished', None)

        q = RequestDAO.query.filter()
        if queue: q = q.filter(RequestDAO.stateCd.in_(queue))

        if nrNum:
            nrNum = nrNum.replace('NR', '').strip()
            nrNum = '%'+nrNum+'%'
            q = q.filter(RequestDAO.nrNum.like(nrNum))
        if activeUser:
            q = q.join(RequestDAO.activeUser).filter(User.username.like('%'+activeUser+'%'))

        #TODO: fix count on search by compName -- returns count of all names that match -- want it to be all NRs (nrs can have multiple names that match)
        # ---- right now count is adjusted on the frontend in method 'populateTable'
        if compName:
            q = q.join(RequestDAO.names).filter(Name.name.like('%' + compName + '%'))

        if furnished == 'false':
            q = q.filter(RequestDAO.furnished != 'Y')

        if unfurnished == 'false':
            q = q.filter(RequestDAO.furnished != 'N')

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
               'nameRequests': Requests.search_request_schemas.dump(q.all()).data
               }

        ## counts for updatedToday and priorities
        data = rep['nameRequests']
        for row in data:
            try:
                if row['priorityCd'] == 'Y':
                    rep['response']['numPriorities'] += 1
            except KeyError or AttributeError:
                pass

        today = str(datetime.datetime.now)[0:10]
        for row in data:
            try:
                if row['lastUpdate'][0:10] == today:
                    rep['response']['numUpdatedToday'] += 1
            except KeyError or AttributeError:
                pass

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
    @jwt.requires_auth
    def get(nr):
        # return jsonify(request_schema.dump(RequestDAO.query.filter_by(nr=nr.upper()).first_or_404()))
        return jsonify(RequestDAO.query.filter_by(nrNum =nr.upper()).first_or_404().json())

    @staticmethod
    # @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def delete(nr):
        nrd = RequestDAO.find_by_nr(nr)
        # even if not found we still return a 204, which is expected spec behaviour
        if nrd:
            nrd.stateCd = State.CANCELLED
            nrd.save_to_db()

        return '', 204

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def patch(nr, *args, **kwargs):
        """  Patches the NR, only STATE can be changed with some business rules around roles/scopes

        :param nr (str): NameRequest Number in the format of 'NR 000000000'
        :param args:  __futures__
        :param kwargs: __futures__
        :return: 200 - success; 40X for errors

        :HEADER: Valid JWT Bearer Token for a valid REALM
        :JWT Scopes: - USER.APPROVER, USER.EDITOR, USER.VIEWONLY

        APPROVERS: Can change from almost any state, other than CANCELLED, EXPIRED and ( COMPLETED not yet furnished )
        EDITOR: Can't change to a COMPLETED state (ACCEPTED, REJECTED, CONDITION)
        VIEWONLY: Can't change anything, so that are bounced
        """

        # do the cheap check first before the more expensive ones
        #check states
        json_input = request.get_json()
        if not json_input:
            return jsonify({'message': 'No input data provided'}), 400

        # Currently only state changes are supported by patching
        # all these checks to get removed to marshmallow
        state = json_input.get('state', None)
        if not state:
            return jsonify({"message": "state not set"}), 406

        if state not in State.VALID_STATES:
            return jsonify({"message": "not a valid state"}), 406

        #check user scopes
        if not jwt.validate_roles([User.APPROVER]):
            raise AuthError({
                "code": "Unauthorized",
                "description": "You don't have access to this resource."
            }, 403)

        if (state in (State.APPROVED,
                     State.REJECTED,
                     State.CONDITIONAL))\
                and not jwt.validate_roles([User.APPROVER]):
            return jsonify({"message": "Only Names Examiners can set state: {}".format(state)}), 428

        try:
            nrd = RequestDAO.find_by_nr(nr)
            if not nrd:
                return jsonify({"message": "NR not found"}), 404

            user = User.find_by_jwtToken(g.jwt_oidc_token_info)
            if not user:
                user = User.create_from_jwtToken(g.jwt_oidc_token_info)

            #NR is in a final state, but maybe the user wants to pull it back for corrections
            if nrd.stateCd in State.COMPLETED_STATE:
                if not jwt.validate_roles([User.APPROVER]):
                    return jsonify({"message": "Only Names Examiners can alter completed Requests"}), 401

                if nrd.furnished == RequestDAO.REQUEST_FURNISHED:
                    return jsonify({"message": "Request has already been furnished and cannot be altered"}), 409

                if state != State.INPROGRESS:
                    return jsonify({"message": "Completed unfurnished Requests can only be set to an INPROGRESS state"
                                    }), 400

            elif state in State.RELEASE_STATES:
                if nrd.userId != user.id or nrd.stateCd != State.INPROGRESS:
                    return jsonify({"message": "The Request must be INPROGRESS and assigned to you before you can change it."}), 401

            existing_nr = RequestDAO.get_inprogress(user)
            if existing_nr:
                existing_nr.stateCd = State.HOLD
                existing_nr.save_to_db()

            nrd.stateCd = state
            nrd.userId = user.id
            nrd.save_to_db()

        except NoResultFound as nrf:
            # not an error we need to track in the log
            return jsonify({"message": "Request:{} not found".format(nr)}), 404
        except Exception as err:
            current_app.logger.error("Error when patching NR:{0} Err:{1}".format(nr, err))
            return jsonify({"message": "NR had an internal error"}), 404

        return jsonify({'message': 'Request:{} - patched'.format(nr)}), 200

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
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

        #check user scopes
        if not jwt.validate_roles([User.APPROVER]):
            raise AuthError({
                "code": "Unauthorized",
                "description": "You don't have access to this resource."
            }, 403)

        if (state in (State.APPROVED,
                     State.REJECTED,
                     State.CONDITIONAL))\
                and not jwt.validate_roles([User.APPROVER]):
            return jsonify(message='Only Names Examiners can set state: {}'.format(state)), 428

        try:
            nr_d = RequestDAO.find_by_nr(nr)

            # TODO: add in error checking/handling for dates
            if json_input['expirationDate']:
                json_input['expirationDate'] = datetime.strptime(json_input['expirationDate'][5:], '%d %b %Y %H:%M:%S %Z')
            if json_input['submittedDate']:
                json_input['submittedDate'] = datetime.strptime(json_input['submittedDate'][5:], '%d %b %Y %H:%M:%S %Z')

            if not nr_d:
                return jsonify(message='NR not found'), 404

            user = User.find_by_jwtToken(g.jwt_oidc_token_info)
            if not user:
                user = User.create_from_jwtToken(g.jwt_oidc_token_info)

            #NR is in a final state, but maybe the user wants to pull it back for corrections
            if nr_d.stateCd in State.COMPLETED_STATE:
                if not jwt.validate_roles([User.EDITOR]):
                    return jsonify(
                        message='Only Names Examiners can alter completed Requests'
                    ), 401
                if state != State.INPROGRESS:
                    return jsonify(
                        message='Completed unfurnished Requests can only be set to an INPROGRESS state'
                    ), 400
            # elif state in State.RELEASE_STATES:
            #     if nr_d.userId != user.id or nr_d.stateCd != State.INPROGRESS:
            #         return jsonify(
            #               message='The Request must be INPROGRESS and assigned to you before you can change it.'
            #         ), 401
            # elif nr_d.userId != user.id or nr_d.stateCd != State.INPROGRESS:
            #     return jsonify(
            #         message='The Request must be INPROGRESS and assigned to you before you can change it.'
            #     ), 401

            ### REQUEST HEADER ###

            # update request header
            errors = request_header_schema.validate(json_input, partial=True)
            errors.pop('submittedDate', None)
            errors.pop('expirationDate', None)
            errors.pop('previousNr', None)
            if errors:
                return jsonify(errors), 400
            request_header_schema.load(json_input, instance=nr_d, partial=True)
            nr_d.stateCd = state
            nr_d.userId = user.id
            nr_d.additionalInfo = json_input.get('additionalInfo', None)
            nr_d.consentFlag = json_input.get('consentFlag', None)
            nr_d.expirationDate = json_input.get('expirationDate', None)
            nr_d.furnished = json_input.get('furnished', 'N')
            nr_d.natureBusinessInfo = json_input.get('natureBusinessInfo', None)
            nr_d.priorityCd = json_input.get('priorityCd', 'N')
            nr_d.submitCount = json_input.get('submitCount', 1)
            nr_d.submittedDate = json_input.get('submittedDate', None)
            nr_d.xproJurisdiction = json_input.get('xproJurisdiction', None)
            # get previous request ID from previous NR number
            try:
                previousNr = json_input['previousNr']
                nr_d.previousRequestId = RequestDAO.find_by_nr(previousNr).requestId
            except AttributeError:
                nr_d.previousRequestId = None
            except KeyError:
                nr_d.previousRequestId = None

            ### END request header ###

            ### APPLICANTS ###
            # TODO: applicants not updating properly -- needs fix
            applicants_d = nr_d.applicants.one_or_none()
            if applicants_d:
                appl = json_input.get('applicants', None)
                if appl:
                    errm = applicant_schema.validate(appl, partial=True)
                    errm.pop('firstName', None)
                    if errm:
                        return jsonify(errm)

                    applicant_schema.load(appl, instance=applicants_d, partial=True)
                else:
                    applicants_d.delete_from_db()

            ### END applicants ###

            ### NAMES ###
            # TODO: set consumptionDate not working -- breaks changing name values
            for nrd_name in nr_d.names.all():
                for in_name in json_input['names']:

                    if nrd_name.choice == in_name['choice']:
                        errors = names_schema.validate(in_name, partial=False)
                        if errors:
                            return jsonify(errors), 400

                        names_schema.load(in_name, instance=nrd_name, partial=False)

            ### END names ###

            ### COMMENTS ###

            # we only add new comments, we do not change existing comments
            # - we can find new comments in json as those with no ID

            for in_comment in json_input['comments']:
                is_new_comment = False
                try:
                    if in_comment['id'] is None or in_comment['id'] == 0:
                        is_new_comment = True
                except KeyError:
                    is_new_comment = True

                if is_new_comment and in_comment['comment'] is not None:
                    new_comment = Comment()
                    new_comment.comment = in_comment['comment']
                    new_comment.examiner = user
                    new_comment.nrId = nr_d.id

            ### END comments ###

            ### NWPTA ###

            for nrd_nwpta in nr_d.partnerNS.all():
                for in_nwpta in json_input['nwpta']:
                    if nrd_nwpta.partnerJurisdictionTypeCd == in_nwpta['partnerJurisdictionTypeCd']:

                        errors = nwpta_schema.validate(in_nwpta, partial=False)
                        if errors:
                            return jsonify(errors), 400

                        nwpta_schema.load(in_nwpta, instance=nrd_nwpta, partial=False)
            ### END nwpta ###

            ### Finally save the entire graph
            nr_d.save_to_db()

        except ValidationError as ve:
            return jsonify(ve.messages)

        except NoResultFound as nrf:
            # not an error we need to track in the log
            return jsonify(message='Request:{} not found'.format(nr)), 404

        except Exception as err:
            current_app.logger.error("Error when replacing NR:{0} Err:{1}".format(nr, err))
            return jsonify(message='NR had an internal error'), 500

        current_app.logger.debug(nr_d.json())
        return jsonify(nr_d.json()), 200


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
            results, msg, code  = SolrQueries.get_results(analysis_type, nrd_name.name, start=start, rows=rows)

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

        nrd, nrd_name, msg, code = NRNames.common(nr, choice)
        if not nrd:
            return msg, code

        user = User.find_by_jwtToken(g.jwt_oidc_token_info)
        if not check_ownership(nrd, user):
            return jsonify({"message": "You must be the active editor and it must be INPROGRESS"}), 403

        names_schema.load(json_data, instance=nrd_name, partial=False)
        nrd_name.save_to_db()

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

        return jsonify({"message": "Patched {nr} - {json}".format(nr=nr, json=json_data)}), 200


def check_ownership(nrd, user):
    if nrd.stateCd == State.INPROGRESS and nrd.userId == user.id:
        return True
    return False

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


def mergedicts(dict1, dict2):
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(mergedicts(dict1[k], dict2[k])))
            else:
                # If one of the values is not a dict, you can't continue merging it.
                # Value from second dict overrides one in first and we move on.
                yield (k, dict2[k])
                # Alternatively, replace this with exception raiser to alert you of value conflicts
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])
