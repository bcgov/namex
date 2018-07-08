"""Requests used to support the namex API

TODO: Fill in a larger description once the API is defined for V1
"""
from flask import request, jsonify, g, current_app
from flask_restplus import Namespace, Resource, fields, cors
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, desc, asc, text, exc
from sqlalchemy.inspection import inspect
import types
import re

from marshmallow import ValidationError
from app import oidc
from app.auth_services import required_scope, AuthError
from app.models import db, User, State, Name, NameSchema
from app.models import Request as RequestDAO, RequestsSchema
from app.models import DecisionReason

from app.utils.util import cors_preflight
from .solr import SolrQueries

# Register a local namespace for the requests
api = Namespace('nameRequests', description='Name Request System - Core API for reviewing a Name Request')


# Marshmallow schemas
request_schema = RequestsSchema(many=False)
request_schemas = RequestsSchema(many=True)
names_schema = NameSchema(many=False)
names_schemas = NameSchema(many=True)


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
    @oidc.accept_token(require_token=True)
    def get(*args, **kwargs):
        try:
            return jsonify(g.oidc_token_info), 200
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
    @oidc.accept_token(require_token=True)
    def get():
        if not (required_scope(User.EDITOR) or required_scope(User.APPROVER)):
            return {"message": "Error: You do not have access to the Name Request queue."}, 403

        try:
            user = User.find_by_jwtToken(g.oidc_token_info)
            if not user:
                user = User.create_from_jwtToken(g.oidc_token_info)

            nr = RequestDAO.get_queued_oldest(user)

        except SQLAlchemyError as err:
            # TODO should put some span trace on the error message
            return jsonify({'message': 'An error occurred getting the next Name Request.'}), 500
        except AttributeError as err:
            current_app.logger.error(err)
            return jsonify({'message': 'There are no Name Requests to work on.'}), 404

        return '{{"nameRequest": "{0}" }}'.format(nr), 200


@cors_preflight("GET, POST")
@api.route('/', methods=['GET', 'POST', 'OPTIONS'])
class Requests(Resource):
    a_request = api.model('Request', {'submitter': fields.String('The submitter name'),
                                      'corpType': fields.String('The corporation type'),
                                      'reqType': fields.String('The name request type')
                                      })

    START=0
    ROWS=50

    search_request_schemas = RequestsSchema(many=True
        ,exclude=['id'
            ,'applicants'
            ,'partnerNS'
            ,'requestId'
            ,'previousRequestId'])

    @staticmethod
    @cors.crossdomain(origin='*')
    @oidc.accept_token(require_token=True)
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
                sort_by = sort_by + '{columns} {direction}'.format(columns=cols[k], direction=vl)
                order_list = order_list + '{attribute} {direction}'.format(attribute=k, direction=vl)

        # Assemble the query
        q = RequestDAO.query.filter()
        if queue: q = q.filter(RequestDAO.stateCd.in_(queue))
        q = q.order_by(text(sort_by))

        # get a count of the full set size, this ignore the offset & limit settings
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = db.session.execute(count_q).scalar()

        # Add the paging
        q = q.offset(start * rows)
        q = q.limit(rows)

        # create the response
        rep = {'response':{'start':start,
                           'rows': rows,
                           'numFound': count,
                           'queue': queue,
                           'order': order_list
                           },
               'nameRequests': Requests.search_request_schemas.dump(q.all()).data
               }

        return jsonify(rep), 200

    @api.errorhandler(AuthError)
    def handle_auth_error(ex):
        # response = jsonify(ex.error)
        # response.status_code = ex.status_code
        # return response, 401
        return {}, 401

    # noinspection PyUnusedLocal,PyUnusedLocal
    @api.expect(a_request)
    @cors.crossdomain(origin='*')
    @oidc.accept_token(require_token=True)
    def post(self, *args, **kwargs):

        current_app.logger.info('Someone is trying to post a new request')
        return jsonify({'message': 'Not Implemented'}), 501


