import json

from flask import request, make_response, jsonify
from flask_restplus import Resource, cors, fields, marshal_with, marshal
from flask_jwt_oidc import AuthError

from namex.utils.logging import setup_logging
from namex.utils.auth import cors_preflight
from namex.utils.api_resource import clean_url_path_param, handle_exception

from namex.constants import PaymentState, PaymentStatusCode

from namex.models import Request as RequestDAO, Payment as PaymentDAO

from namex.services.payment.exceptions import SBCPaymentException, SBCPaymentError, PaymentServiceError
from namex.services.payment.payments import get_payment, create_payment, update_payment, CreatePaymentRequest, UpdatePaymentRequest

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


@cors_preflight('GET, PUT')
@payment_api.route('/<string:payment_identifier>', strict_slashes=False, methods=['GET', 'PUT', 'OPTIONS'])
@payment_api.doc(params={
    'payment_identifier': ''
})
class Payment(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @payment_api.response(200, 'Success', '')
    # @marshal_with(payment_response_schema)
    def get(payment_identifier):
        try:
            payment_identifier = clean_url_path_param(payment_identifier)

            payment = get_payment(payment_identifier)

            if not payment:
                return jsonify(message=MSG_NOT_FOUND), 404

            data = jsonify(payment.to_dict())
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

    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @payment_api.expect(payment_request_schema)
    @payment_api.response(200, 'Success', '')
    # @marshal_with()
    def put(payment_identifier):
        try:
            payment_identifier = clean_url_path_param(payment_identifier)

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

            payment_response = update_payment(payment_identifier, req)
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


@cors_preflight('DELETE')
@payment_api.route('/extra', strict_slashes=False, methods=['DELETE', 'OPTIONS'])
class Extra(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @payment_api.expect()
    @payment_api.response(200, 'Success', '')
    # @marshal_with()
    @payment_api.doc(params={
        '': ''
    })
    def delete():
        pass


@cors_preflight('GET')
@payment_api.route('/<int:nr_id>/payments', strict_slashes=False, methods=['GET', 'OPTIONS'])
@payment_api.doc(params={
    'nr_id': 'NR Number - This field is required'
})
class NameRequestPayment(Resource):
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


@cors_preflight('GET, POST')
@payment_api.route('/<int:nr_id>', strict_slashes=False, methods=['POST', 'OPTIONS'])
@payment_api.doc(params={
})
class NameRequestPayments(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @payment_api.expect(payment_request_schema)
    @payment_api.response(200, 'Success', '')
    # @marshal_with()
    @payment_api.doc(params={
        'nr_id': 'Name Request number'
    })
    def post(nr_id):
        try:
            # Find the existing name request
            nr_model = RequestDAO.query.get(nr_id)

            if not nr_model:
                # Should this be a 400 or 404... hmmm
                return None, None, jsonify(message='{nr_id} not found'.format(nr_id=nr_id)), 400

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
class NameRequestPayment(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @payment_api.response(200, 'Success', '')
    # @marshal_with(payment_response_schema)
    def get(nr_id, payment_id):
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

    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @payment_api.expect(payment_request_schema)
    @payment_api.response(200, 'Success', '')
    # @marshal_with()
    def put(nr_id, payment_id):
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
