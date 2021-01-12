"""Requests used to support the namex API

TODO: Fill in a larger description once the API is defined for V1
"""

from flask import make_response, jsonify
from flask_restx import Namespace, Resource, cors
from flask_jwt_oidc import AuthError

from namex.utils.auth import cors_preflight
from namex.utils.api_resource import get_query_param_str
from namex.utils.logging import setup_logging

from .bc_name_analysis_response import BcAnalysisResponse as AnalysisResponse

from namex.services.name_request.auto_analyse import AnalysisRequestActions

from namex.constants import \
    ValidLocations, BCProtectedNameEntityTypes, BCUnprotectedNameEntityTypes, XproUnprotectedNameEntityTypes

from namex.services.name_request.builders.name_analysis_builder import NameAnalysisBuilder
from namex.services.name_request.auto_analyse.protected_name_analysis import ProtectedNameAnalysisService
from namex.services.name_request.auto_analyse.unprotected_name_analysis import UnprotectedNameAnalysisService

setup_logging()  # It's important to do this first

# Register a local namespace for the requests
api = Namespace('bcNameAnalysis', description='API for Analysing BC Names')


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
    if location != ValidLocations.CA_BC.value:
        raise ValueError('Invalid location provided')

    is_protected = False
    is_unprotected = False
    valid_request_actions = []

    if entity_type in BCProtectedNameEntityTypes.list():
        is_protected = True
        valid_request_actions = [
            AnalysisRequestActions.NEW.value,
            AnalysisRequestActions.CHG.value,
            AnalysisRequestActions.MVE.value
        ]
    elif entity_type in BCUnprotectedNameEntityTypes.list():
        is_unprotected = True
        valid_request_actions = (AnalysisRequestActions.NEW.value, AnalysisRequestActions.DBA.value)

    if is_protected and is_unprotected:
        raise ValueError('An entity name cannot be both protected and unprotected')

    if is_protected and entity_type not in BCProtectedNameEntityTypes.list():
        raise ValueError('Invalid entity_type provided for a protected BC entity name')

    if is_unprotected and entity_type not in BCUnprotectedNameEntityTypes.list():
        raise ValueError('Invalid entity_type provided for an unprotected BC entity name')

    if request_action not in valid_request_actions:
        raise Exception('Operation not currently supported')

    return True


@cors_preflight("GET")
@api.route('/', strict_slashes=False, methods=['GET', 'OPTIONS'])
class BcNameAnalysis(Resource):
    """
    We use different service sub-types depending on:

    - the location and the entity type:
      BC:
          NAME PROTECTED:
              CR = 'CORPORATION'
              UL = 'UNLIMITED_LIABILITY_COMPANY'
              CP = 'COOPERATIVE'
              BC = 'BENEFIT_COMPANY'
              CC = 'COMMUNITY_CONTRIBUTION_COMPANY'
          NAME UNPROTECTED (Just check for conflicts!):
              FR = 'SOLE_PROPRIETORSHIP'
              DBA = 'DOING_BUSINESS_AS'
              GP = 'GENERAL_PARTNERSHIP'
              LP = 'LIMITED_PARTNERSHIP'
              LL = 'LIMITED_LIABILITY_PARTNERSHIP'

    - the request actions, which are not location dependent:
      NEW = Start a new business (NAME PROTECTION)
      AML = Amalgamate (NAME PROTECTION, BC ONLY)
      CHG = Change your name
      - It's coming stub it out
      MVE = Move your business
      - Always to examination
      CNV = Convert to another structure
      - Always to examination
      REH = Restore from historical business
      - Always to examination
      REN = Restore by starting a new business
      - Always to examination
    """

    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
        'name': 'A company / organization name string',
        'location': 'A location code [ BC (only)]',
        'entity_type_cd': 'An entity type code [ CR, UL, CC ]',
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

        valid_location = location == ValidLocations.CA_BC.value
        valid_protected_entity_type = entity_type in BCProtectedNameEntityTypes.list()
        valid_unprotected_entity_type = entity_type in BCUnprotectedNameEntityTypes.list()
        is_protected_action = request_action in [AnalysisRequestActions.NEW.value, AnalysisRequestActions.CHG.value,
                                                 AnalysisRequestActions.MVE.value]
        is_unprotected_action = request_action in [AnalysisRequestActions.NEW.value]

        try:
            if valid_location and valid_protected_entity_type and is_protected_action:
                # Use ProtectedNameAnalysisService
                service = ProtectedNameAnalysisService()
                builder = NameAnalysisBuilder(service)

            elif valid_location and valid_unprotected_entity_type and is_unprotected_action:
                # Use UnprotectedNameAnalysisService
                service = UnprotectedNameAnalysisService()
                builder = NameAnalysisBuilder(service)

            else:
                raise Exception('Invalid scenario')

            if not service:
                raise ValueError('Invalid service provided')
            if not builder:
                raise ValueError('Invalid builder provided')

            # Register and initialize the builder
            service.use_builder(builder)  # Required step! TODO: Enforce this!
            service.set_entity_type(entity_type)  # Required step! TODO: Enforce this!

            np_svc_prep_data = service.name_processing_service

            np_svc_prep_data.prepare_data() # Required step! TODO: Enforce this!
            service.set_name(name, np_svc_prep_data)  # Required step! TODO: Enforce this!
            service.set_synonym_dictionaries() # Required step! TODO: Enforce this!

        except Exception as err:
            print('Error initializing BcNameAnalysis service: ' + repr(err.with_traceback(None)))
            raise

        # Perform the name analysis - execute analysis using the supplied builder
        # @:return an array of ProcedureResult[]
        analysis = service.execute_analysis()

        # Build the appropriate response for the analysis result
        analysis_response = AnalysisResponse(service, analysis)
        payload = analysis_response.build_response().to_json()

        response = make_response(payload, 200)
        return response
