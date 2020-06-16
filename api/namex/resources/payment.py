from flask import request, make_response, jsonify
from flask_restplus import Namespace, Resource, cors, fields, marshal_with, marshal
from flask_jwt_oidc import AuthError

from namex.utils.logging import setup_logging
from namex.utils.util import cors_preflight

from urllib.parse import unquote_plus

import json

from namex.services.payment.fees import calculate_fees, CalculateFeesRequest

from namex.services.payment.invoices import get_invoices, get_invoice

from namex.services.payment.payments import get_payment, create_payment, update_payment

from namex.services.payment.receipts import get_receipt

from namex.services.payment.transactions import \
    get_transactions, get_transaction, create_transaction, update_transaction, \
    GetTransactionsRequest, GetTransactionRequest, CreateTransactionRequest, UpdateTransactionRequest

from openapi_client.models import PaymentRequest

setup_logging()  # It's important to do this first

# Register a local namespace for the NR reserve
payment_api = Namespace('payments', description='Payment API - Uses Service BC Pay')


def validate_request(request):
    return True


dictionary_list = payment_api.model('DictionaryList', {
    'key': fields.String,
    'list': fields.List(fields.String)
})

# Define our response object
response_dict_list = payment_api.model('ResponseDictionaryList', {
    'data': fields.List(fields.Nested(dictionary_list))
})

# Define our response object
response_list = payment_api.model('List', {
    'data': fields.List(fields.String)
})

# Define our response object
response_string = payment_api.model('String', {
    'data': fields.String
})


payment_info_schema = payment_api.model('PaymentInfo', {
    'method_of_payment': fields.String
})

filing_type_schema = payment_api.model('FilingType', {
    'filing_type_code': fields.String,
    'priority': fields.Boolean,
    'filing_description': fields.String
})

filing_info_schema = payment_api.model('FilingInfo', {
    'corp_type': fields.String,
    'date': fields.String,
    'filing_types': fields.List(fields.Nested(filing_type_schema)),
})

contact_info_schema = payment_api.model('ContactInfo', {
    'first_name': fields.String,
    'last_name': fields.String,
    'address': fields.String,
    'city': fields.String,
    'province': fields.String,
    'postal_code': fields.String,
})

business_info_schema = payment_api.model('BusinessInfo', {
    'business_identifier': fields.String,
    'business_name': fields.String,
    'contact_info': fields.Nested(contact_info_schema)
})

payment_request_schema = payment_api.model('PaymentRequest', {
    'payment_info': fields.Nested(payment_info_schema),
    'business_info': fields.Nested(business_info_schema),
    'filing_info': fields.Nested(filing_info_schema)
})


calculate_fees_request_schema = payment_api.model('CalculateFeesRequest', {
    'corp_type': fields.String,
    'filing_type_code': fields.String,
    'jurisdiction': fields.String,
    'date': fields.String,
    'priority': fields.String
})


payment_invoice_schema = payment_api.model('PaymentInvoice', {
    'id': fields.String,
    'reference_number': fields.String,
    'status_code': fields.String,
    'created_by': fields.String,
    'created_on': fields.String
})

payment_response_schema = payment_api.model('Payment', {
    'id': fields.String,
    'invoices': fields.List(fields.Nested(payment_invoice_schema)),
    'payment_method': fields.String,
    'status_code': fields.String,
    'created_by': fields.String,
    'created_on': fields.String,
    'updated_by': fields.String,
    'updated_on': fields.String
})


