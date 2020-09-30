import json

from datetime import datetime
from dateutil.relativedelta import relativedelta

from flask import current_app, request, make_response, jsonify
from flask_restplus import cors, fields
from flask_jwt_oidc import AuthError

from namex.utils.logging import setup_logging
from namex.utils.auth import cors_preflight
from namex.utils.api_resource import clean_url_path_param, handle_exception

from namex.constants import PaymentState, PaymentStatusCode, RequestAction, NameRequestActions
from namex.models import Request as RequestDAO, Payment as PaymentDAO, State, Event

from namex.resources.name_requests.abstract_nr_resource import AbstractNameRequestResource

from namex.services import EventRecorder
from namex.services.name_request.name_request_state import get_nr_state_actions
from namex.services.payment.exceptions import SBCPaymentException, SBCPaymentError, PaymentServiceError
from namex.services.payment.payments import get_payment, create_payment, update_payment
from namex.services.name_request.utils import has_active_payment, get_active_payment

from .api_namespace import api as payment_api
from .utils import build_payment_request, merge_payment_request

from openapi_client.models import PaymentRequest

setup_logging()  # It's important to do this first

MSG_BAD_REQUEST_NO_JSON_BODY = 'No JSON data provided'
MSG_SERVER_ERROR = 'Server Error!'
MSG_NOT_FOUND = 'Resource not found'
MSG_ERROR_CREATING_RESOURCE = 'Could not create / update resource'


def validate_request(request):
    return True


# Define our DTO models
# Generic model types
dictionary_list_model = payment_api.model('DictionaryList', {
    'key': fields.String,
    'list': fields.List(fields.String)
})

dict_list_model = payment_api.model('DictionaryListList', {
    'data': fields.List(fields.Nested(dictionary_list_model))
})

list_model = payment_api.model('List', {
    'data': fields.List(fields.String)
})

string_model = payment_api.model('String', {
    'data': fields.String
})

# Custom model types
payment_info_schema = payment_api.model('PaymentInfo', {
    'methodOfPayment': fields.String
})

filing_type_schema = payment_api.model('FilingType', {
    'filingTypeCode': fields.String,
    'priority': fields.Boolean,
    'filingDescription': fields.String
})

filing_info_schema = payment_api.model('FilingInfo', {
    'corpType': fields.String,
    'date': fields.String,
    'filingTypes': fields.List(fields.Nested(filing_type_schema)),
})

contact_info_schema = payment_api.model('ContactInfo', {
    # 'firstName': fields.String,
    # 'lastName': fields.String,
    'addressLine1': fields.String,
    'city': fields.String,
    'province': fields.String,
    'country': fields.String,
    'postalCode': fields.String,
})

business_info_schema = payment_api.model('BusinessInfo', {
    'businessIdentifier': fields.String,
    'businessName': fields.String,
    'contactInfo': fields.Nested(contact_info_schema)
})


payment_invoice_schema = payment_api.model('PaymentInvoice', {
    'id': fields.String,
    'referenceNumber': fields.String,
    'statusCode': fields.String,
    'createdBy': fields.String,
    'createdOn': fields.String
})

payment_response_schema = payment_api.model('Payment', {
    'id': fields.String,
    'invoices': fields.List(fields.Nested(payment_invoice_schema)),
    'paymentMethod': fields.String,
    'statusCode': fields.String,
    'createdBy': fields.String,
    'createdOn': fields.String,
    'updatedBy': fields.String,
    'updatedOn': fields.String
})

# Define our request objects
# These are POSTED use camelCase
payment_request_schema = payment_api.model('PaymentRequest', {
    'paymentInfo': fields.Nested(payment_info_schema),
    'businessInfo': fields.Nested(business_info_schema),
    'filingInfo': fields.Nested(filing_info_schema)
})


