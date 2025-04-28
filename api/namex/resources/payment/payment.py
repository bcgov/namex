import json
from datetime import datetime

import requests
from dateutil import parser as dateutil_parser
from flask import current_app, jsonify, make_response, request
from flask_jwt_oidc import AuthError
from flask_restx import fields

from namex import jwt
from namex.constants import NameRequestActions, PaymentState, PaymentStatusCode
from namex.models import Event, State, User
from namex.models import Payment as PaymentDAO
from namex.models import Request as RequestDAO
from namex.resources.name_requests.abstract_nr_resource import AbstractNameRequestResource
from namex.services import EventRecorder
from namex.services.name_request.name_request_state import get_nr_state_actions, is_reapplication_eligible
from namex.services.name_request.utils import get_active_payment, has_active_payment
from namex.services.payment.exceptions import PaymentServiceError, SBCPaymentError, SBCPaymentException
from namex.services.payment.models import PaymentRequest
from namex.services.payment.payments import cancel_payment, create_payment, get_payment, refund_payment
from namex.utils.api_resource import clean_url_path_param, handle_exception
from namex.utils.auth import cors_preflight, validate_roles

from .api_namespace import api as payment_api
from .utils import build_payment_request, merge_payment_request

MSG_BAD_REQUEST_NO_JSON_BODY = 'No JSON data provided'
MSG_SERVER_ERROR = 'Server Error!'

NAME_REQUEST_EXTENSION_PAD_HOURS = 12  # TODO this should be defined as a lookup from somewhere


# Define our DTO models
# Generic model types
dictionary_list_model = payment_api.model('DictionaryList', {'key': fields.String, 'list': fields.List(fields.String)})

dict_list_model = payment_api.model('DictionaryListList', {'data': fields.List(fields.Nested(dictionary_list_model))})

list_model = payment_api.model('List', {'data': fields.List(fields.String)})

string_model = payment_api.model('String', {'data': fields.String})

# Custom model types
payment_info_schema = payment_api.model('PaymentInfo', {'methodOfPayment': fields.String})

filing_type_schema = payment_api.model(
    'FilingType', {'filingTypeCode': fields.String, 'priority': fields.Boolean, 'filingDescription': fields.String}
)

filing_info_schema = payment_api.model(
    'FilingInfo',
    {
        'corpType': fields.String,
        'date': fields.String,
        'filingTypes': fields.List(fields.Nested(filing_type_schema)),
    },
)

contact_info_schema = payment_api.model(
    'ContactInfo',
    {
        # 'firstName': fields.String,
        # 'lastName': fields.String,
        'addressLine1': fields.String,
        'city': fields.String,
        'province': fields.String,
        'country': fields.String,
        'postalCode': fields.String,
    },
)

business_info_schema = payment_api.model(
    'BusinessInfo',
    {
        'businessIdentifier': fields.String,
        'businessName': fields.String,
        'contactInfo': fields.Nested(contact_info_schema),
    },
)


payment_invoice_schema = payment_api.model(
    'PaymentInvoice',
    {
        'id': fields.String,
        'referenceNumber': fields.String,
        'statusCode': fields.String,
        'createdBy': fields.String,
        'createdOn': fields.String,
    },
)

payment_response_schema = payment_api.model(
    'Payment',
    {
        'id': fields.String,
        'invoices': fields.List(fields.Nested(payment_invoice_schema)),
        'paymentMethod': fields.String,
        'statusCode': fields.String,
        'createdBy': fields.String,
        'createdOn': fields.String,
        'updatedBy': fields.String,
        'updatedOn': fields.String,
    },
)

# Define our request objects
# These are POSTED use camelCase
payment_request_schema = payment_api.model(
    'PaymentRequest',
    {
        'paymentInfo': fields.Nested(payment_info_schema),
        'businessInfo': fields.Nested(business_info_schema),
        'filingInfo': fields.Nested(filing_info_schema),
    },
)


@payment_api.errorhandler(AuthError)
def handle_auth_error(ex):
    """Handle auth error."""
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


def custom_strftime_suffix(d):
    """Custom time with suffix."""
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def custom_strftime(dt_format, t):
    """Custom time."""
    return t.strftime(dt_format).replace('{S}', str(t.day) + custom_strftime_suffix(t.day))


