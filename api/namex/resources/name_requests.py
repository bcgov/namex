from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields, cors
from flask_jwt_oidc import AuthError
from namex.utils.util import cors_preflight
import json
from namex import jwt
from flask import current_app
from namex.models import db

from namex.utils.logging import setup_logging
setup_logging() ## important to do this first

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func, text
from sqlalchemy.inspection import inspect

from namex.models import Request as RequestDAO, User, Name, Event, State,Comment
from namex.services import ServicesError, MessageServices, EventRecorder
from namex.services.name_request import get_or_create_user_by_jwt


# Register a local namespace for the NR reserve
api = Namespace('publicNameRequests', description='Public facing Name Requests')
@cors_preflight("POST")
@api.route('/<string:name>/<string:requestAction>/<string:location>/<string: entityType>', methods=['POST','OPTIONS'])
class Name_Requests(Resource):
     a_request = api.model('Request', {'name': fields.String('The name to be reserved'),
                                      'entityType': fields.String('The type of business'),
                                      'requestAction': fields.String('The type of name request'),
                                      'location': fields.String('The location such as province or country')
                                      })

     @staticmethod
     @api.expect(a_request)
     @cors.crossdomain(origin='*')
     @jwt.requires_roles([User.PUBLIC])
     # noinspection PyUnusedLocal,PyUnusedLocal
     def post(name, entityType,requestAction, location, *args, **kwargs):
        if(name == None or requestAction == None or location == None or entityType == None):
             return jsonify({'message': 'Missing input data provided'}), 400

        user = get_or_create_user_by_jwt(g.jwt_oidc_token_info)
        if(user.username != 'name_request_service_account'):
            return jsonify({'message': 'Missing input data provided'}), 400
        #TODO:  There is a list of things to do here: 1) get an NR, set state=RESERVED, set requestType, entitytype, request_action and name, name_state
        #TODO:  jusridiction (if location =BC otherwise we will ge the jurisidction after), update the models/database and then update solr)

