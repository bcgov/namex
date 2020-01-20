"""Requests used to support the namex API

TODO: Fill in a larger description once the API is defined for V1
"""

from flask import request, make_response, jsonify, g, current_app, get_flashed_messages
from flask_restplus import Namespace, Resource, fields, cors
from flask_jwt_oidc import AuthError

from namex.utils.util import cors_preflight
from namex.utils.logging import setup_logging

#from sqlalchemy.dialects import postgresql
#from sqlalchemy.orm.exc import NoResultFound
#from sqlalchemy import func, text
#from sqlalchemy.inspection import inspect

#from namex import jwt, nro, services

# Import DTOs
from namex.resources.auto_analyse import \
    ConsentingBody, \
    NameAction, \
    DescriptiveWord, \
    Conflict, \
    NameAnalysisIssue, \
    NameAnalysisResponse

from namex.resources.auto_analyse.analysis_strategies import \
    ValidNameResponseStrategy, \
    AddDistinciveWordResponseStrategy, \
    AddDescriptiveWordResponseStrategy, \
    ContainsWordsToAvoidResponseStrategy, \
    DesignationMismatchResponseStrategy, \
    TooManyWordsResponseStrategy, \
    NameRequiresConsentResponseStrategy, \
    ContainsUnclassifiableWordResponseStrategy, \
    CorporateNameConflictResponseStrategy

setup_logging() ## important to do this first

# Register a local namespace for the requests
api = Namespace('nameAnalysis', description='Name Analysis - Core API for analysing a Name')


@api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@cors_preflight("GET")
@api.route('/', strict_slashes=False, methods=['GET', 'OPTIONS'])
class NameAnalysis(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    #@jwt.requires_auth
    #@api.expect()
    def get():
        # any
        name = request.args.get('name')
        # one of ['bc', 'ca', 'intl']
        location = request.args.get('location')
        # what are the entity types?
        entityType = request.args.get('entityType')
        # one of ['new', 'existing', 'continuation'
        requestType = request.args.get('requestType')

        # Go get stuff from the db

        # These are the options:
        # API Returns
        strategy = ValidNameResponseStrategy()
        # Requires addition of distinctive word
        strategy = AddDistinciveWordResponseStrategy()
        # Requires addition of descriptive word
        strategy = AddDescriptiveWordResponseStrategy()
        # Name Contains a Word To Avoid
        strategy = ContainsWordsToAvoidResponseStrategy()
        # Designation Mismatch
        strategy = DesignationMismatchResponseStrategy()
        # Too Many Words
        strategy = TooManyWordsResponseStrategy()
        # Name Requires Consent
        strategy = NameRequiresConsentResponseStrategy()
        # Contains Unclassifiable Word
        strategy = ContainsUnclassifiableWordResponseStrategy()
        # Conflicts with the Corporate Database
        strategy = CorporateNameConflictResponseStrategy()

        payload = strategy.build_response().to_json()

        response = make_response(payload, 200)
        return response