# noinspection PyUnresolvedReferences
@cors_preflight("GET, PATCH, PUT, DELETE")
@api.route('/<string:nr>', methods=['GET', 'PATCH', 'PUT', 'DELETE', 'OPTIONS'])
class Request(Resource):

    @staticmethod
    @cors.crossdomain(origin='*')
    @oidc.accept_token(require_token=True)
    def get(nr):
        # return jsonify(request_schema.dump(RequestDAO.query.filter_by(nr=nr.upper()).first_or_404()))
        return jsonify(RequestDAO.query.filter_by(nrNum =nr.upper()).first_or_404().json())

    @staticmethod
    # @cors.crossdomain(origin='*')
    @oidc.accept_token(require_token=True)
    def delete(nr):
        nrd = RequestDAO.find_by_nr(nr)
        # even if not found we still return a 204, which is expected spec behaviour
        if nrd:
            nrd.stateCd = State.CANCELLED
            nrd.save_to_db()

        return '', 204

    @staticmethod
    @cors.crossdomain(origin='*')
    @oidc.accept_token(require_token=True)
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
        if not (required_scope(User.EDITOR) or required_scope(User.APPROVER)):
            raise AuthError({
                "code": "Unauthorized",
                "description": "You don't have access to this resource."
            }, 403)

        if (state in (State.APPROVED,
                     State.REJECTED,
                     State.CONDITIONAL))\
                and not required_scope(User.APPROVER):
            return jsonify({"message": "Only Names Examiners can set state: {}".format(state)}), 428

        try:
            nrd = RequestDAO.find_by_nr(nr)
            if not nrd:
                return jsonify({"message": "NR not found"}), 404

            user = User.find_by_jwtToken(g.oidc_token_info)
            if not user:
                user = User.create_from_jwtToken(g.oidc_token_info)

            #NR is in a final state, but maybe the user wants to pull it back for corrections
            if nrd.stateCd in State.COMPLETED_STATE:
                if not required_scope(User.APPROVER):
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
    @oidc.accept_token(require_token=True)
    def put(nr, *args, **kwargs):

         # Stubbed out for the UX folks to test and send anything from the UI.
        pass
        return jsonify({'message': '{} successfully replaced'.format(nr)}), 202

        # do the cheap check first before the more expensive ones
        json_input = request.get_json()
        if not json_input:
            return jsonify({'message': 'No input data provided'}), 400

        res = RequestsSchema().load(json_input, partial=True)
        in_nr = res.data

        nrd = RequestDAO.find_by_nr(nr)
        if not nrd:
            return jsonify({'message': 'Request: {} does not exit'.format(nr)}), 404

        user = User.find_by_jwtToken(g.oidc_token_info)



        if not user or nrd.stateCd != State.INPROGRESS or nrd.userId != user.id:
            return jsonify({"message": "The Request must be INPROGRESS and assigned to you before you can change it."}), 401


        nrd.stateCd = in_nr['state']
        nrd.adminComment = in_nr['adminComment']
        nrd.applicant = in_nr['applicant']
        nrd.phoneNumber = in_nr['phoneNumber']
        nrd.contact = in_nr['contact']
        nrd.abPartner = in_nr['abPartner']
        nrd.skPartner = in_nr['skPartner']
        nrd.consentFlag = in_nr['consentFlag']
        nrd.examComment = in_nr['examComment']
        nrd.expiryDate = in_nr['expiryDate']
        nrd.requestTypeCd = in_nr['requestTypeCd']
        nrd.priorityCd = in_nr['priorityCd']
        nrd.tilmaInd = in_nr['tilmaInd']
        nrd.tilmaTransactionId = in_nr['tilmaTransactionId']
        nrd.xproJurisdiction = in_nr['xproJurisdiction']
        nrd.additionalInfo = in_nr['additionalInfo']
        nrd.natureBusinessInfo = in_nr['natureBusinessInfo']
        nrd.userNote = in_nr['userNote']
        nrd.nuansNum = in_nr['nuansNum']
        nrd.nuansExpirationDate = in_nr['nuansExpirationDate']
        nrd.assumedNuansNum = in_nr['assumedNuansNum']
        nrd.assumedNuansName = in_nr['assumedNuansName']
        nrd.assumedNuansExpirationDate = in_nr['assumedNuansExpirationDate']
        nrd.lastNuansUpdateRole = in_nr['lastNuansUpdateRole']

        #update the name info
        for name in nrd.names.all():
            choice = name.choice
            for nm in res.data['names']:
                if nm.choice == choice:
                    name.name = nm.name
                    name.state= nm.state
                    name.conflict1 = nm.conflict1
                    name.conflict2 = nm.conflict2
                    name.conflict3 = nm.conflict3
                    name.conflict1_num = nm.conflict1_num
                    name.conflict2_num = nm.conflict2_num
                    name.conflict3_num = nm.conflict3_num
                    name.decision_text = nm.decision_text

        nrd.save_to_db()

        current_app.logger.info("nrd: {}".format(nrd.state))

        return jsonify({'message': '{} successfully replaced'.format(nr)}), 202