@payment_api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@cors_preflight('GET, POST')
@payment_api.route('/<int:nr_id>', strict_slashes=False, methods=['GET', 'POST', 'OPTIONS'])
@payment_api.doc(params={
})
class NameRequestPayments(AbstractNameRequestResource):
    @cors.crossdomain(origin='*')
    def get(self, nr_id):
        try:
            nr_model = RequestDAO.query.get(nr_id)
            nr_payments = nr_model.payments.all()

            response_data = []
            # Wrap our payment
            for payment in nr_payments:
                payment_response = get_payment(payment.payment_token)

                if not payment_response:
                    return None
                    # TODO: Maybe throw an error here?

                # Wrap the response, providing info from both the SBC Pay response and the payment we created
                response_data.append({
                    'id': payment.id,
                    'nrId': payment.nrId,
                    'token': payment.payment_token,
                    'statusCode': payment.payment_status_code,
                    'completionDate': payment.payment_completion_date,
                    'payment': payment.as_dict(),
                    'sbcPayment': payment_response.to_dict()
                })

            return jsonify(response_data), 200
        except PaymentServiceError as err:
            return handle_exception(err, err.message, 500)
        except SBCPaymentException as err:
            return handle_exception(err, err.message, err.status_code)
        except SBCPaymentError as err:
            return handle_exception(err, err.message, 500)
        except Exception as err:
            return handle_exception(err, err, 500)

    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @payment_api.expect(payment_request_schema)
    @payment_api.response(200, 'Success', '')
    # @marshal_with()
    @payment_api.doc(params={
        'nr_id': 'Name Request number'
    })
    def post(self, nr_id):
        """
        At this point, the Name Request will still be using a TEMPORARY NR number.
        Confirming the payment on the frontend triggers this endpoint. Here, we:
        - Save the request to NRO which gives us a real NR.
        - Create the payment via SBC Pay.
        - If payment creation is successful, create a corresponding payment record in our system.
        :param nr_id:
        :return:
        """
        try:
            # Find the existing name request
            nr_model = RequestDAO.query.get(nr_id)

            if not nr_model:
                # Should this be a 400 or 404... hmmm
                return None, None, jsonify(message='{nr_id} not found'.format(nr_id=nr_id)), 400

            # Save back to NRO to get the updated NR Number
            update_solr = False
            nr_model = self.update_records_in_network_services(nr_model, update_solr)

            json_input = request.get_json()
            payment_request = {}
            if not json_input:
                # return jsonify(message=MSG_BAD_REQUEST_NO_JSON_BODY), 400
                # Grab the data from the NR, if it exists
                payment_request = build_payment_request(nr_model)
            elif isinstance(json_input, dict):
                payment_request = merge_payment_request(nr_model, json_input)
            elif isinstance(json_input, str):
                payment_request = merge_payment_request(nr_model, json.loads(json_input))

            # Grab the info we need off the request
            payment_info = payment_request.get('paymentInfo')
            filing_info = payment_request.get('filingInfo')
            business_info = payment_request.get('businessInfo')

            # Create our payment request
            req = PaymentRequest(
                payment_info=payment_info,
                filing_info=filing_info,
                business_info=business_info
            )

            payment_response = create_payment(req)

            if not payment_response:
                raise PaymentServiceError(message=MSG_ERROR_CREATING_RESOURCE)

            if payment_response and payment_response.status_code == PaymentStatusCode.CREATED.value:
                # Save the payment info to Postgres
                payment = PaymentDAO()
                payment.nrId = nr_model.id
                payment.payment_token = str(payment_response.id)
                payment.payment_completion_date = payment_response.created_on
                payment.payment_status_code = PaymentState.CREATED.value
                payment.save_to_db()

                # Wrap the response, providing info from both the SBC Pay response and the payment we created
                data = jsonify({
                    'id': payment.id,
                    'nrId': payment.nrId,
                    'token': payment.payment_token,
                    'statusCode': payment.payment_status_code,
                    'completionDate': payment.payment_completion_date,
                    'payment': payment.as_dict(),
                    'sbcPayment': payment_response.to_dict()
                })

                # Record the event
                nr_svc = self.nr_service
                # EventRecorder.record(nr_svc.user, Event.PATCH + ' [payment ID: {id}]'.format(id=payment.id), nr_model, data)

                response = make_response(data, 201)
                return response

        except PaymentServiceError as err:
            return handle_exception(err, err.message, 500)
        except SBCPaymentException as err:
            return handle_exception(err, err.message, err.status_code)
        except SBCPaymentError as err:
            return handle_exception(err, err.message, 500)
        except Exception as err:
            return handle_exception(err, err, 500)


