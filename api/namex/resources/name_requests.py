from flask import jsonify, request
from flask_restplus import Namespace, Resource, cors
from namex.utils.util import cors_preflight
from flask import current_app
from namex.models import db
from datetime import timedelta
from pytz import timezone

from namex.utils.logging import setup_logging
setup_logging() ## important to do this first

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.inspection import inspect

from urllib.parse import unquote_plus
from datetime import datetime

from namex.models import Request, Name, NRNumber

from namex.services import ServicesError, MessageServices, EventRecorder

from namex.services.name_request.auto_analyse import AnalysisRequestActions

from namex.constants import request_type_mapping, RequestAction, EntityType


# Register a local namespace for the NR reserve
api = Namespace('nameRequests', description='Public facing Name Requests')


# TODO: Determine whether to throw an Error or Validation
def validate_name_request(entity_type, request_action):

    # Raise error if entity_type is invalid
    if entity_type not in EntityType.list():
        raise ValueError('Invalid request action provided')

    # Raise error if request_action is invalid
    if request_action not in RequestAction.list():
        raise ValueError('Invalid request action provided')
    #TODO Add a check for valid states include the states in constnats, they are somewhereright now
    # may want to move them
    return True

def set_request_type(entity_type, request_action):
    for item in request_type_mapping:
        if(item[1] == entity_type and item[2] == request_action):
            output = item
            break
    request_type =  list(output)
    return request_type[0]


def create_expiry_date(start: datetime, expires_in_days: int, expiry_hour: int = 23, expiry_min: int = 59,
                           tz: timezone = timezone('US/Pacific')) -> datetime:

        date = (start.astimezone(tz) + timedelta(days=expires_in_days)) \
            .replace(hour=expiry_hour, minute=expiry_min, second=0, microsecond=0)

        return date

@cors_preflight("POST")
@api.route('/', strict_slashes=False, methods=['POST', 'OPTIONS'])
class NameRequest(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')

    @api.doc(params={
        'name': 'A company / organization name string inclduing designation',
        'entity_type': 'An entity type code [ CR, UL, CC ]',
        'request_action': 'A request action code',
        'designation': 'The designation if at the end',
        'reserve_state': 'Reservation state [ RESERVED | COND-RESERVE]'
    })

    def post():
        name = unquote_plus(request.args.get('name').strip()) if request.args.get('name') else None
        entity_type = unquote_plus(request.args.get('entity_type').strip()) if request.args.get('entity_type') else None
        request_action = unquote_plus(request.args.get('request_action').strip()) if request.args.get('request_action') else None
        designation = unquote_plus(request.args.get('designation').strip()) if request.args.get('designation') else None
        reserve_state = unquote_plus(request.args.get('reserve_state').strip()) if request.args.get('reserve_state') else None

        if not validate_name_request(entity_type, request_action):
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
            #TODO:Add a check whne the number has reached 999999
            # and you need to roll over to teh next letter in the alphabet and reste the number to 000000

        next_nr_num = NRNumber.get_next_nr_num(last_nr)
        r.nrNum = next_nr_num
        r.save_to_db()

        #set the name attributes
        name_request.id = next_nr_id
        name_request.submittedDate=datetime.utcnow()
        name_request.requestTypeCd = set_request_type(entity_type, request_action)
        name_request.nrNum=next_nr_num # must be replaced with a formula
        if(reserve_state == 'COND-RESERVE'):
            name_request.consentFlag =  'Y'
            #could also set the consent decision text

        name_request.expirationDate= create_expiry_date(start=name_request.submittedDate, expires_in_days=56, tz=timezone('UTC'))
        name_request.stateCd=reserve_state

        name_request.entity_type_cd = entity_type
        name_request.request_action_cd= request_action
        reserved_name.choice = 1
        reserved_name.name = name
        reserved_name.state = reserve_state
        reserved_name.designation = designation
        reserved_name.nrId = next_nr_id
        name_request.names.append(reserved_name)
        name_request.save_to_db()

        current_app.logger.debug(name_request.json())
        return jsonify(name_request.json()), 200






