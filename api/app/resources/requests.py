"""Requests used to support the namex API

TODO: Fill in a larger description once the API is defined for V1
"""
from flask import request, jsonify, g, current_app # _request_ctx_stack
from flask_restplus import Resource, fields, cors
from marshmallow import ValidationError
from app import api, oidc
from app.auth_services import required_scope, AuthError
from app.models import User, State
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError
from app.utils.util import cors_preflight
from datetime import datetime
import logging

from . import temp_hackery
from .solr import SolrQueries

from app.auth_services import AuthError
from app.models import Request as RequestDAO, RequestsSchema

request_schema = RequestsSchema(many=False)
request_schemas = RequestsSchema(many=True)

# noinspection PyUnresolvedReferences
@cors_preflight("GET")
@api.route('/echo', methods=['GET', 'OPTIONS'])
class Echo(Resource):

    @staticmethod
    @cors.crossdomain(origin='*')
    @oidc.accept_token(require_token=True)
    def get (*args, **kwargs):
        try:
            return jsonify(g.oidc_token_info), 200
        except Exception as err:
            return {"error": "{}".format(err)}, 500


#################### QUEUES #######################
@cors_preflight("GET")
@api.route('/requests/queues/@me/oldest', methods=['GET','OPTIONS'])
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
            #TODO should put some span trace on the error message
            return jsonify({'message': 'An error occurred getting the next Name Request.'}), 500
        except AttributeError as err:
            return jsonify({'message': 'There are no Name Requests to work on.'}), 404

        return '{{"nameRequest": "{0}" }}'.format(nr), 200

@cors_preflight("POST")
@api.route('/requests', methods=['POST', 'OPTIONS'])
class Requests(Resource):
    a_request = api.model('Request', {'submitter': fields.String('The submitter name'),
                                      'corpType': fields.String('The corporation type'),
                                      'reqType': fields.String('The name request type')
                                      })

    @api.errorhandler(AuthError)
    def handle_auth_error(ex):
        # response = jsonify(ex.error)
        # response.status_code = ex.status_code
        # return response, 401
        return {}, 401

    # noinspection PyUnusedLocal,PyUnusedLocal
    @api.expect(a_request)
    @cors.crossdomain(origin='*')
    # @auth_services.requires_auth
    @oidc.accept_token(require_token=True)
    def post(self, *args, **kwargs):

        json_input = request.get_json()
        if not json_input:
            return {'message': 'No input data provided'}, 400

        return {}, 501


# noinspection PyUnresolvedReferences
@cors_preflight("GET, PATCH, PUT, DELETE")
@api.route('/requests/<string:nr>', methods=['GET', 'PATCH', 'PUT', 'DELETE', 'OPTIONS'])
class Request(Resource):

    @staticmethod
    @cors.crossdomain(origin='*')
    # @auth_services.requires_auth
    @oidc.accept_token(require_token=True)
    def get(nr):
        # return jsonify(request_schema.dump(RequestDAO.query.filter_by(nr=nr.upper()).first_or_404()))
        return jsonify(RequestDAO.query.filter_by(nrNum =nr.upper()).first_or_404().json())

    @staticmethod
    @cors.crossdomain(origin='*')
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
            logging.log(logging.ERROR, "Error when patching NR:{0} Err:{1}".format(nr, err))
            return jsonify({"message": "NR had an internal error"}), 404

        return jsonify({"message": "Request:{} - patched".format(nr)}), 200

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

        nrd.save_to_db()

        logging.log(logging.INFO,"nrd: {}".format(nrd.state))

        return jsonify({'message': '{} successfully replaced'.format(nr)}), 202


@cors_preflight("GET")
@api.route('/requests/<string:nr>/analysis/<int:choice>/<string:types>', methods=['GET','OPTIONS'])
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

        try:
            solr = SolrQueries.get_results(types, nrd_name.name, start=start, rows=rows)
        except Exception as err:
            logging.log(logging.ERROR, err, type, nrd_name.name)
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