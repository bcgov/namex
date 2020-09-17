from flask import request, make_response, jsonify
from flask_restplus import Resource, cors, fields, marshal_with, marshal
from flask_jwt_oidc import AuthError

from urllib.parse import unquote_plus

from namex.utils.logging import setup_logging
from namex.utils.auth import cors_preflight
from namex.utils.api_resource import clean_url_path_param, handle_exception

from namex.services.payment.transactions import \
    get_transactions, get_transaction, create_transaction, update_transaction, \
    GetTransactionsRequest, GetTransactionRequest, CreateTransactionRequest, UpdateTransactionRequest

from .api_namespace import api as payment_api

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


@payment_api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@cors_preflight('GET')
@payment_api.route('/<string:payment_identifier>/transactions', strict_slashes=False, methods=['GET', 'OPTIONS'])
@payment_api.doc(params={
    'payment_identifier': ''
})
class PaymentTransactions(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @payment_api.response(200, 'Success', '')
    # @marshal_with()
    def get(payment_identifier):
        payment_identifier = clean_url_path_param(payment_identifier)

        req = GetTransactionsRequest(
            payment_identifier=payment_identifier
        )

        transactions = get_transactions(req)

        if not transactions:
            return

        data = jsonify(transactions.to_dict())
        response = make_response(data, 200)
        return response


@cors_preflight('GET, POST, PUT')
@payment_api.route('/<string:payment_identifier>/transaction', strict_slashes=False, methods=['GET', 'POST', 'PUT', 'OPTIONS'])
class PaymentTransaction(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @payment_api.response(200, 'Success', '')
    # @marshal_with()
    @payment_api.doc(params={
        'receipt_number': '',
        'transaction_identifier': ''
    })
    def get(payment_identifier):
        payment_identifier = clean_url_path_param(payment_identifier)
        receipt_number = unquote_plus(request.args.get('receipt_number').strip()) if request.args.get('receipt_number') else None
        transaction_identifier = unquote_plus(request.args.get('transaction_identifier').strip()) if request.args.get('transaction_identifier') else None

        req = GetTransactionRequest(
            payment_identifier=payment_identifier,
            receipt_number=receipt_number,
            transaction_identifier=transaction_identifier
        )

        transaction = get_transaction(req)

        if not transaction:
            return

        data = jsonify(transaction.to_dict())
        response = make_response(data, 200)
        return response

    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @payment_api.expect()
    @payment_api.response(200, 'Success', '')
    # @marshal_with()
    @payment_api.doc(params={
        'redirect_uri': ''
    })
    def post(payment_identifier):
        payment_identifier = clean_url_path_param(payment_identifier)
        redirect_uri = unquote_plus(request.args.get('redirect_uri').strip()) if request.args.get('redirect_uri') else None

        req = CreateTransactionRequest(
            payment_identifier=payment_identifier,
            redirect_uri=redirect_uri
        )

        transaction = create_transaction(req)

        data = jsonify(transaction.to_dict())
        response = make_response(data, 200)
        return response

    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @payment_api.expect()
    @payment_api.response(200, 'Success', '')
    # @marshal_with()
    @payment_api.doc(params={
        'receipt_number': '',
        'transaction_identifier': ''
    })
    def put(payment_identifier):
        payment_identifier = clean_url_path_param(payment_identifier)

        json_input = request.get_json()
        if not json_input:
            return jsonify(message=MSG_BAD_REQUEST_NO_JSON_BODY), 400

        receipt_number = json_input.get('receipt_number', None)
        transaction_identifier = json_input.get('transaction_identifier', None)

        req = UpdateTransactionRequest(
            payment_identifier=payment_identifier,
            receipt_number=receipt_number,
            transaction_identifier=transaction_identifier
        )

        transaction = update_transaction(req)

        data = jsonify(transaction.to_dict())
        response = make_response(data, 200)
        return response
