"""Requests used to support the namex API.

TODO: Fill in a larger description once the API is defined for V1
"""
from http import HTTPStatus

from flask import jsonify, make_response
from flask.globals import current_app
from flask_restx import Namespace, Resource, cors

from namex.constants import (  # noqa: I001
    BCProtectedNameEntityTypes,  # noqa: I001
    BCUnprotectedNameEntityTypes,  # noqa: I001
    ValidLocations,  # noqa: I001
    XproUnprotectedNameEntityTypes,  # noqa: I001
)  # noqa: I001
from namex.services.name_request.auto_analyse import AnalysisIssueCodes, AnalysisRequestActions  # noqa: I005
from namex.services.name_request.auto_analyse.protected_name_analysis import ProtectedNameAnalysisService
from namex.services.name_request.auto_analyse.unprotected_name_analysis import UnprotectedNameAnalysisService
from namex.services.name_request.auto_analyse.xpro_name_analysis import XproNameAnalysisService
from namex.services.name_request.builders.name_analysis_builder import NameAnalysisBuilder
from namex.utils.api_resource import get_query_param_str
from namex.utils.auth import cors_preflight
from namex.utils.logging import setup_logging

from .bc_name_analysis_response import BcAnalysisResponse
from .xpro_name_analysis_response import XproAnalysisResponse


setup_logging()  # It's important to do this first

# Register a local namespace for the requests
api = Namespace('nameAnalysis', description='API for Analysing BC Names')


def bc_validate_name_request(location, entity_type, request_action):
    """Validate the params for bc analysis."""
    errors = []
    # Check location is valid
    if location != ValidLocations.CA_BC.value:
        errors.append('Invalid location provided')

    # Check request_action is valid
    if request_action not in AnalysisRequestActions.list():
        errors.append('Invalid request action provided')

    is_protected = False
    is_unprotected = False
    valid_request_actions = []
    if entity_type in BCProtectedNameEntityTypes.list():
        is_protected = True
        valid_request_actions = [
            AnalysisRequestActions.NEW.value,
            AnalysisRequestActions.CHG.value,
            AnalysisRequestActions.MVE.value,
            AnalysisRequestActions.REH.value,
            AnalysisRequestActions.REN.value,
            AnalysisRequestActions.CNV.value,
            AnalysisRequestActions.AML.value
        ]
    # elif entity_type in BCUnprotectedNameEntityTypes.list():
    #     is_unprotected = True
    #     valid_request_actions = (AnalysisRequestActions.NEW.value, AnalysisRequestActions.DBA.value)

    if is_protected and is_unprotected:
        errors.append('An entity name cannot be both protected and unprotected')

    if is_protected and entity_type not in BCProtectedNameEntityTypes.list():
        errors.append('Invalid entity_type provided for a protected BC entity name')

    if is_unprotected and entity_type not in BCUnprotectedNameEntityTypes.list():
        errors.append('Invalid entity_type provided for an unprotected BC entity name')

    if request_action not in valid_request_actions:
        errors.append('Operation not currently supported')

    return errors


def xpro_validate_name_request(location, entity_type, request_action):
    """Validate the params for xpro analysis."""
    errors = []

    # Check if location is invalid
    if location not in ValidLocations.list():
        errors.append('Invalid location provided')

    # Check if request_action is invalid
    if request_action not in AnalysisRequestActions.list():
        errors.append('Invalid request action provided')

    # Check validity for entity_type or request_action for a location
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
        errors.append('Invalid location provided')

    if entity_type not in XproUnprotectedNameEntityTypes.list():
        errors.append('Invalid entity_type provided for an XPRO entity')

    if request_action not in valid_request_actions:
        errors.append('Operation not currently supported')

    return errors


