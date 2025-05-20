import copy
import json
from datetime import datetime
from flask import current_app, jsonify, make_response, request
from flask_restx import Namespace, Resource

from namex import jwt
from namex.models import Event as EventDAO
from namex.models import Payment, State, User
from namex.models import Request as RequestDAO
from namex.services import EventRecorder
from namex.utils.auth import cors_preflight
from namex.utils.queue_util import publish_resend_email_notification
from pytz import timezone as pytz_timezone

# Register a local namespace for the event history
api = Namespace('events', description='Audit trail of events for a Name Request')


@cors_preflight('GET, POST')
@api.route('/<string:nr>', methods=['GET', 'POST', 'OPTIONS'])
class Events(Resource):
    @staticmethod
    @jwt.has_one_of_roles([User.APPROVER, User.EDITOR, User.VIEWONLY])
    def get(nr):
        nrd = RequestDAO.query.filter_by(nrNum=nr.upper()).first_or_404().json()
        request_id = 0
        if 'id' in nrd:
            request_id = nrd['id']
        if not request_id:
            return make_response(jsonify({'message': 'Request NR:{} not found'.format(nr)}), 404)

        event = EventDAO.query.filter_by(nrId=request_id).order_by('id').first_or_404().json()
        if 'id' not in event:
            return make_response(jsonify({'message': 'No events for NR:{} not found'.format(nr)}), 404)

        event_results = EventDAO.query.filter_by(nrId=request_id).order_by('id').all()

        # info needed for each event
        nr_event_info = {
            'id': None,
            'additionalInfo': None,
            'consent_dt': None,
            'consentFlag': None,
            'corpNum': None,
            'eventDate': None,
            'expirationDate': None,
            'furnished': None,
            'names': [],
            'priorityCd': None,
            'requestTypeCd': None,
            'request_action_cd': None,
            'stateCd': None,
            'user_action': None,
            'user_name': None,
            ## the following are for notification events
            'option': None,
            'email': None
        }
        # previous event (used for 'user_action' logic)
        e_dict_previous = {}
        # transaction history that will be returned in the payload
        e_txn_history = []

        for e in event_results:
            previous_nr_event_info = copy.deepcopy(nr_event_info)
            e_dict = e.json()
            nr_event_info['id'] = e_dict['id']

            # skip unneeded events for transaction history due to workflow:
            # - 1. patch[checkout] changes the NR state to inprogress
            # - 2. patch[edit] changes NR information (not including state)
            # - 3. patch[checkin] changes the NR state back to it's previous state
            if e_dict['action'] in ['patch [checkout]', 'patch [checkin]']:
                continue

            # update NR state unless action was a patch [edit] (see comment above for why)
            if e_dict['action'] != 'patch [edit]':
                nr_event_info['stateCd'] = e_dict['stateCd']
                # TODO: capture below cases in the event record data
                # if state is CONDITIONAL and consentFlag is null, then set it to Y
                if nr_event_info['stateCd'] == State.CONDITIONAL and nr_event_info['consentFlag'] in ['N', None]:
                    nr_event_info['consentFlag'] = 'Y'
                # if state is not CONDITIONAL remove event consent data
                if nr_event_info['stateCd'] != State.CONDITIONAL:
                    nr_event_info['consentFlag'] = 'N'
                    nr_event_info['consent_dt'] = None

            event_json_data = (
                dict(json.loads(e_dict['jsonData'])) if isinstance(e_dict['jsonData'], str) else e_dict['jsonData']
            )
            if event_json_data:
                if e_dict['action'] == 'notification':
                    Events.__read_notification_json(nr_event_info, event_json_data)
                else:
                    Events.__read_event_json(nr_event_info, event_json_data)

            # update event date
            nr_event_info['eventDate'] = e_dict['eventDate']

            # update username
            user = User.query.filter_by(id=e_dict['userId']).first().json()
            nr_event_info['user_name'] = user['username']

            # update user action
            user_action = e_dict['action']
            if e_dict['action'] == 'patch [edit]':
                user_action = 'Edit NR Details (Name Request)'
            if e_dict['action'] == 'update_from_nro':
                user_action = 'Get NR Details from NRO'
            if e_dict['action'] == 'get' and e_dict['stateCd'] == State.INPROGRESS:
                user_action = 'Get Next NR'
            if e_dict['action'] == 'patch' and e_dict['stateCd'] == State.INPROGRESS:
                user_action = 'Load NR'
            if e_dict['action'] == 'patch' and e_dict['stateCd'] == State.HOLD:
                user_action = 'Hold Request'
            if e_dict['action'] == 'marked_on_hold' and e_dict['stateCd'] == State.HOLD:
                user_action = 'Marked on Hold'
            if e_dict['action'] == 'put' and e_dict['stateCd'] == State.DRAFT:
                user_action = 'Edit NR Details (NameX)'
            if (
                e_dict['action'] == 'put'
                and e_dict['stateCd'] == State.INPROGRESS
                and 'additional' in e_dict['jsonData']
            ):
                if len(e_dict_previous) == 0 or (
                    e_dict_previous['stateCd'] in [State.HOLD, State.DRAFT, State.INPROGRESS]
                ):
                    user_action = 'Edit NR Details (NameX)'
                if e_dict_previous and e_dict_previous['stateCd'] in [
                    State.APPROVED,
                    State.REJECTED,
                    State.CONDITIONAL,
                ]:
                    # event data will still have an expiration date, but actual NR will have cleared
                    nr_event_info['expirationDate'] = None
                    if previous_nr_event_info['furnished'] == 'Y':
                        user_action = 'Reset'
                    else:
                        user_action = 'Re-Open'
            if e_dict['action'] == 'put' and (
                e_dict['stateCd'] == State.APPROVED
                or e_dict['stateCd'] == State.REJECTED
                or e_dict['stateCd'] == State.CONDITIONAL
            ):
                user_action = 'Edit NR Details after Completion'
            if (
                e_dict['action'] == 'put'
                and e_dict['stateCd'] == State.INPROGRESS
                and 'additional' not in e_dict['jsonData']
                and '"state": "NE"' not in e_dict['jsonData']
            ):
                user_action = 'Complete the Name Choice'
            if e_dict['action'] == 'patch' and (
                e_dict['stateCd'] == State.APPROVED
                or e_dict['stateCd'] == State.REJECTED
                or e_dict['stateCd'] == State.CONDITIONAL
            ):
                user_action = 'Decision'
            if (
                e_dict['action'] == 'put'
                and e_dict['stateCd'] == State.INPROGRESS
                and 'additional' not in e_dict['jsonData']
                and '"state": "NE"' in e_dict['jsonData']
            ):
                user_action = 'Undo Decision'
            if e_dict['action'] == 'nro_update' and (
                e_dict['stateCd'] == State.APPROVED
                or e_dict['stateCd'] == State.REJECTED
                or e_dict['stateCd'] == State.CONDITIONAL
            ):
                user_action = 'Updated NRO'
            if e_dict['action'] == 'post' and (event_json_data and 'comment' in event_json_data):
                user_action = 'Staff Comment'
                nr_event_info['comment'] = event_json_data['comment']
            if e_dict['stateCd'] == State.CANCELLED and (
                e_dict['action'] == 'post' or e_dict['action'] == 'update_from_nro'
            ):
                user_action = 'Cancelled in NRO'
            if e_dict['stateCd'] == State.CANCELLED and (e_dict['action'] == 'patch' or e_dict['action'] == 'put'):
                user_action = 'Cancelled in Namex'
            if e_dict['stateCd'] == State.EXPIRED and e_dict['action'] == 'post':
                user_action = 'Expired by NRO'
            if e_dict['stateCd'] == State.HISTORICAL and e_dict['action'] == 'post':
                user_action = 'Set to Historical by NRO(Migration)'
            if e_dict['stateCd'] == State.COMPLETED and (
                e_dict['action'] == 'post' or e_dict['action'] == 'update_from_nro'
            ):
                user_action = 'Migrated by NRO'
            if e_dict['action'] == 'post' and (
                e_dict['stateCd'] in [State.DRAFT, State.PENDING_PAYMENT] and not e_dict_previous
            ):
                # state of these will be DRAFT, but show as PENDING_PAYMENT to avoid confusion
                user_action = 'Created NRL'
                nr_event_info['stateCd'] = State.PENDING_PAYMENT
            if '[rollback]' in e_dict['action']:
                user_action = 'UI Error - NR Rolled Back'
            if '[cancel]' in e_dict['action']:
                user_action = 'Cancelled in Name Request'
            if user_action == EventDAO.NR_DAY_JOB:
                user_action = 'NR Day Job'

            payment_action = ''
            payment_display = {
                Payment.PaymentActions.CREATE.value: 'Created NR',
                Payment.PaymentActions.REAPPLY.value: 'Reapplied NR',
                Payment.PaymentActions.UPGRADE.value: 'Upgraded Priority',
                Payment.PaymentActions.RESUBMIT.value: 'Resubmitted NR',
            }
            for action in Payment.PaymentActions:
                if action.value in e_dict['action']:
                    payment_action = action.value
                    break
            if payment_action:
                if '[payment created]' in e_dict['action']:
                    user_action = f'{payment_display[payment_action]} (Payment Initialized)'
                elif '[payment completed]' in e_dict['action']:
                    user_action = f'{payment_display[payment_action]} (Payment Completed)'
                elif '[payment cancelled]' in e_dict['action']:
                    user_action = f'{payment_display[payment_action]} (Payment Cancelled)'
                elif '[payment refunded]' in e_dict['action']:
                    user_action = f'{payment_display[payment_action]} (Payment Refunded)'
                else:
                    user_action = f'{payment_display[payment_action]} (Unknown)'

            # case where they refund the whole NR (not just a specific payment/event)
            if 'request-refund' in e_dict['action']:
                user_action = 'Refund Requested'

            nr_event_info['user_action'] = user_action

            # add event to transaction history (at the beginning of the list)
            e_txn_history.insert(0, copy.deepcopy(nr_event_info))

            # set previous event
            e_dict_previous = e_dict

        if len(e_txn_history) == 0:
            return make_response(jsonify({'message': f'No valid events for {nr} found'}), 404)

        resp = {'response': {'count': len(e_txn_history)}, 'transactions': e_txn_history}

        return make_response(jsonify(resp), 200)

    @staticmethod
    def __read_notification_json(nr_event_info, event_json_data):
        """
        Private method to process notification JSON data.
        :param nr_event_info: Dictionary to update with event information
        :param event_json_data: JSON data from the event
        """
        nr_event_info['email'] = event_json_data['email']
        nr_event_info['option'] = event_json_data['option']
        nr_event_info['resend_date'] = event_json_data.get('resend_date')

    @staticmethod
    def __read_event_json(nr_event_info, event_json_data):
        """
        Private method to process event JSON data.
        :param nr_event_info: Dictionary to update with event information
        :param event_json_data: JSON data from the event
        """
        if all(key in event_json_data.keys() for key in ['choice', 'name']):
            if len(nr_event_info['names']) > 0:
                update_index = 0
                for name, i in zip(nr_event_info['names'], range(len(nr_event_info['names']))):
                    if name['choice'] == event_json_data['choice']:
                        update_index = i
                        break
                nr_event_info['names'][update_index] = event_json_data
            else:
                nr_event_info['names'].append(event_json_data)
        elif 'state' in event_json_data and event_json_data['state'] == 'CONSUMED':
            for name_info in nr_event_info['names']:
                if name_info.get('state') in ('APPROVED', 'CONDITION'):
                    name_info['corpNum'] = event_json_data['corpNum']
        else:
            for key in nr_event_info.keys():
                if key in event_json_data.keys():
                    if key == 'stateCd':
                        continue
                    nr_event_info[key] = event_json_data[key]
            if 'entity_type_cd' in event_json_data.keys() and 'requestTypeCd' not in event_json_data.keys():
                nr_event_info['requestTypeCd'] = event_json_data['entity_type_cd']

    @staticmethod
    def post(nr):
        """
        Record a new event for a Name Request.
        :param nr: Name Request number
        :return: Response indicating success or failure
        """
        try:
            # Fetch the Name Request
            nrd = RequestDAO.query.filter_by(nrNum=nr.upper()).first_or_404()

            # Parse the payload
            payload = request.get_json()
            if not payload:
                return make_response(jsonify({'message': 'No JSON payload provided'}), 400)

            # Ensure eventJson is serialized
            event_json = payload.get('eventJson', {})

            # Record the event
            EventRecorder.record_as_system(
                payload.get('action'),
                nrd,  # Pass the Name Request ID instead of the request object
                event_json
            )

            return make_response(jsonify({'message': 'Event recorded successfully'}), 201)
        except Exception as e:
            return make_response(jsonify({'message': f'Error recording event: {str(e)}'}), 500)


