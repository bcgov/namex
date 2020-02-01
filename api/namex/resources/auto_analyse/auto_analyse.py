"""Requests used to support the namex API

TODO: Fill in a larger description once the API is defined for V1
"""

from flask import request, make_response, jsonify
from flask_restplus import Namespace, Resource, cors
from flask_jwt_oidc import AuthError

from urllib.parse import unquote_plus

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

from namex.services.name_request.auto_analyse import AnalysisRequestActions

from namex.constants import \
    ValidLocations, BCProtectedNameEntityTypes, BCUnprotectedNameEntityTypes, XproUnprotectedNameEntityTypes

from namex.services.name_request.name_analysis_builder_v2.name_analysis_builder import NameAnalysisBuilder
from namex.services.name_request.auto_analyse.protected_name_analysis import ProtectedNameAnalysisService
from namex.services.name_request.auto_analyse.unprotected_name_analysis import UnprotectedNameAnalysisService

setup_logging()  # It's important to do this first

# Register a local namespace for the requests
api = Namespace('nameAnalysis', description='Name Analysis - Core API for analysing a Name')


@api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


# TODO: Determine whether to throw an Error or Validation
def validate_name_request(location, entity_type, request_action):
    # Raise error if location is invalid
    if location not in ValidLocations:
        raise ValueError('Invalid location provided')

    # Raise error if request_action is invalid
    if request_action not in AnalysisRequestActions.list():
        raise ValueError('Invalid request action provided')

    # Throw any errors related to invalid entity_type or request_action for a location
    if location == ValidLocations.CA_BC:
        is_protected = False
        is_unprotected = False

        # Determine what request actions are valid
        valid_request_actions = ()

        if entity_type in BCProtectedNameEntityTypes:
            is_protected = True
            valid_request_actions = (AnalysisRequestActions.NEW, AnalysisRequestActions.AML)
        elif entity_type in BCUnprotectedNameEntityTypes:
            is_unprotected = True
            valid_request_actions = (AnalysisRequestActions.NEW, AnalysisRequestActions.DBA)

        if is_protected and is_unprotected:
            raise ValueError('An entity name cannot be both protected and unprotected')

        if is_protected and entity_type not in BCProtectedNameEntityTypes:
            raise ValueError('Invalid entity_type provided for a protected BC entity name')

        if is_unprotected and entity_type not in BCUnprotectedNameEntityTypes:
            raise ValueError('Invalid entity_type provided for an unprotected BC entity name')

        if request_action not in valid_request_actions:
            raise Exception('Operation not currently supported')

    elif location in (ValidLocations.CA_NOT_BC, ValidLocations.INTL):
        # If XPRO, nothing is protected (for now anyway)
        valid_request_actions = (AnalysisRequestActions.NEW, AnalysisRequestActions.DBA)

        if entity_type not in XproUnprotectedNameEntityTypes:
            raise ValueError('Invalid entity_type provided for an XPRO entity')

        if request_action not in valid_request_actions:
            raise Exception('Operation not currently supported')

    return True


@cors_preflight("GET")
@api.route('/', strict_slashes=False, methods=['GET', 'OPTIONS'])
class NameAnalysis(Resource):
    '''
    1) What is your location
    2) What type of entity
    3) Does your entity type have NAME PROTECTION

    We use different service sub-types depending on:

    - the location and the entity type:
      BC:
          NAME PROTECTED:
              CR = 'BC_CORPORATION'
              UL = 'BC_UNLIMITED_LIABILITY_COMPANY'
              CP = 'BC_COOPERATIVE'
              BC = 'BC_BENEFIT_COMPANY'
              CC = 'BC_COMMUNITY_CONTRIBUTION_COMPANY'
          NAME UNPROTECTED (Just check for conflicts!):
              FR = 'BC_SOLE_PROPRIETORSHIP'
              DBA = 'BC_DOING_BUSINESS_AS'
              GP = 'BC_GENERAL_PARTNERSHIP'
              LP = 'BC_LIMITED_PARTNERSHIP'
              LL = 'BC_LIMITED_LIABILITY_PARTNERSHIP'
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
        'location': 'A location code [ BC | CA | INTL ]',
        'entity_type': 'An entity type code [ CR, UL, CC ]',
        'request_action': 'A request action code'  # TODO: Use request_action not request_type, this needs to be updated on the front end!!!
        # 'request_type': 'A request action code'  # TODO: Leave this as request_type for now...
    })
    def get():
        name = unquote_plus(request.args.get('name')) if request.args.get('name') else None
        location = unquote_plus(request.args.get('location')) if request.args.get('location') else None
        entity_type = unquote_plus(request.args.get('entity_type')) if request.args.get('entity_type') else None
        # TODO: Let's not call var request_type because it's ambiguous - change to request_action on frontend too
        request_action = unquote_plus(request.args.get('request_action').strip()) if request.args.get('request_action') else None  # TODO: Use request_action not request_type, this needs to be updated on the front end!!!
        # request_action = unquote_plus(request.args.get('request_type').strip()) if request.args.get('request_type') else None  # TODO: Leave this as request_type for now...

        # Do our service stuff
        # Instantiate an appropriate service and register a builder for that service (subclasses of NameAnalysisDirector)
        # We can optionally use a different builder if we want to further tweak analysis by modifying the following procedures:
        # do_analysis (performs the checks)
        # check_name_is_well_formed
        # check_words_to_avoid
        # search_conflicts
        # check_words_requiring_consent
        # check_designation

        service = None

        if not validate_name_request(location, entity_type, request_action):
            return  # TODO: Return invalid response! What is it?

        try:
            if location == ValidLocations.CA_BC and entity_type in BCProtectedNameEntityTypes and request_action in (AnalysisRequestActions.NEW, AnalysisRequestActions.AML):
                # Use ProtectedNameAnalysisService
                service = ProtectedNameAnalysisService()
                builder = NameAnalysisBuilder(service)

            elif location == ValidLocations.CA_BC and entity_type in BCUnprotectedNameEntityTypes and request_action in AnalysisRequestActions.NEW:
                # Use UnprotectedNameAnalysisService
                service = UnprotectedNameAnalysisService()
                builder = NameAnalysisBuilder(service)

            elif location in (ValidLocations.CA_NOT_BC, ValidLocations.INTL) and entity_type in XproUnprotectedNameEntityTypes and request_action in (AnalysisRequestActions.NEW, AnalysisRequestActions.DBA):
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
            service.set_name(name)  # Required step! TODO: Enforce this!

        except Exception as error:
            print('Error initializing NameAnalysisService: ' + repr(error))
            raise

        # Perform the name analysis - execute analysis using the supplied builder
        # @:return an array of ProcedureResult[]
        analysis = service.execute_analysis()

        # Build the appropriate response for the analysis result
        analysis_response = AnalysisResponse(entity_type, analysis)
        payload = analysis_response.build_response().to_json()

        response = make_response(payload, 200)
        return response