@cors_preflight('GET')
@api.route('/', strict_slashes=False, methods=['GET', 'OPTIONS'])
class NameAnalysis(Resource):
    """Name analysis endpoint.

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
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
        'name': 'A company / organization name string',
        'location': 'A location code [ BC (only)]',
        'entity_type_cd': 'An entity type code [ CR, UL, CC ]',
        'request_action_cd': 'A request action code [ NEW ]',
        'analysis_type': '[ designation, structure ]',
        'jurisdiction': '[ BC, XPRO ]'
    })
    def get():
        """Get structure analysis for a name."""
        name = get_query_param_str('name')
        allowed_special_chars = ['/', '[', ']', '^', '*', '+', '=', '&', '(', ')', ',', '”', '’', '#', '@', '!', '?', ';', ':']
        for special_char in allowed_special_chars:
            name = name.replace(special_char, ' ')
        location = get_query_param_str('location')
        entity_type = get_query_param_str('entity_type_cd')
        request_action = get_query_param_str('request_action_cd')
        designation_only = get_query_param_str('analysis_type') in ['designation', None]
        # TODO: take out xpro flow entirely (not used in name analysis flow anymore)
        xpro = get_query_param_str('jurisdiction') not in ['BC', None]
        if xpro:
            return jsonify(message=['xpro not supported']), HTTPStatus.NOT_IMPLEMENTED
        service = None

        errors = bc_validate_name_request(location, entity_type, request_action)  # \
            # if not xpro else xpro_validate_name_request(location, entity_type, request_action)
        if errors:
            return jsonify(message=errors), HTTPStatus.BAD_REQUEST

        # # used for BC
        # valid_protected_entity_type = None
        # valid_unprotected_entity_type = None
        # is_protected_action = None
        # is_unprotected_action = None
        # # used for XPRO
        # valid_xpro_action = None
        # # used for both
        # valid_location = None
        # valid_entity_type = None
        # if xpro:
        #     valid_location = location in [ValidLocations.CA_NOT_BC.value, ValidLocations.INTL.value]
        #     valid_entity_type = entity_type in XproUnprotectedNameEntityTypes.list()
        #     valid_xpro_action = request_action in [
        #         AnalysisRequestActions.NEW.value,
        #         AnalysisRequestActions.AML.value,
        #         AnalysisRequestActions.CHG.value,
        #         AnalysisRequestActions.ASSUMED.value,
        #         AnalysisRequestActions.REN.value,
        #         AnalysisRequestActions.REH.value,
        #         AnalysisRequestActions.MVE.value
        #     ]
        # else:
        #     valid_location = location == ValidLocations.CA_BC.value
        #     valid_protected_entity_type = entity_type in BCProtectedNameEntityTypes.list()
        #     valid_unprotected_entity_type = entity_type in BCUnprotectedNameEntityTypes.list()
        #     is_protected_action = request_action in [
        #         AnalysisRequestActions.NEW.value,
        #         AnalysisRequestActions.CHG.value,
        #         AnalysisRequestActions.MVE.value
        #     ]
        #     is_unprotected_action = request_action in [AnalysisRequestActions.NEW.value]

        try:
            # if xpro:
            #     if valid_location and valid_entity_type and valid_xpro_action:
            #         service = ProtectedNameAnalysisService() \
            #             if request_action == AnalysisRequestActions.MVE.value else XproNameAnalysisService()
            #         builder = NameAnalysisBuilder(service)
            #     else:
            #         return jsonify(message=['Invalid scenario']), HTTPStatus.BAD_REQUEST

            # else:
            # if valid_location and valid_protected_entity_type:  # and is_protected_action:
            #  # Use ProtectedNameAnalysisService
            service = ProtectedNameAnalysisService()
            builder = NameAnalysisBuilder(service)
            # else:  # valid_location and valid_unprotected_entity_type:  # and is_unprotected_action:
                # Use UnprotectedNameAnalysisService
                # service = UnprotectedNameAnalysisService()
                # builder = NameAnalysisBuilder(service)
            # else:
            #     return jsonify(message=['Invalid scenario']), HTTPStatus.BAD_REQUEST

            if not service:
                return jsonify(message=['Failed to initialize service']), HTTPStatus.INTERNAL_SERVER_ERROR
            if not builder:
                return jsonify(message=['Failed to initialize builder']), HTTPStatus.INTERNAL_SERVER_ERROR

            # Register and initialize the builder
            service.use_builder(builder)  # Required step! TODO: Enforce this!
            service.set_entity_type(entity_type)  # Required step! TODO: Enforce this!
            service.set_name(name, designation_only)  # Required step! TODO: Enforce this!

        except Exception as err:
            current_app.logger.error('Error initializing NameAnalysis service: ' + repr(err.with_traceback(None)))
            raise

        # Perform the name analysis - execute analysis using the supplied builder
        # @:return an array of ProcedureResult[]
        analysis = service.execute_analysis(designation_only)

        # Build the appropriate response for the analysis result
        analysis_response = BcAnalysisResponse(service, analysis)  # \
            # if not xpro else XproAnalysisResponse(service, analysis)

        # Remove issues for end designation more than once if they are not duplicates
        valid_issues = []
        for issue in analysis_response.issues:
            if issue.issue_type == AnalysisIssueCodes.END_DESIGNATION_MORE_THAN_ONCE:
                valid_name_actions = []
                seen_designations = []
                for name_action in issue.name_actions:
                    if name_action.word in seen_designations:
                        valid_name_actions.append(name_action)
                    else:
                        seen_designations.append(name_action.word)
                if len(valid_name_actions) > 0:
                    issue.name_actions = valid_name_actions
                    valid_issues.append(issue)
                # else ^ this issue will not be added to the response
            else:
                valid_issues.append(issue)

        analysis_response.issues = valid_issues
        payload = analysis_response.build_response().to_json()
        response = make_response(payload, HTTPStatus.OK)
        return response