@cors_preflight('GET, POST, PATCH')
@api.route('/event/<int:event_id>', methods=['GET', 'POST', 'PATCH', 'OPTIONS'])
class SingleEvent(Resource):
    @staticmethod
    def get(event_id):
        """
        Retrieve a single event by its event_id.
        :param event_id: ID of the event
        :return: JSON representation of the event or an error message
        """
        try:
            # Fetch the event by ID
            event = EventDAO.query.get_or_404(event_id)

            # Convert the event to JSON
            event_data = event.json()

            return make_response(jsonify(event_data), 200)
        except Exception as e:
            return make_response(jsonify({'message': f'Error retrieving event: {str(e)}'}), 500)

    @staticmethod
    def post(event_id):
        """
        Resend a notification for a specific event by its event_id.
        :param event_id: ID of the event
        :return: Response indicating success or failure
        """
        try:
            # Fetch the event by ID
            event = EventDAO.query.get_or_404(event_id)

            # Extract necessary data from the event
            event_data = event.json()
            if event_data.get('action') != 'notification':
                return make_response(jsonify({'message': 'Event is not a notification event'}), 400)

            nr_id = event_data.get('requestId')
            nr_num = RequestDAO.find_by_id(nr_id).nrNum if nr_id else None  # Corrected syntax

            # Parse jsonData to a JSON object and extract 'option'
            json_data = event_data.get('jsonData')
            if isinstance(json_data, str):
                json_data = json.loads(json_data)  # Parse if it's a string
            option = json_data.get('option') if json_data else None

            if not nr_num:
                return make_response(jsonify({'message': 'nrNum not found in event data'}), 400)

            if not option:
                return make_response(jsonify({'message': 'option not found in event data'}), 400)

            # Publish the resend notification to the queue
            publish_resend_email_notification(nr_num, option, event_id)

            return make_response(jsonify({'message': 'Resend notification published successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': f'Error publishing resend notification: {str(e)}'}), 500)

    @staticmethod
    def patch(event_id):
        """
        Update the resend_date in the event's eventJson.
        """
        try:
            # 1. Query the existing event
            event = EventDAO.query.get_or_404(event_id)

            # Get the existing eventJson from the model (not from .json(), which may be stale)
            event_json = event.eventJson
            if isinstance(event_json, str):
                event_json = json.loads(event_json)

            # 2. Update or add the resend_date in Pacific timezone, formatted as yyyy-mm-dd, hh:mm PM TZ
            pacific = pytz_timezone('US/Pacific')
            now_pacific = datetime.now(pacific)
            resend_date = now_pacific.strftime('%Y-%m-%d, %I:%M %p %Z')
            event_json['resend_date'] = resend_date

            # 3. Save and commit the change
            event.eventJson = json.dumps(event_json)
            event.save_to_db()

            return make_response(jsonify({'message': f'Event {event_id} updated successfully'}), 200)
        except Exception as e:
            current_app.logger.error(f'Failed to update event {event_id}: {e}')
            return make_response(jsonify({'message': f'Failed to update event {event_id}: {str(e)}'}), 500)