@cors_preflight("GET")
@api.route('/<string:nr>/analysis/<int:choice>/<string:types>', methods=['GET','OPTIONS'])
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
    @oidc.accept_token(require_token=True)
    def get(nr, choice, types, *args, **kwargs):
        start = request.args.get('start', RequestsAnalysis.START)
        rows = request.args.get('rows',RequestsAnalysis.ROWS)

        if types not in SolrQueries.VALID_QUERIES:
            return jsonify({"message": "{type} is not a valid analysis type for that name choice".format(type=type)}), 404

        nrd = RequestDAO.find_by_nr(nr)

        if not nrd:
            return jsonify({"message": "{nr} not found".format(nr=nr)}), 404

        nrd_name = nrd.names.filter_by(choice=choice).one_or_none()

        if not nrd_name:
            return jsonify({"message": "Name choice:{choice} not found for {nr}".format(nr=nr, choice=choice)}), 404

        if types != 'restricted_words':
            try:
                solr = SolrQueries.get_results(types, nrd_name.name, start=start, rows=rows)
            except Exception as err:
                current_app.logger.error('SOLR - name:{}, types:{}, err:{}'.format(nrd_name.name, types, err))
                return jsonify({"message": "Internal server error"}) , 500

            conflicts = {"response": {"numFound": solr['response']['numFound'],
                                      "start": solr['response']['start'],
                                      "rows": solr['responseHeader']['params']['rows'],
                                      "maxScore": solr['response']['maxScore'],
                                      "name": solr['responseHeader']['params']['q'][5:]
                                      },
                         'names':solr['response']['docs'],
                         'highlighting':solr['highlighting']}

            return jsonify(conflicts), 200

        else:
            return RequestsAnalysis.get_restricted_words_conditions(nrd_name.name)

    @staticmethod
    def get_restricted_words_conditions(corp_name):
        """ 1. put all possible restricted words/phrases in a list
                          - used later to compare against sql fn
                       parse corp_name from snake_case into sql format
        """
        word_list = corp_name.split()

        # this adds in all possible phrases that are two or more words to word_list
        phrases = []
        phrase = ''
        for indx, word in enumerate(word_list):
            for possible_phrase in word_list[indx:]:
                if phrase != '':
                    phrase += possible_phrase
                    phrases.append(phrase)
                else:
                    phrase += possible_phrase
                if indx < len(word_list):
                    phrase += ' '
            phrase = ''

        word_list = word_list + phrases
        """------------------------------------------------------"""

        """ 2. get words/phrases in corp_name that are restricted
                - query for list of all restricted words
                    - compare these words to word_list
        """

        get_all_restricted_words_sql = text("select * from restricted_word;")
        try:
            restricted_words_obj = db.engine.execute(get_all_restricted_words_sql)

        except exc.SQLAlchemyError:
            print(exc.SQLAlchemyError)
            return jsonify({"message": "An error occurred accessing the restricted words."}), 500
        except AttributeError:
            return jsonify({"message": "Could not find any restricted words."}), 404
        restricted_words_dict = []
        for row in restricted_words_obj:
            for word in word_list:
                if row[1] == word:
                    restricted_words_dict.append({'id':row[0],'phrase':row[1]})
        """-----------------------------------------------------------------"""

        """ 3. get condition info based on word_id for each restricted word """

        restricted_words_conditions = []
        for word in restricted_words_dict:
            get_cnd_id_sql = text("select cnd_id from restricted_word_condition where word_id = {}".format(word['id']))
            try:
                cnd_id_obj = db.engine.execute(get_cnd_id_sql)
                cnd_ids = cnd_id_obj.fetchall()

                cnd_obj_list = []
                for id in cnd_ids:
                    cnd_id = id[0]
                    get_cnd_sql = text("select * from restricted_condition where cnd_id = {}".format(cnd_id))
                    cnd_obj_list.append(db.engine.execute(get_cnd_sql))

                cnd_info = []
                for obj in cnd_obj_list:
                    obj_tuple = obj.fetchall()[0]
                    cnd_text = obj_tuple[1]
                    cnd_allow_use = obj_tuple[2]
                    cnd_consent_req = obj_tuple[3]
                    cnd_consent_body = obj_tuple[4]
                    cnd_instr = obj_tuple[5]

                    cnd_info.append({'id': cnd_id,
                                    'text': cnd_text,
                                    'allow_use': cnd_allow_use,
                                    'consent_required': cnd_consent_req,
                                    'consenting_body': cnd_consent_body,
                                    'instructions': cnd_instr})
                restricted_words_conditions.append({'word_info': word, 'cnd_info': cnd_info})
            except exc.SQLAlchemyError:
                print(exc.SQLAlchemyError)
                return jsonify(
                    {"message": "An error occurred accessing the condition for {}.".format(word['id'])}), 500
            except AttributeError:
                return jsonify({"message": "Could not find any condition info for {}.".format(word['id'])}), 404
            except:
                # print('error')
                cnd_info = 'Not Available'
                restricted_words_conditions.append({'word_info': word, 'cnd_info': cnd_info})
        """------------------------------------------------------------------------------------"""

        return jsonify({"restricted_words_conditions": restricted_words_conditions}), 200