def format_payment_time(dt):
    """Format payment time."""
    return dt.strftime('%b %d, %Y')


def map_receipt(receipt):
    """Map receipt."""
    if isinstance(receipt['receiptDate'], str):
        receipt['receiptDate'] = format_payment_time(dateutil_parser.parse(receipt['receiptDate']))

    return receipt


def handle_payment_response(payment_action, payment_response, payment, nr_id, nr_model, nr_svc):
    """Handle payment response."""
    try:
        successful_status_list = [
            PaymentStatusCode.APPROVED.value,
            PaymentStatusCode.CREATED.value,
            PaymentStatusCode.COMPLETED.value,
        ]
        if payment_response.statusCode in successful_status_list:
            # Update the payment info to Postgres
            payment.payment_token = str(payment_response.id)
            # namex-pay will set payment_status_code to completed state after actioning it on the queue
            payment.payment_status_code = payment_response.statusCode
            payment.save_to_db()

            # happens for PAD. If completed/approved right away queue will have err'd so apply changes here
            # TODO: send email / furnish payment for these
            if payment_response.statusCode in [PaymentStatusCode.APPROVED.value, PaymentStatusCode.COMPLETED.value]:
                if payment_action in [PaymentDAO.PaymentActions.CREATE.value, PaymentDAO.PaymentActions.RESUBMIT.value]:  # pylint: disable=R1705
                    if nr_model.stateCd == State.PENDING_PAYMENT:
                        nr_model.stateCd = State.DRAFT
                    payment.payment_completion_date = datetime.utcnow()

                elif payment_action == PaymentDAO.PaymentActions.UPGRADE.value:
                    # TODO: handle this (refund payment and prevent action?)
                    if nr_model.stateCd == State.PENDING_PAYMENT:
                        msg = f'Upgrading a non-DRAFT NR for payment.id={payment.id}'
                        current_app.logger.debug(msg)

                    nr_model.priorityCd = 'Y'
                    nr_model.priorityDate = datetime.utcnow()
                    payment.payment_completion_date = datetime.utcnow()

                elif payment_action == PaymentDAO.PaymentActions.REAPPLY.value:
                    # TODO: handle this (refund payment and prevent action?)

                    if is_reapplication_eligible(nr_model.expirationDate):
                        expiry_days = nr_svc.get_expiry_days(nr_model.request_action_cd, nr_model.requestTypeCd)
                        nr_model.expirationDate = nr_svc.create_expiry_date(nr_model.expirationDate, expiry_days)
                    payment.payment_completion_date = datetime.utcnow()

                nr_model.save_to_db()
                payment.save_to_db()
                EventRecorder.record(
                    nr_svc.user, Event.POST + f' [payment completed {payment_action}]', nr_model, nr_model.json()
                )

            else:
                # Record the event
                EventRecorder.record(
                    nr_svc.user, Event.POST + f' [payment created] {payment_action}', nr_model, nr_model.json()
                )

            # Wrap the response, providing info from both the SBC Pay response and the payment we created
            data = jsonify(
                {
                    'id': payment.id,
                    'nrId': payment.nrId,
                    'nrNum': nr_model.nrNum,
                    'token': payment.payment_token,
                    'statusCode': payment.payment_status_code,
                    'action': payment.payment_action,
                    'completionDate': payment.payment_completion_date,
                    'payment': payment.as_dict(),
                    'sbcPayment': payment_response.as_dict(),
                    'isPaymentActionRequired': payment_response.isPaymentActionRequired,
                }
            )

            response = make_response(data, 201)
            return response
        # something went wrong with status code above
        else:
            # log actual status code
            current_app.logger.error('Error with status code. Actual status code: ' + payment_response.statusCode)
            EventRecorder.record(
                nr_svc.user, Event.POST + f' [payment failed] {payment_action}', nr_model, nr_model.json()
            )
            # return generic error status to the front end
            return make_response(jsonify(message=f'Name Request {nr_id} encountered an error'), 402)
    except Exception as err:
        current_app.logger.error(err.with_traceback(None))
        EventRecorder.record(nr_svc.user, Event.POST + f' [payment failed] {payment_action}', nr_model, nr_model.json())
        return make_response(jsonify(message=f'Name Request {nr_id} encountered an error'), 500)


