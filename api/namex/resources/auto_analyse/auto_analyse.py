"""Requests used to support the namex API

TODO: Fill in a larger description once the API is defined for V1
"""

from flask import request, make_response, jsonify, g, current_app, get_flashed_messages
from flask_restplus import Namespace, Resource, fields, cors
from flask_jwt_oidc import AuthError

from namex.utils.util import cors_preflight
from namex.utils.logging import setup_logging

from namex.resources.auto_analyse.analysis_strategies import \
    ValidNameResponseStrategy, \
    AddDistinctiveWordResponseStrategy, \
    AddDescriptiveWordResponseStrategy, \
    ContainsWordsToAvoidResponseStrategy, \
    DesignationMismatchResponseStrategy, \
    TooManyWordsResponseStrategy, \
    NameRequiresConsentResponseStrategy, \
    ContainsUnclassifiableWordResponseStrategy, \
    CorporateNameConflictResponseStrategy

from namex.services.name_request.auto_analyse import AnalysisResultCodes

from namex.services.name_request.name_analysis_builder_v1.name_analysis_builder import NameAnalysisBuilder
from namex.services.name_request.auto_analyse.auto_analyse import AutoAnalyseService

setup_logging()  # It's important to do this first

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
    # @jwt.requires_auth
    # @api.expect()
    def get():
        # any
        name = request.args.get('name')
        # one of ['bc', 'ca', 'intl']
        location = request.args.get('location')
        # what are the entity types?
        entity_type = request.args.get('entityType')
        # one of ['new', 'existing', 'continuation'
        request_type = request.args.get('requestType')

        # Do our service stuff
        # TODO: How to invoke services? Per call or singleton?
        service = AutoAnalyseService()
        builder = NameAnalysisBuilder(service)

        # Register and initialize the desired builder
        service.use_builder(builder)
        # Execute analysis using the supplied builder
        result = service.execute_analysis()

        # Execute analysis returns a response strategy code
        def response_strategies(strategy):
            strategies = {
                AnalysisResultCodes.VALID_NAME: ValidNameResponseStrategy,
                AnalysisResultCodes.ADD_DISTINCTIVE_WORD: AddDistinctiveWordResponseStrategy,
                AnalysisResultCodes.ADD_DESCRIPTIVE_WORD: AddDescriptiveWordResponseStrategy,
                AnalysisResultCodes.TOO_MANY_WORDS: TooManyWordsResponseStrategy,
                AnalysisResultCodes.CONTAINS_UNCLASSIFIABLE_WORD: ContainsUnclassifiableWordResponseStrategy,
                AnalysisResultCodes.WORD_TO_AVOID: ContainsWordsToAvoidResponseStrategy,
                AnalysisResultCodes.NAME_REQUIRES_CONSENT: NameRequiresConsentResponseStrategy,
                AnalysisResultCodes.DESIGNATION_MISMATCH: DesignationMismatchResponseStrategy,
                AnalysisResultCodes.CORPORATE_CONFLICT: CorporateNameConflictResponseStrategy
            }
            return strategies.get(strategy, 'Invalid response strategy')

        response_strategy = None
        if callable(response_strategies(result.status)):
            response_strategy = response_strategies(result.status)(result.issues)

        payload = response_strategy.build_response().to_json()

        response = make_response(payload, 200)
        return response