@cors_preflight("GET, PUT, PATCH")
@api.route('/<string:nr>/names/<int:choice>', methods=['GET', "PUT", "PATCH",'OPTIONS'])
class NRNames(Resource):

    @staticmethod
    def common(nr, choice):
        """:returns: object, code, msg
        """
        if not validNRFormat(nr):
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
    @oidc.accept_token(require_token=True)
    def get(nr, choice, *args, **kwargs):

        nrd, nrd_name, msg, code = NRNames.common(nr, choice)
        if not nrd:
            return msg, code

        return names_schema.dumps(nrd_name).data, 200

    @staticmethod
    @cors.crossdomain(origin='*')
    @oidc.accept_token(require_token=True)
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

        user = User.find_by_jwtToken(g.oidc_token_info)
        if not check_ownership(nrd, user):
            return jsonify({"message": "You must be the active editor and it must be INPROGRESS"}), 403

        names_schema.load(json_data, instance=nrd_name, partial=False)
        nrd_name.save_to_db()

        return jsonify({"message": "Replace {nr} choice:{choice} with {json}".format(nr=nr, choice=choice, json=json_data)}), 200

    @staticmethod
    @cors.crossdomain(origin='*')
    @oidc.accept_token(require_token=True)
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

        user = User.find_by_jwtToken(g.oidc_token_info)
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
    #@oidc.accept_token(require_token=True)
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


def validNRFormat(nr):
    '''NR should be of the format "NR 1234567"
    '''
    if len(nr) != 10 or nr[:2] != 'NR' or nr[2:3] != ' ':
        return False

    try:
        num = int(nr[3:])
    except:
        return False

    return True
