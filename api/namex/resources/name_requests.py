from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields, cors
from flask_jwt_oidc import AuthError
from namex.utils.util import cors_preflight
import json
from namex import jwt, services
from flask import current_app
from namex.models import db

from namex.utils.logging import setup_logging
setup_logging() ## important to do this first

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.inspection import inspect

from urllib.parse import unquote_plus
from datetime import datetime

from namex.models import Request, Name, NRNumber, User, Event,State,Comment
from namex.services import ServicesError, MessageServices, EventRecorder
from namex.services.name_request import get_or_create_user_by_jwt, convert_to_ascii

from namex.services.name_request.auto_analyse import AnalysisRequestActions

from namex.constants import \
    ValidLocations, BCProtectedNameEntityTypes, BCUnprotectedNameEntityTypes, XproUnprotectedNameEntityTypes


# Register a local namespace for the NR reserve
api = Namespace('nameRequests', description='Public facing Name Requests')

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
    if location == ValidLocations.CA_BC.value:
        is_protected = False
        is_unprotected = False

        # Determine what request actions are valid
        valid_request_actions = ()

        if entity_type in BCProtectedNameEntityTypes.list():
            is_protected = True
            valid_request_actions = (AnalysisRequestActions.NEW.value, AnalysisRequestActions.AML.value)

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

    elif location in (ValidLocations.CA_NOT_BC.list(), ValidLocations.INTL.list()):
        # If XPRO, nothing is protected (for now anyway)
        valid_request_actions = (AnalysisRequestActions.NEW.value, AnalysisRequestActions.DBA.value)

        if entity_type not in XproUnprotectedNameEntityTypes.list():
            raise ValueError('Invalid entity_type provided for an XPRO entity')

        if request_action not in valid_request_actions:
            raise Exception('Operation not currently supported')

    return True

@cors_preflight("POST")
@api.route('/', strict_slashes=False, methods=['POST', 'OPTIONS'])
class NameRequest(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_roles([User.PUBLIC])

    @api.doc(params={
        'name': 'A company / organization name string',
        'location': 'A location code [ BC | CA | INTL ]',
        'entity_type': 'An entity type code [ CR, UL, CC ]',
        'request_action': 'A request action code',
        'designation': 'The designation if at the end'
    })
    def post():
        #ADD THE CHECK FOR USERNAME_RQEQUEST SERVICE ACCOUNT BEFORE PROCEEDING
        name = unquote_plus(request.args.get('name').strip()) if request.args.get('name') else None
        location = unquote_plus(request.args.get('location').strip()) if request.args.get('location') else None
        entity_type = unquote_plus(request.args.get('entity_type').strip()) if request.args.get('entity_type') else None
        request_action = unquote_plus(request.args.get('request_action').strip()) if request.args.get('request_action') else None
        designation = unquote_plus(request.args.get('designation').strip()) if request.args.get('designation') else None

        if not validate_name_request(location, entity_type, request_action):
            return jsonify(message='Incorrect input data provided'), 400

        name_request = Request()
        reserved_name = Name()

        seq = db.Sequence('requests_id_seq')
        next_nr_id = db.engine.execute(seq)

        r = db.session.query(NRNumber).first()
        if(r == None):
            #set starting nr number
            last_nr = 'NR L000000'
        else:
            last_nr = r.nrNum
        next_nr_num = NRNumber.get_next_nr_num(last_nr)
        r.nrNum = next_nr_num
        r.save_to_db()

        #set the name attributes
        name_request.id = next_nr_id
        name_request.submittedDate=datetime.utcnow()
        name_request.nrNum=next_nr_num # must be replaced with a formula
        # requestTypeCd= a formuls,
        # expirationDate= formula submitted date + 56 days,
        #consentFlag= #need more data (by reserved or conditionally reserved)
        name_request.stateCd='RESERVED'  # must be reserved

        #name_request.entity_type_cd = entity_type
        #name_request.request_action_cd = request_action

        reserved_name.choice = 1
        reserved_name.name = name
        reserved_name.state = 'RESERVED'
        reserved_name.designation = designation
        reserved_name.nrId = next_nr_id

        name_request.names.append(reserved_name)
        name_request.save_to_db()

        current_app.logger.debug(name_request.json())
        return jsonify(name_request.json()), 200






