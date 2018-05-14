"""Requests used to support the namex API

TODO: Fill in a larger description once the API is defined for V1
"""
from flask import request, jsonify, g # _request_ctx_stack
from flask_restplus import Resource, fields, cors
from marshmallow import ValidationError
from app import api, auth_services, oidc
from app.models import User
from sqlalchemy.orm.exc import NoResultFound
from app.utils.util import cors_preflight
from datetime import datetime
import logging

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


@cors_preflight("GET")
@api.route('/requests/queues/@me/oldest', methods=['GET','OPTIONS'])
class RequestsQueue(Resource):
    """Acting like a QUEUE this gets the next NR (just the NR number)
    and assigns it to your auth id
    """

    # @auth_services.requires_auth
    # noinspection PyUnusedLocal,PyUnusedLocal
    @staticmethod
    @cors.crossdomain(origin='*')
    @oidc.accept_token(require_token=True)
    def get():
        try:
            user = User.find_by_jwtToken(g.oidc_token_info)
            if not user:
                user = User.create_from_jwtToken(g.oidc_token_info)
            nr = RequestDAO.get_queued_oldest(user)
        except exc.SQLAlchemyError as err:
            #TODO should put some span trace on the error message
            logging.log(logging.ERROR, 'error in getting next NR. {}'.format(err))
            return {"message": "An error occurred getting the next Name Request."}, 500
        except AttributeError as err:
            return {"message": "There are no Name Requests to work on."}, 404

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
            nrd.state = RequestDAO.STATE_CANCELLED
            nrd.save_to_db()

        return '', 204

    @staticmethod
    @cors.crossdomain(origin='*')
    @oidc.accept_token(require_token=True)
    def patch(nr, *args, **kwargs):

        # do the cheap check first before the more expensive ones
        json_input = request.get_json()
        if not json_input:
            return jsonify({'message': 'No input data provided'}), 400

        # Currently only state changes are supported by patching
        # all these checks to get removed to marshmallow
        state = json_input.get('state', None)
        if not state:
            return jsonify({"message": "state not set"}), 406

        if state not in RequestDAO.VALID_STATES:
            return jsonify({"message": "not a valid state"}), 406

        try:
            nrd = RequestDAO.find_by_nr(nr)
            if not nrd:
                return jsonify({"message": "NR not found"}), 404

            user = User.find_by_jwtToken(g.oidc_token_info)
            if not user:
                user = User.create_from_jwtToken(g.oidc_token_info)

            if state in RequestDAO.RELEASE_STATES:
                if nrd.userId != user.id or nrd.state != RequestDAO.STATE_INPROGRESS:
                    return jsonify({"message": "The Request must be INPROGRESS and assigned to you before you can change it."}), 401

            existing_nr = RequestDAO.get_inprogress(user)
            if existing_nr:
                existing_nr.state = RequestDAO.STATE_HOLD
                existing_nr.save_to_db()

            nrd.state = state
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



        if not user or nrd.state != RequestDAO.STATE_INPROGRESS or nrd.userId != user.id:
            return jsonify({"message": "The Request must be INPROGRESS and assigned to you before you can change it."}), 401


        nrd.state = in_nr['state']
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