@payment_api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@cors_preflight('GET, POST')
@payment_api.route('/', strict_slashes=False, methods=['GET', 'POST', 'OPTIONS'])
@payment_api.doc(params={
})
class Payments(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @payment_api.expect(payment_request_schema)
    @payment_api.response(200, 'Success', '')
    # @marshal_with()
    @payment_api.doc(params={
    })
    def post():
        json_input = json.loads(request.get_json())
        if not json_input:
            return jsonify(message='No JSON data provided'), 400

        payment_info = json_input.get('payment_info')
        filing_info = json_input.get('filing_info')
        business_info = json_input.get('business_info')

        req = PaymentRequest(
            payment_info=payment_info,
            filing_info=filing_info,
            business_info=business_info
        )

        payment = create_payment(req)
        data = jsonify(payment.to_dict())
        response = make_response(data, 200)
        return response


@cors_preflight('GET, PUT')
@payment_api.route('/<string:payment_identifier>', strict_slashes=False, methods=['GET', 'POST', 'PUT', 'OPTIONS'])
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
        payment_identifier = unquote_plus(payment_identifier.strip()) if payment_identifier else None

        payment = get_payment(payment_identifier)
        data = jsonify(payment.to_dict())
        response = make_response(data, 200)
        return response

    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @payment_api.expect(payment_request_schema)
    @payment_api.response(200, 'Success', '')
    # @marshal_with()
    def put(payment_identifier):
        payment_identifier = unquote_plus(payment_identifier.strip()) if payment_identifier else None

        json_input = json.loads(request.get_json())
        if not json_input:
            return jsonify(message='No JSON data provided'), 400

        payment_info = json_input.get('payment_info')
        filing_info = json_input.get('filing_info')
        business_info = json_input.get('business_info')

        req = PaymentRequest(
            payment_info=payment_info,
            filing_info=filing_info,
            business_info=business_info
        )

        payment = update_payment(payment_identifier, req)
        data = jsonify(payment.to_dict())
        response = make_response(data, 200)
        return response


@cors_preflight('POST')
@payment_api.route('/fees', strict_slashes=False, methods=['POST', 'OPTIONS'])
class PaymentFees(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @payment_api.expect(calculate_fees_request_schema)
    @payment_api.response(200, 'Success', '')
    # @marshal_with()
    @payment_api.doc(params={
    })
    def post():
        json_input = json.loads(request.get_json())
        if not json_input:
            return jsonify(message='No JSON data provided'), 400

        corp_type = json_input.get('corp_type')
        filing_type_code = json_input.get('filing_type_code')
        jurisdiction = json_input.get('jurisdiction', None)
        date = json_input.get('date', None)
        priority = json_input.get('priority', None)

        req = CalculateFeesRequest(
            corp_type=corp_type,
            filing_type_code=filing_type_code,
            jurisdiction=jurisdiction,
            date=date,
            priority=priority
        )

        fees = calculate_fees(req)
        data = jsonify(fees.to_dict())
        response = make_response(data, 200)
        return response


@cors_preflight('GET')
@payment_api.route('/<string:payment_identifier>/invoices', strict_slashes=False, methods=['GET', 'OPTIONS'])
@payment_api.doc(params={
    'payment_identifier': ''
})
class PaymentInvoices(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @payment_api.response(200, 'Success', '')
    # @marshal_with()
    @payment_api.doc(params={
    })
    def get(payment_identifier):
        payment_identifier = unquote_plus(payment_identifier.strip()) if payment_identifier else None

        invoices = get_invoices(payment_identifier)
        data = jsonify(invoices.to_dict())
        response = make_response(data, 200)
        return response


@cors_preflight('GET')
@payment_api.route('/<string:payment_identifier>/invoice', strict_slashes=False, methods=['GET', 'OPTIONS'])
@payment_api.doc(params={
    'payment_identifier': ''
})
class PaymentInvoice(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @payment_api.response(200, 'Success', '')
    # @marshal_with()
    @payment_api.doc(params={
        'invoice_id': '[required]'
    })
    def get(payment_identifier):
        payment_identifier = unquote_plus(payment_identifier.strip()) if payment_identifier else None
        invoice_id = unquote_plus(request.args.get('invoice_id').strip()) if request.args.get('invoice_id') else None

        invoice = get_invoice(payment_identifier, invoice_id)
        data = jsonify(invoice.to_dict())
        response = make_response(data, 200)
        return response


@cors_preflight('GET')
@payment_api.route('/<string:payment_identifier>/receipt', strict_slashes=False, methods=['GET', 'OPTIONS'])
@payment_api.doc(params={
    'payment_identifier': ''
})
class PaymentReceipt(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @payment_api.response(200, 'Success', '')
    # @marshal_with()
    def get(payment_identifier):
        payment_identifier = unquote_plus(payment_identifier.strip()) if payment_identifier else None

        receipt = get_receipt(payment_identifier)

        if not receipt:
            return

        data = jsonify(receipt.to_dict())
        response = make_response(data, 200)
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
        payment_identifier = unquote_plus(payment_identifier.strip()) if payment_identifier else None

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
        payment_identifier = unquote_plus(payment_identifier.strip()) if payment_identifier else None
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
        payment_identifier = unquote_plus(payment_identifier.strip()) if payment_identifier else None
        redirect_uri = unquote_plus(request.args.get('redirect_uri').strip()) if request.args.get('redirect_uri') else None

        req = CreateTransactionRequest(
            payment_identifier=payment_identifier,
            redirect_uri=redirect_uri
        )

        return create_transaction(req)

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
        payment_identifier = unquote_plus(payment_identifier.strip()) if payment_identifier else None
        receipt_number = unquote_plus(request.args.get('receipt_number').strip()) if request.args.get('receipt_number') else None
        transaction_identifier = unquote_plus(request.args.get('transaction_identifier').strip()) if request.args.get('transaction_identifier') else None

        req = UpdateTransactionRequest(
            payment_identifier=payment_identifier,
            receipt_number=receipt_number,
            transaction_identifier=transaction_identifier
        )

        return update_transaction(req)


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