@cors_preflight('GET, PUT')
@payment_api.route('/<int:nr_id>/payment/<string:payment_id>', strict_slashes=False, methods=['GET', 'PUT', 'OPTIONS'])
@payment_api.doc(params={
    'nr_id': '',
    'payment_id': ''
})
class NameRequestPayment(AbstractNameRequestResource):
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @payment_api.response(200, 'Success', '')
    # @marshal_with(payment_response_schema)
    def get(self, nr_id, payment_id):
        try:
            # Find the existing name request
            nr_model = RequestDAO.query.get(nr_id)

            if not nr_model:
                # Should this be a 400 or 404... hmmm
                return None, None, jsonify(message='{nr_id} not found'.format(nr_id=nr_id)), 400

            payment_id = int(clean_url_path_param(payment_id))
            payment = PaymentDAO.query.get(payment_id)

            payment_response = get_payment(payment.payment_token)

            if not payment_response:
                return jsonify(message=MSG_NOT_FOUND), 404  # TODO: What if we have a record?

            # Wrap the response, providing info from both the SBC Pay response and the payment we created
            data = jsonify({
                'id': payment.id,
                'nrId': payment.nrId,
                'token': payment.payment_token,
                'statusCode': payment.payment_status_code,
                'completionDate': payment.payment_completion_date,
                'payment': payment.as_dict(),
                'sbcPayment': payment_response.to_dict()
            })

            response = make_response(data, 200)
            return response

        except PaymentServiceError as err:
            return handle_exception(err, err.message, 500)
        except SBCPaymentException as err:
            return handle_exception(err, err.message, err.status_code)
        except SBCPaymentError as err:
            return handle_exception(err, err.message, 500)
        except Exception as err:
            return handle_exception(err, err, 500)

    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @payment_api.expect(payment_request_schema)
    @payment_api.response(200, 'Success', '')
    # @marshal_with()
    def put(self, nr_id, payment_id):
        try:
            # Find the existing name request
            nr_model = RequestDAO.query.get(nr_id)

            if not nr_model:
                # Should this be a 400 or 404... hmmm
                return None, None, jsonify(message='{nr_id} not found'.format(nr_id=nr_id)), 400

            payment_id = clean_url_path_param(payment_id)

            json_input = request.get_json()
            if not json_input:
                return jsonify(message=MSG_BAD_REQUEST_NO_JSON_BODY), 400

            # Grab the info we need off the request
            payment_info = json_input.get('paymentInfo')
            filing_info = json_input.get('filingInfo')
            business_info = json_input.get('businessInfo')

            # Update our payment request
            req = PaymentRequest(
                payment_info=payment_info,
                filing_info=filing_info,
                business_info=business_info
            )

            payment_response = update_payment(payment_id, req)
            if not payment_response:
                raise PaymentServiceError(message=MSG_ERROR_CREATING_RESOURCE)

            data = jsonify(payment_response.to_dict())
            response = make_response(data, 200)
            return response

        except PaymentServiceError as err:
            return handle_exception(err, err.message, 500)
        except SBCPaymentException as err:
            return handle_exception(err, err.message, err.status_code)
        except SBCPaymentError as err:
            return handle_exception(err, err.message, 500)
        except Exception as err:
            return handle_exception(err, err, 500)