class PaymentNameRequestResource(AbstractNameRequestResource):
    """Name request payment resoure endpoint."""

    @staticmethod
    def approve_nr(nr, svc):
        """
        This method is for updating the name request when an active payment exists on the NR.
        :param nr:
        :param svc:
        :return:
        """
        # Update the names, we can ignore everything else as this is only
        # invoked when we're completing a payment
        nr = svc.map_request_names(nr)
        nr = svc.save_request(nr)
        # Return the updated name request
        return nr


@cors_preflight('GET')
@payment_api.route('/<int:nr_id>', strict_slashes=False, methods=['GET', 'OPTIONS'])
@payment_api.doc(params={})
class FindNameRequestPayments(PaymentNameRequestResource):
    """Find name request payments endpoints."""

    def get(self, nr_id):
        """Get endpoint."""
        try:
            nr_model = RequestDAO.query.get(nr_id)
            nr_payments = nr_model.payments.all()

            response_data = []
            # Wrap our payment
            for payment in nr_payments:
                if payment.payment_token:
                    payment_response = get_payment(payment.payment_token)
                    receipts = payment_response.receipts
                    if not receipts and payment_response.statusCode == PaymentState.APPROVED.value:
                        # generate temp receipts for approved payments
                        current_app.logger.debug('adding temporary receipt details.')
                        receipts = [
                            {
                                'id': payment.payment_token,
                                'receiptAmount': None,
                                'receiptDate': None,
                                'receiptNumber': 'Pending',
                            }
                        ]
                        payment_response.receipts = receipts
                        response_data.append(
                            {
                                'id': payment.id,
                                'nrId': payment.nrId,
                                'token': payment.payment_token,
                                'statusCode': payment.payment_status_code,
                                'action': payment.payment_action,
                                'completionDate': payment.payment_completion_date,
                                'payment': payment.as_dict(),
                                'sbcPayment': payment_response.as_dict(),
                                'receipts': receipts,
                            }
                        )
                    else:
                        # Wrap the response, providing info from both the SBC Pay response and the payment we created
                        response_data.append(
                            {
                                'id': payment.id,
                                'nrId': payment.nrId,
                                'token': payment.payment_token,
                                'statusCode': payment.payment_status_code,
                                'action': payment.payment_action,
                                'completionDate': payment.payment_completion_date,
                                'payment': payment.as_dict(),
                                'sbcPayment': payment_response.as_dict(),
                                'receipts': list(map(lambda r: map_receipt(r), receipts)),
                            }
                        )

            return make_response(jsonify(response_data), 200)
        except PaymentServiceError as err:
            return handle_exception(err, err.message, 500)
        except SBCPaymentException as err:
            return handle_exception(err, err.message, err.status_code)
        except SBCPaymentError as err:
            return handle_exception(err, err.message, 500)
        except Exception as err:
            return handle_exception(err, err, 500)


