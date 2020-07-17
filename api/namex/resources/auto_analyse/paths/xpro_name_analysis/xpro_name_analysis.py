"""Requests used to support the namex API

TODO: Fill in a larger description once the API is defined for V1
"""

from flask import request, make_response, jsonify
from flask_restplus import Namespace, Resource, cors
from flask_jwt_oidc import AuthError

from urllib.parse import unquote_plus

from namex.services.name_request.auto_analyse.protected_name_analysis import ProtectedNameAnalysisService
from namex.utils.util import cors_preflight
from namex.utils.logging import setup_logging

from .xpro_name_analysis_response import XproAnalysisResponse as AnalysisResponse
from namex.services.name_request.auto_analyse import AnalysisRequestActions

from namex.constants import \
    ValidLocations, XproUnprotectedNameEntityTypes

from namex.services.name_request.builders.name_analysis_builder import NameAnalysisBuilder
from namex.services.name_request.auto_analyse.xpro_name_analysis import XproNameAnalysisService

setup_logging()  # It's important to do this first

# Register a local namespace for the requests
api = Namespace('xproNameAnalysis', description='Xpro Name Analysis API for analysing Extra-Provincial Names')


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
        AnalysisRequestActions.CHG.value,
        AnalysisRequestActions.CNV.value,
        AnalysisRequestActions.DBA.value,
        AnalysisRequestActions.MVE.value,
        AnalysisRequestActions.REH.value,
        AnalysisRequestActions.REST.value,
        AnalysisRequestActions.REN.value
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
    '''
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
      AML = Amalgamate (NAME PROTECTION, BC ONLY)
      DBA = Get a new trade name (NO NAME PROTECTION)
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
    '''
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
        'name': 'A company / organization name string',
        'location': 'A location code [ CA (only) ]',
        'entity_type': 'An entity type code [ XCR, RLC ]',
        'request_action': 'A request action code [ NEW ]'
    })
    def get():
        name = unquote_plus(request.args.get('name').strip()) if request.args.get('name') else None
        location = unquote_plus(request.args.get('location').strip()) if request.args.get('location') else None
        entity_type = unquote_plus(request.args.get('entity_type').strip()) if request.args.get('entity_type') else None
        request_action = unquote_plus(request.args.get('request_action').strip()) if request.args.get('request_action') else None

        service = None

        if not validate_name_request(location, entity_type, request_action):
            return  # TODO: Return invalid response! What is it?

        valid_location = location in [ValidLocations.CA_NOT_BC.value, ValidLocations.INTL.value]
        valid_entity_type = entity_type in XproUnprotectedNameEntityTypes.list()
        is_mve_action = request_action == AnalysisRequestActions.MVE.value
        is_other_action = request_action in [
            AnalysisRequestActions.NEW.value,
            AnalysisRequestActions.CHG.value,
            AnalysisRequestActions.CNV.value,
            AnalysisRequestActions.DBA.value,
            AnalysisRequestActions.REH.value,
            AnalysisRequestActions.REST.value,
            AnalysisRequestActions.REN.value
        ]

        try:
            if valid_location and valid_entity_type and is_mve_action:
                # Use ProtectedNameAnalysisService
                service = ProtectedNameAnalysisService()
                builder = NameAnalysisBuilder(service)
            elif valid_location and valid_entity_type and is_other_action:
                # Use UnprotectedNameAnalysisService
                service = XproNameAnalysisService()
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
            service.set_name(name)  # Required step! TODO: Enforce this!

        except Exception as error:
            print('Error initializing NameAnalysisService: ' + repr(error))
            raise

        # Perform the name analysis - execute analysis using the supplied builder
        # @:return an array of ProcedureResult[]
        analysis = service.execute_analysis()

        # Build the appropriate response for the analysis result
        analysis_response = AnalysisResponse(service, analysis)
        payload = analysis_response.build_response().to_json()

        response = make_response(payload, 200)
        return response