@cors_preflight('PATCH')
@payment_api.route('/<int:nr_id>/payment/<int:payment_id>/<string:payment_action>', strict_slashes=False, methods=['PATCH', 'OPTIONS'])
@payment_api.doc(params={
    'nr_id': 'NR Number - This field is required',
    'payment_action': 'Payment NR Action - One of [COMPLETE, UPGRADE, REAPPLY, REFUND]'
})
class NameRequestPaymentAction(AbstractNameRequestResource):
    # REST Method Handlers
    @cors.crossdomain(origin='*')
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
            nr_svc = self.nr_service

            nr_svc.nr_num = nr_model.nrNum
            nr_svc.nr_id = nr_model.id

            valid_update_states = [State.DRAFT, State.COND_RESERVE, State.RESERVED]

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
            return jsonify(response_data), 200
        except PaymentServiceError as err:
            return handle_exception(err, err.message, 500)
        except Exception as err:
            return handle_exception(err, repr(err), 500)

    def handle_payment_actions(self, action, model, payment_id):
        return {
            NameRequestActions.COMPLETE.value: self.complete_reservation_payment,
            NameRequestActions.UPGRADE.value: self.complete_upgrade_payment,
            NameRequestActions.REAPPLY.value: self.complete_reapply_payment,
            NameRequestActions.REFUND.value: self.complete_refund
        }.get(action)(model, payment_id)

    def complete_reservation_payment(self, nr_model, payment_id):
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
        if sbc_payment_response.status_code == PaymentStatusCode.COMPLETED.value:
            payment.payment_status_code = PaymentState.COMPLETED.value
            payment.payment_completion_date = sbc_payment_response.created_on
            payment.save_to_db()

            # Use apply_state_change to change state, as it enforces the State change pattern
            # apply_state_change takes the model, updates it to the specified state, and executes the callback handler

            # This handles updates if the NR state is DRAFT, COND_RESERVE or RESERVED
            # If the state is COND_RESERVE update state to CONDITIONAL
            # If the state is RESERVED update state to APPROVED
            # Then update the name request as required

            if nr_model.stateCd == State.DRAFT:
                # If the state is DRAFT, leave it as a DRAFT
                nr_model = nr_svc.apply_state_change(nr_model, State.DRAFT, self.handle_nr_approval)
            if nr_model.stateCd == State.COND_RESERVE:
                # If the state is COND_RESERVE update state to CONDITIONAL, and update the name request as required
                nr_model = nr_svc.apply_state_change(nr_model, State.CONDITIONAL, self.handle_nr_approval)
            elif nr_model.stateCd == State.RESERVED:
                # If the state is RESERVED update state to APPROVED, and update the name request as required
                nr_model = nr_svc.apply_state_change(nr_model, State.APPROVED, self.handle_nr_approval)

            # This handles the updates for NRO and Solr, if necessary
            self.update_records_in_network_services(nr_model)

            # Record the event
            # EventRecorder.record(nr_svc.user, Event.PATCH + ' [payment ID: {id}]'.format(id=payment_id), nr_model, nr_svc.request_data)

        return nr_model

    def complete_upgrade_payment(self, nr_model, payment_id=None):
        """
        Invoked when upgrading an existing Name Request reservation to PRIORITY status.
        :param nr_model:
        :param payment_id:
        :return:
        """
        nr_svc = self.nr_service

        if not nr_model.stateCd == State.DRAFT:
            raise PaymentServiceError(message='Error upgrading Name Request, request is in an invalid state!')

        # This handles updates if the NR state is 'patchable'
        nr_model = self.update_nr_fields(nr_model, nr_model.stateCd)

        nr_model.priorityCd = 'Y'
        nr_model.priorityDate = datetime.utcnow()

        # Save the name request
        nr_model.save_to_db()

        # Update the actions, as things change once the payment is successful
        self.nr_service.current_state_actions = get_nr_state_actions(nr_model.stateCd, nr_model)
        # We have not accounted for multiple payments.
        # We will need to add a request_payment model (request_id and payment_id)
        # This handles the updates for NRO and Solr, if necessary
        update_solr = True
        nr_model = self.update_records_in_network_services(nr_model, update_solr)

        # Record the event
        # EventRecorder.record(nr_svc.user, Event.PATCH + ' [upgrade]', nr_model, nr_svc.request_data)

        return nr_model

    def complete_reapply_payment(self, nr_model, payment_id=None):
        """
        Invoked when re-applying for an existing Name Request reservation.
        Extend the Name Request's expiration date by 56 days. If the request action is set to REH or REST,
        extend the expiration by an additional year (plus the default 56 days).
        :param nr_model:
        :return:
        """
        nr_svc = self.nr_service

        if nr_model.submitCount < 3:
            if nr_model.request_action_cd in [RequestAction.REH.value, RequestAction.REN.value]:
                # If request action is REH or REST extend by 1 year (+ 56 default) days
                nr_model = nr_svc.extend_expiry_date(nr_model, (datetime.utcnow() + relativedelta(years=1, days=56)))
                nr_model = nr_svc.update_request_submit_count(nr_model)
            else:
                # Extend expiry date by (default) 56 days
                nr_model = nr_svc.extend_expiry_date(nr_model, datetime.utcnow())
                nr_model = nr_svc.update_request_submit_count(nr_model)

            # This handles updates if the NR state is 'patchable'
            # nr_model = self.update_nr_fields(nr_model, nr_model.stateCd)

            # This handles the updates for NRO and Solr, if necessary
            update_solr = True
            nr_model = self.update_records_in_network_services(nr_model, update_solr)

            # Record the event
            # EventRecorder.record(nr_svc.user, Event.PATCH + ' [re-apply]', nr_model, nr_svc.request_data)
        else:
            # TODO: Make a custom exception for this?
            raise PaymentServiceError(message='Submit count maximum of 3 retries has been reached!')

        return nr_model

    def complete_refund(self, nr_model, payment_id=None):
        nr_svc = self.nr_service

        # This handles updates if the NR state is 'patchable'
        # nr_model = self.update_nr_fields(nr_model, nr_model.stateCd)

        # This handles the updates for NRO and Solr, if necessary
        update_solr = True
        nr_model = self.update_records_in_network_services(nr_model, update_solr)

        # Record the event
        # EventRecorder.record(nr_svc.user, Event.PATCH, nr_model, nr_svc.request_data)

        return nr_model