@cors_preflight('POST')
@payment_api.route('/<int:nr_id>/<string:payment_action>', strict_slashes=False, methods=['POST', 'OPTIONS'])
@payment_api.doc(params={})
class CreateNameRequestPayment(AbstractNameRequestResource):
    @staticmethod
    def _is_staff(auth_header):
        """Determine if the user is a staff member."""
        return auth_header and validate_roles(jwt, auth_header, [User.STAFF])

    @staticmethod
    def _affiliate_business_account(auth_header, business_account_id, nr_model):
        """Affiliate the new NR to the business account."""
        auth_svc_url = current_app.config.get('AUTH_SVC_URL')
        if not auth_svc_url:
            raise ValueError('AUTH_SVC_URL is not configured in the application.')

        nr_num = nr_model.nrNum
        phone_num = nr_model.applicants[0].phoneNumber
        auth_url = f'{auth_svc_url}/orgs/{business_account_id}/affiliations?newBusiness=true'
        headers = {'Authorization': auth_header, 'Content-Type': 'application/json'}
        payload = {'businessIdentifier': nr_num, 'phone': phone_num}

        try:
            response = requests.post(url=auth_url, json=payload, headers=headers)

            # Check the response status
            if not response.ok:
                current_app.logger.error(
                    f'Failed to affiliate business account {business_account_id} with {nr_num}. '
                    f'Status Code: {response.status_code}, Response: {response.text}'
                )
            else:
                current_app.logger.debug(
                    f'Successfully affiliated business account {business_account_id} with {nr_num}.'
                )
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f'Error affiliating business account {business_account_id} with {nr_num}: {e}')

    """Create name request payment endpoints."""

    @payment_api.expect(payment_request_schema)
    @payment_api.response(200, 'Success', '')
    @payment_api.doc(
        params={
            'nr_id': 'Name Request number',
            'payment_action': 'Payment NR Action - One of [CREATE, UPGRADE, REAPPLY, RESUBMIT]',
        }
    )
    def post(self, nr_id, payment_action=NameRequestActions.CREATE.value):
        """
        At this point, the Name Request will still be using a TEMPORARY NR number.
        Confirming the payment on the frontend triggers this endpoint. Here, we:
        - Create the payment via SBC Pay.
        - If payment creation is successful, create a corresponding payment record in our system.
        :param nr_id:
        :param payment_action:
        :return:
        """
        try:
            # Find the existing name request
            nr_model = RequestDAO.query.get(nr_id)
            # only used for adding namerequest service user to event recording
            nr_svc = self.nr_service
            if not nr_model:
                # Should this be a 400 or 404... hmmm
                return make_response(jsonify(message=f'Name Request {nr_id} not found'), 400)

            if not payment_action:
                return make_response(jsonify(message=f'Invalid payment action, {payment_action} not found'), 400)

            valid_payment_action = payment_action in [
                NameRequestActions.CREATE.value,
                NameRequestActions.UPGRADE.value,
                NameRequestActions.REAPPLY.value,
                NameRequestActions.RESUBMIT.value,
            ]

            if not valid_payment_action:
                return make_response(jsonify(message=f'Invalid payment action [{payment_action}]'), 400)

            # We only handle payments if the NR is in the following states
            valid_payment_states = [
                State.DRAFT,
                State.COND_RESERVE,
                State.RESERVED,
                State.CONDITIONAL,
                State.APPROVED,
                State.PENDING_PAYMENT,
            ]
            valid_nr_state = nr_model.stateCd in valid_payment_states
            if not valid_nr_state:
                return make_response(jsonify(message=f'Invalid NR state [{payment_action}]'), 400)

            json_input = request.get_json()
            headers = json_input.get('headers')
            auth_header = headers.get('Authorization')
            is_new_nr = False
            is_staff = self._is_staff(auth_header)

            if valid_payment_action and valid_nr_state:
                if payment_action in [NameRequestActions.CREATE.value, NameRequestActions.RESUBMIT.value]:
                    update_solr = True
                    nr_model = self.add_new_nr_number(nr_model, update_solr)
                    is_new_nr = True

            existing_payment = PaymentDAO.find_by_existing_nr_id(nr_id, payment_action)
            if existing_payment:
                # if we already have a payment record, we can request existing payment status and return it
                # get the payment status from Pay API
                if payment_action == PaymentDAO.PaymentActions.REAPPLY.value and is_reapplication_eligible(
                    nr_model.expirationDate
                ):
                    # skip valid cases of REAPPLY, as these potentially can have more than a single instance
                    pass
                else:
                    payment_response = get_payment(existing_payment.payment_token)
                    return handle_payment_response(
                        payment_action, payment_response, existing_payment, nr_id, nr_model, nr_svc
                    )

            payment_request = {}
            if not json_input:
                # return make_response(jsonify(message=MSG_BAD_REQUEST_NO_JSON_BODY), 400
                # Grab the data from the NR, if it exists
                payment_request = build_payment_request(nr_model)
            elif isinstance(json_input, dict):
                payment_request = merge_payment_request(nr_model, json_input)
            elif isinstance(json_input, str):
                payment_request = merge_payment_request(nr_model, json.loads(json_input))

            # Grab the info we need off the request
            payment_info = payment_request.get('paymentInfo', {})
            filing_info = payment_request.get('filingInfo')
            business_info = payment_request.get('businessInfo')
            details = payment_request.get('details')

            account_info = {}
            if folio_number := headers.pop('folioNumber', None):
                filing_info['folioNumber'] = folio_number

            if is_staff:
                if routing_slip_number := headers.get('routingSlipNumber'):
                    account_info['routingSlip'] = routing_slip_number
                    del headers['routingSlipNumber']

                if bcol_account_number := headers.get('bcolAccountNumber'):
                    account_info['bcolAccountNumber'] = bcol_account_number
                    del headers['bcolAccountNumber']

                if dat_number := headers.get('datNumber'):
                    account_info['datNumber'] = dat_number
                    del headers['datNumber']

                waive_fees = headers.get('waiveFees', False)
                filing_info.get('filingTypes')[0]['waiveFees'] = waive_fees
                if 'waiveFees' in headers:
                    del headers['waiveFees']

                # This is to support staff-payment-enabled switch to false in Launch Darkly
                if not account_info and not waive_fees:
                    headers = {}

            # Create our payment request
            req = PaymentRequest(
                paymentInfo=payment_info,
                filingInfo=filing_info,
                businessInfo=business_info,
                accountInfo=account_info,
                details=details,
            )

            # Save the payment info to Postgres
            payment = PaymentDAO()
            payment.nrId = nr_model.id
            payment.payment_action = payment_action
            # payment will be saved in handle_payment_response with a payment_token

            payment_response = create_payment(req.as_dict(), headers)
            payment_response_result = handle_payment_response(
                payment_action, payment_response, payment, nr_id, nr_model, nr_svc
            )
            # after a new NR saved
            # if logged in user is a staff, affiliate the new NR with the business_account_id
            if is_new_nr and is_staff:
                business_account_id = json_input.get('businessAccountId')
                if business_account_id:
                    current_app.logger.debug(
                        f'Affiliating to business account ID: {business_account_id} with {nr_model.nrNum}'
                    )
                    # affiliate the new NR to the account_info
                    # affiliate_business_account(business_account_id, nr_model.nrNum)
                    self._affiliate_business_account(auth_header, business_account_id, nr_model)

            return payment_response_result

        except PaymentServiceError as err:
            return handle_exception(err, err.message, 500)
        except SBCPaymentException as err:
            response = req.as_dict()
            response['errors'] = [err.message]
            return make_response(jsonify(response), err.status_code)
        except SBCPaymentError as err:
            return handle_exception(err, err.message, 500)
        except Exception as err:
            return handle_exception(err, err, 500)


