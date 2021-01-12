"""Requests used to support the namex API

TODO: Fill in a larger description once the API is defined for V1
"""

from flask import make_response, jsonify
from flask_restx import Namespace, Resource, cors
from flask_jwt_oidc import AuthError

from namex.utils.auth import cors_preflight
from namex.utils.api_resource import get_query_param_str
from namex.utils.logging import setup_logging

from namex.services.name_request.auto_analyse.protected_name_analysis import ProtectedNameAnalysisService

from .xpro_name_analysis_response import XproAnalysisResponse as AnalysisResponse
from namex.services.name_request.auto_analyse import AnalysisRequestActions

from namex.constants import \
    ValidLocations, XproUnprotectedNameEntityTypes

from namex.services.name_request.builders.name_analysis_builder import NameAnalysisBuilder
from namex.services.name_request.auto_analyse.xpro_name_analysis import XproNameAnalysisService

setup_logging()  # It's important to do this first

# Register a local namespace for the requests
api = Namespace('xproNameAnalysis', description='API for Analysing Extra-Provincial Names')


@api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


# TODO: Determine whether to throw an Error or Validation
def validate_name_request(location, entity_type, request_action):
    # Raise error if location is invalid
    if location not in ValidLocations.list():
        raise ValueError('Invalid location provided')

    # Raise error if request_action is invalid
    if request_action not in AnalysisRequestActions.list():
        raise ValueError('Invalid request action provided')

    # Throw any errors related to invalid entity_type or request_action for a location
    valid_location = location in [ValidLocations.CA_NOT_BC.value, ValidLocations.INTL.value]
    valid_request_actions = [
        AnalysisRequestActions.NEW.value,
        AnalysisRequestActions.AML.value,
        AnalysisRequestActions.CHG.value,
        AnalysisRequestActions.ASSUMED.value,
        AnalysisRequestActions.REN.value,
        AnalysisRequestActions.REH.value,
        AnalysisRequestActions.MVE.value
    ]

    if not valid_location:
        raise ValueError('Invalid location provided')

    if entity_type not in XproUnprotectedNameEntityTypes.list():
        raise ValueError('Invalid entity_type provided for an XPRO entity')

    if request_action not in valid_request_actions:
        raise Exception('Operation not currently supported')

    return True


@cors_preflight("GET")
@api.route('/', strict_slashes=False, methods=['GET', 'OPTIONS'])
class XproNameAnalysis(Resource):
    """
    We use different service sub-types depending on:

    - the location and the entity type:
      NOT BC:
          XCR = 'XPRO_CORPORATION'
          XUL = 'XPRO_UNLIMITED_LIABILITY_COMPANY'
          XCP = 'XPRO_COOPERATIVE'
          XLC = 'XPRO_LIMITED_LIABILITY_COMPANY'
          XLP = 'XPRO_LIMITED_PARTNERSHIP'
          XLL = 'XPRO_LIMITED_LIABILITY_PARTNERSHIP'

    - the request actions, which are not location dependent:
      NEW = Start a new business (NAME PROTECTION)
      CHG = Change your name
      ASSUMED = Assumed Name only for certain entity types. handled on the fornt-end
    """

    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
        'name': 'A company / organization name string',
        'location': 'A location code [ CA (only) ]',
        'entity_type_cd': 'An entity type code [ XCR, RLC ]',
        'request_action_cd': 'A request action code [ NEW ]'
    })
    def get():
        name = get_query_param_str('name')
        location = get_query_param_str('location')
        entity_type = get_query_param_str('entity_type_cd')
        request_action = get_query_param_str('request_action_cd')

        service = None

        if not validate_name_request(location, entity_type, request_action):
            return  # TODO: Return invalid response! What is it?

        valid_location = location in [ValidLocations.CA_NOT_BC.value, ValidLocations.INTL.value]
        valid_entity_type = entity_type in XproUnprotectedNameEntityTypes.list()

        try:
            if valid_location and valid_entity_type and request_action in (AnalysisRequestActions.NEW.value,
                                                                           AnalysisRequestActions.AML.value,
                                                                           AnalysisRequestActions.CHG.value,
                                                                           AnalysisRequestActions.ASSUMED.value,
                                                                           AnalysisRequestActions.REN.value,
                                                                           AnalysisRequestActions.REH.value,
                                                                           AnalysisRequestActions.MVE.value):

                service = ProtectedNameAnalysisService() if request_action == AnalysisRequestActions.MVE.value else XproNameAnalysisService()
                builder = NameAnalysisBuilder(service)

            else:
                raise Exception('Invalid scenario')

            if not service:
                raise ValueError('Invalid service provided')
            if not builder:
                raise ValueError('Invalid builder provided')

            # Update entity type to Protected Name
            if request_action == AnalysisRequestActions.MVE.value:
                entity_type = entity_type[1:] if entity_type[0] == 'X' else entity_type

            # Register and initialize the builder
            service.use_builder(builder)  # Required step! TODO: Enforce this!
            service.set_entity_type(entity_type)  # Required step! TODO: Enforce this!

            np_svc_prep_data = service.name_processing_service

            np_svc_prep_data.prepare_data()  # Required step! TODO: Enforce this!
            service.set_name(name, np_svc_prep_data)  # Required step! TODO: Enforce this!
            service.set_synonym_dictionaries()  # Required step! TODO: Enforce this!

        except Exception as err:
            print('Error initializing XproNameAnalysis service: ' + repr(err.with_traceback(None)))
            raise

        # Perform the name analysis - execute analysis using the supplied builder
        # @:return an array of ProcedureResult[]
        analysis = service.execute_analysis()

        # Build the appropriate response for the analysis result
        analysis_response = AnalysisResponse(service, analysis)
        payload = analysis_response.build_response().to_json()

        response = make_response(payload, 200)
        return response