@cors_preflight('DELETE, GET, PUT')
@payment_api.route(
    '/<int:nr_id>/payment/<string:payment_id>', strict_slashes=False, methods=['DELETE', 'GET', 'PUT', 'OPTIONS']
)
@payment_api.doc(params={'nr_id': '', 'payment_id': ''})
class NameRequestPayment(AbstractNameRequestResource):
    """Name request payment endpoints."""

    @payment_api.response(200, 'Success', '')
    # TODO: Update schema and marshal
    # @marshal_with(payment_response_schema)
    def get(self, nr_id, payment_id):
        """Get endpoint."""
        try:
            # Find the existing name request
            nr_model = RequestDAO.query.get(nr_id)

            if not nr_model:
                # Should this be a 400 or 404... hmmm
                return make_response(jsonify(message=f'{nr_id} not found'), 400)

            payment_id = int(clean_url_path_param(payment_id))
            payment = PaymentDAO.query.get(payment_id)

            payment_response = get_payment(payment.payment_token)
            receipts = payment_response.receipts
            data = []
            if not receipts and payment_response.statusCode == PaymentState.APPROVED.value:
                # generate temp receipts for approved payments
                current_app.logger.debug('adding temporary receipt details.')
                receipts = [
                    {
                        'id': payment.payment_token,
                        'receiptAmount': None,
                        'receiptDate': None,
                        'receiptNumber': 'Pending',
                    }
                ]
                payment_response.receipts = receipts
                data.append(
                    {
                        'id': payment.id,
                        'nrId': payment.nrId,
                        'token': payment.payment_token,
                        'statusCode': payment.payment_status_code,
                        'action': payment.payment_action,
                        'completionDate': payment.payment_completion_date,
                        'payment': payment.as_dict(),
                        'sbcPayment': payment_response.as_dict(),
                        'receipts': receipts,
                    }
                )
            else:
                # Wrap the response, providing info from both the SBC Pay response and the payment we created
                data.append(
                    {
                        'id': payment.id,
                        'nrId': payment.nrId,
                        'token': payment.payment_token,
                        'statusCode': payment.payment_status_code,
                        'action': payment.payment_action,
                        'completionDate': payment.payment_completion_date,
                        'payment': payment.as_dict(),
                        'sbcPayment': payment_response.as_dict(),
                        'receipts': list(map(lambda r: map_receipt(r), receipts)),
                    }
                )

            return make_response(jsonify(data), 200)

        except PaymentServiceError as err:
            return handle_exception(err, err.message, 500)
        except SBCPaymentException as err:
            return handle_exception(err, err.message, err.status_code)
        except SBCPaymentError as err:
            return handle_exception(err, err.message, 500)
        except Exception as err:
            return handle_exception(err, err, 500)

    def delete(self, nr_id, payment_id):
        """Delete endpoint."""
        try:
            # Find the existing name request
            nr_model = RequestDAO.query.get(nr_id)
            if not nr_model:
                return make_response(jsonify(message=f'No NR found with id: {nr_id}.'), 404)

            # Find the existing payment record
            payment = PaymentDAO.find_by_payment_token(payment_id)
            if not payment:
                return make_response(jsonify(message=f'No payment record with id: {payment_id}.'), 404)

            # check payment record state is CREATED
            current_payment_state = payment.payment_status_code
            if current_payment_state != PaymentStatusCode.CREATED.value:
                return make_response(
                    jsonify(message=f'Unable to cancel a payment record in {current_payment_state} state.'), 400
                )

            try:
                # cancelling may change with refactor
                cancel_payment(payment.payment_token)

                payment.payment_status_code = PaymentState.CANCELLED.value
                payment.save_to_db()
                nr_svc = self.nr_service
                EventRecorder.record(
                    nr_svc.user,
                    Event.DELETE + f' [payment cancelled] {payment.payment_action}',
                    nr_model,
                    nr_model.json(),
                )

                response_data = nr_model.json()
                # Add the list of valid Name Request actions for the given state to the response
                response_data['actions'] = get_nr_state_actions(nr_model.stateCd, nr_model)
                return make_response(jsonify(response_data), 200)

            except PaymentServiceError as err:
                # should only get here if there was a conflict (payment went through before cancel happened)
                return handle_exception(err, err.message, 409)
        except Exception as err:
            return handle_exception(err, repr(err), 500)


@cors_preflight('PATCH')
@payment_api.route(
    '/<int:nr_id>/payment/<int:payment_id>/<string:payment_action>', strict_slashes=False, methods=['PATCH', 'OPTIONS']
)
@payment_api.doc(
    params={
        'nr_id': 'NR Number - This field is required',
        'payment_action': 'Payment NR Action - One of [CREATE, UPGRADE, REAPPLY, REFUND]',
    }
)
class NameRequestPaymentAction(AbstractNameRequestResource):
    """Name request payment action endpoints."""

    # REST Method Handlers
    def patch(self, nr_id, payment_id, payment_action):
        """
        :param nr_id:
        :param payment_id:
        :param payment_action:
        :return:
        """
        try:
            # Find the existing name request
            nr_model = RequestDAO.query.get(nr_id)

            # Creates a new NameRequestService, validates the app config, and sets request_data to the NameRequestService instance
            # Override the default self.initialize method
            def initialize(_self):
                # The request payload will be empty when making this call,
                # but we still want to process names, so we need to add
                # them to the request, otherwise they won't be processed!
                _self.request_data = {'names': [n.as_dict() for n in nr_model.names]}
                # Set the request data to the service
                _self.nr_service.request_data = self.request_data

            initialize(self)
            nr_svc = self.nr_service
            nr_svc.nr_num = nr_model.nrNum
            nr_svc.nr_id = nr_model.id

            valid_update_states = [State.DRAFT, State.COND_RESERVE, State.RESERVED, State.PENDING_PAYMENT]

            # This could be moved out, but it's fine here for now
            def validate_patch_request(nr):
                is_valid = True
                msg = ''
                if nr.stateCd in valid_update_states:
                    is_valid = True

                return is_valid, msg

            is_valid_patch, validation_msg = validate_patch_request(nr_model)
            validation_msg = validation_msg if not len(validation_msg) > 0 else 'Invalid request for PATCH'

            if not is_valid_patch:
                raise PaymentServiceError(message=validation_msg)

            process_payment = has_active_payment(nr_model, payment_id)
            if nr_model.stateCd in valid_update_states and not process_payment:
                pass
            elif process_payment:
                # This handles updates if the NR state is 'patchable'
                nr_model = self.handle_payment_actions(payment_action, nr_model, payment_id)

            current_app.logger.debug(nr_model.json())
            response_data = nr_model.json()
            # Add the list of valid Name Request actions for the given state to the response
            response_data['actions'] = nr_svc.current_state_actions
            return make_response(jsonify(response_data), 200)
        except PaymentServiceError as err:
            return handle_exception(err, err.message, 500)
        except Exception as err:
            return handle_exception(err, repr(err), 500)

    def handle_payment_actions(self, action, model: RequestDAO, payment_id: int):
        """Handle payment actions."""
        return {
            NameRequestActions.CREATE.value: self.complete_reservation_payment,
            NameRequestActions.RESUBMIT.value: self.complete_reservation_payment,
            NameRequestActions.UPGRADE.value: self.complete_upgrade_payment,
            NameRequestActions.REAPPLY.value: self.complete_reapply_payment,
            NameRequestActions.REQUEST_REFUND.value: self.request_refund,
            NameRequestActions.CANCEL.value: self.cancel_payment,
        }.get(action)(model, payment_id)

    def complete_reservation_payment(self, nr_model: RequestDAO, payment_id: int):
        """
        Invoked when completing an in-progress Name Request reservation.
        :param nr_model:
        :param payment_id:
        :return:
        """
        nr_svc = self.nr_service

        # Update the state of the payment
        payment = get_active_payment(nr_model, payment_id)
        sbc_payment_response = get_payment(payment.payment_token)

        # TODO: Throw errors if this fails!
        if sbc_payment_response.statusCode in [PaymentStatusCode.COMPLETED.value, PaymentStatusCode.APPROVED.value]:
            payment.payment_status_code = sbc_payment_response.statusCode
            payment.payment_completion_date = sbc_payment_response.createdOn
            payment.save_to_db()

            # This handles updates if the NR state is DRAFT, COND_RESERVE or RESERVED
            # If the state is COND_RESERVE update state to CONDITIONAL
            # If the state is RESERVED update state to APPROVED
            # Then update the name request as required

            if nr_model.stateCd == State.DRAFT:
                # If the state is DRAFT, leave it as a DRAFT
                nr_model = self.update_nr(nr_model, State.DRAFT, self.handle_nr_approve)
            if nr_model.stateCd == State.COND_RESERVE:
                # If the state is COND_RESERVE update state to CONDITIONAL, and update the name request as required
                nr_model = self.update_nr(nr_model, State.CONDITIONAL, self.handle_nr_approve)
            elif nr_model.stateCd == State.RESERVED:
                # If the state is RESERVED update state to APPROVED, and update the name request as required
                nr_model = self.update_nr(nr_model, State.APPROVED, self.handle_nr_approve)

            # Save the name request
            nr_model.save_to_db()

            # Record the event
            EventRecorder.record(nr_svc.user, Event.PATCH + ' [payment completed] RESERVE', nr_model, nr_model.json())

        # Update the actions, as things change once the payment is successful
        self.nr_service.current_state_actions = get_nr_state_actions(nr_model.stateCd, nr_model)

        return nr_model

    def complete_upgrade_payment(self, nr_model: RequestDAO, payment_id: int):
        """
        Invoked when upgrading an existing Name Request reservation to PRIORITY status.
        :param nr_model:
        :param payment_id:
        :return:
        """
        nr_svc = self.nr_service

        if nr_model.stateCd not in [State.DRAFT, State.PENDING_PAYMENT]:
            raise PaymentServiceError(message='Error upgrading Name Request, request is in an invalid state!')

        # Update the state of the payment
        payment = get_active_payment(nr_model, payment_id)
        sbc_payment_response = get_payment(payment.payment_token)

        # TODO: Throw errors if this fails!
        if sbc_payment_response.statusCode in [PaymentStatusCode.COMPLETED.value, PaymentStatusCode.APPROVED.value]:
            payment.payment_status_code = sbc_payment_response.statusCode
            payment.payment_completion_date = sbc_payment_response.createdOn
            payment.save_to_db()

            nr_model.priorityCd = 'Y'
            nr_model.priorityDate = datetime.utcnow()

            # Save the name request
            nr_model.save_to_db()

        # Update the actions, as things change once the payment is successful
        self.nr_service.current_state_actions = get_nr_state_actions(nr_model.stateCd, nr_model)

        # Record the event
        EventRecorder.record(nr_svc.user, Event.PATCH + ' [payment completed] UPGRADE', nr_model, nr_model.json())

        return nr_model

    def complete_reapply_payment(self, nr_model: RequestDAO, payment_id: int):
        """
        Invoked when re-applying for an existing Name Request reservation.
        Extend the Name Request's expiration date by 56 days.
        If the request action is set to REH, REN or REST, OR request type is
        'RCR', 'RUL', 'BERE', 'RCC', 'RCP', 'RFI', 'XRCR', 'RLC', 'XRCP','RSO','XRSO'
        extend the expiration by an additional year (plus the default 56 days).
        :param nr_model:
        :param payment_id:
        :return:
        """
        nr_svc = self.nr_service

        # Update the state of the payment
        payment = get_active_payment(nr_model, payment_id)
        sbc_payment_response = get_payment(payment.payment_token)

        # TODO: Throw errors if this fails!
        if sbc_payment_response.statusCode in [PaymentStatusCode.COMPLETED.value, PaymentStatusCode.APPROVED.value]:
            payment.payment_status_code = sbc_payment_response.statusCode
            payment.payment_completion_date = sbc_payment_response.createdOn
            payment.save_to_db()

            if nr_model.submitCount < 3:
                nr_model = nr_svc.extend_expiry_date(nr_model, datetime.utcnow())
                nr_model = nr_svc.update_request_submit_count(nr_model)
                nr_model.save_to_db()
            else:
                # TODO: Make a custom exception for this?
                raise PaymentServiceError(message='Submit count maximum of 3 retries has been reached!')

        # Update the actions, as things change once the payment is successful
        self.nr_service.current_state_actions = get_nr_state_actions(nr_model.stateCd, nr_model)

        # Record the event
        EventRecorder.record(nr_svc.user, Event.PATCH + ' [payment completed] REAPPLY', nr_model, nr_model.json())

        return nr_model

    def request_refund(self, nr_model: RequestDAO, payment_id: int):
        """
        Processes a SINGLE refund request.
        This is different from the 'refund' in the NameRequest resource PATCH namerequests/{nrId}/REQUEST_REFUND
        which cancels the NR and refunds any associated payments.
        :param nr_model:
        :param payment_id:
        :return:
        """
        # Handle the payments
        valid_states = [PaymentState.APPROVED.value, PaymentState.COMPLETED.value, PaymentState.PARTIAL.value]
        if nr_model.stateCd not in [State.DRAFT]:
            raise PaymentServiceError(message='Invalid NR state for cancel and refund')
        # Cancel any payments associated with the NR
        for payment in nr_model.payments.all():
            if payment.payment_status_code in valid_states and payment.id == payment_id:
                # refund_payment(payment.payment_token, {'reason': 'Name Request user requested refund'})
                refund_payment(payment.payment_token, {})
                payment.payment_status_code = PaymentState.REFUND_REQUESTED.value
                payment.save_to_db()
                nr_svc = self.nr_service
                EventRecorder.record(
                    nr_svc.user,
                    Event.PATCH + f' [payment refunded] {payment.payment_action}',
                    nr_model,
                    nr_model.json(),
                )

        return nr_model

    def cancel_payment(self, nr_model: RequestDAO, payment_id: int):
        """Cancel payment with specified id."""
        valid_states = [PaymentState.CREATED.value]
        for payment in nr_model.payments.all():
            if payment.id == payment_id and payment.payment_status_code in valid_states:
                sbc_payment_response = get_payment(payment.payment_token)
                if sbc_payment_response.statusCode in [
                    PaymentStatusCode.COMPLETED.value,
                    PaymentStatusCode.APPROVED.value,
                ]:
                    raise PaymentServiceError(message='Error cancelling payment. Payment is in a completed state!')
                cancel_payment(payment.payment_token)
                payment.payment_status_code = PaymentState.CANCELLED.value
                payment.save_to_db()
                # record the event
                nr_svc = self.nr_service
                EventRecorder.record(
                    nr_svc.user,
                    Event.DELETE + f' [payment cancelled] {payment.payment_action}',
                    nr_model,
                    nr_model.json(),
                )
        return nr_model
