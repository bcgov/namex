from flask import request, make_response, send_file, jsonify
from flask_restplus import Namespace, Resource, cors, fields, marshal_with, marshal
from flask_jwt_oidc import AuthError

from namex.utils.logging import setup_logging
from namex.utils.util import cors_preflight

from urllib.parse import unquote_plus

from namex.models import Request

from namex.services.payment import PaymentServiceException

from namex.services.payment.fees import calculate_fees, CalculateFeesRequest

from namex.services.payment.invoices import get_invoices, get_invoice

from namex.services.payment.payments import get_payment, create_payment, update_payment, CreatePaymentRequest, UpdatePaymentRequest

from namex.services.payment.receipts import get_receipt

from namex.services.payment.transactions import \
    get_transactions, get_transaction, create_transaction, update_transaction, \
    GetTransactionsRequest, GetTransactionRequest, CreateTransactionRequest, UpdateTransactionRequest

from openapi_client.models import PaymentRequest, PaymentReceiptInput

setup_logging()  # It's important to do this first

# Register a local namespace for the NR reserve
payment_api = Namespace('payments', description='Payment API - Uses Service BC Pay')

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
# Snake case as these are GET params
calculate_fees_request_schema = payment_api.model('CalculateFeesRequest', {
    'corp_type': fields.String,
    'filing_type_code': fields.String,
    'jurisdiction': fields.String,
    'date': fields.String,
    'priority': fields.String
})

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
@payment_api.route('/<string:nr_num>', strict_slashes=False, methods=['POST', 'OPTIONS'])
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
        'nr_num': 'Name Request number'
    })
    def post(nr_num):
        # TODO: Validate NR string format
        # if not Request.validNRFormat(nr_num):
        #    return None, None, jsonify(message='NR number is not in a valid format \'NR 9999999\''), 400

        nr_draft = Request.find_by_nr(nr_num)
        if not nr_draft:
            # Should this be a 400 or 404... hmmm
            return None, None, jsonify(message='{nr_num} not found'.format(nr_num=nr_num)), 400

        json_input = request.get_json()
        if not json_input:
            return jsonify(message=MSG_BAD_REQUEST_NO_JSON_BODY), 400

        # Grab the info we need off the request
        payment_info = json_input.get('paymentInfo')
        filing_info = json_input.get('filingInfo')
        business_info = json_input.get('businessInfo')

        # Create our payment request
        req = PaymentRequest(
            payment_info=payment_info,
            filing_info=filing_info,
            business_info=business_info
        )

        try:
            payment = create_payment(req)
            if not payment:
                raise PaymentServiceException(MSG_ERROR_CREATING_RESOURCE)

            # Update the name request with the payment id
            # nr_draft.paymentToken = str(payment.id)
            nr_draft.payment_token = str(payment.id)
            # Save the name request
            nr_draft.save_to_db()

        except Exception as err:
            return jsonify(message=MSG_SERVER_ERROR + ' ' + str(err)), err.status if err.status else err

        data = jsonify(payment.to_dict())
        response = make_response(data, 200)
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
        payment_identifier = unquote_plus(payment_identifier.strip()) if payment_identifier else None

        try:
            payment = get_payment(payment_identifier)
        except Exception as err:
            return jsonify(message=MSG_SERVER_ERROR + ' ' + str(err)), 500

        if not payment:
            return jsonify(message=MSG_NOT_FOUND), 404

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

        try:
            payment = update_payment(payment_identifier, req)
            if not payment:
                raise PaymentServiceException(MSG_ERROR_CREATING_RESOURCE)

        except Exception as err:
            return jsonify(message=MSG_SERVER_ERROR + ' ' + str(err)), 500

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
    @payment_api.response(200, 'Success')
    @payment_api.response(400, 'Bad Request')
    @payment_api.response(500, 'Internal Server Error')
    # @marshal_with()
    @payment_api.doc(params={
    })
    def post():
        json_input = request.get_json()
        if not json_input:
            return jsonify(message=MSG_BAD_REQUEST_NO_JSON_BODY), 400

        corp_type = json_input.get('corp_type')
        filing_type_code = json_input.get('filing_type_code')
        jurisdiction = json_input.get('jurisdiction', None)
        date = json_input.get('date', None)
        priority = json_input.get('priority', None)

        # Params are snake_case for this POST
        # Response data is also snake_case
        req = CalculateFeesRequest(
            corp_type=corp_type,
            filing_type_code=filing_type_code,
            jurisdiction=jurisdiction,
            date=date,
            priority=priority
        )

        try:
            fees = calculate_fees(req)
            if not fees:
                raise PaymentServiceException(MSG_ERROR_CREATING_RESOURCE)
        except Exception as err:
            return jsonify(message=MSG_SERVER_ERROR + ' ' + str(err)), 500

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

        try:
            invoices = get_invoices(payment_identifier)
        except Exception as err:
            return jsonify(message=MSG_SERVER_ERROR + ' ' + str(err)), 500

        if not invoices:
            return jsonify(message=MSG_NOT_FOUND), 404

        data = jsonify(invoices.to_dict())
        response = make_response(data, 200)
        return response


@cors_preflight('GET')
@payment_api.route('/<string:payment_identifier>/invoice/<int:invoice_id>', strict_slashes=False, methods=['GET', 'OPTIONS'])
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
    def get(payment_identifier, invoice_id):
        payment_identifier = unquote_plus(payment_identifier.strip()) if payment_identifier else None
        invoice_id = invoice_id if invoice_id else None

        try:
            invoice = get_invoice(payment_identifier, invoice_id)
        except Exception as err:
            return jsonify(message=MSG_SERVER_ERROR + ' ' + str(err)), 500

        if not invoice:
            return jsonify(message=MSG_NOT_FOUND), 404

        data = jsonify(invoice.to_dict())
        response = make_response(data, 200)
        return response


@cors_preflight('GET')
# @payment_api.route('/<string:payment_identifier>/receipt/<int:invoice_id>', strict_slashes=False, methods=['POST', 'OPTIONS'])
@payment_api.route('/<string:payment_identifier>/receipt', strict_slashes=False, methods=['POST', 'OPTIONS'])
@payment_api.doc(params={
    'payment_identifier': '',
    # 'invoice_id': '[required]'
})
class PaymentReceipt(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @payment_api.response(200, 'Success', '')
    # @marshal_with()
    # def post(payment_identifier, invoice_id):
    def post(payment_identifier):
        payment_identifier = unquote_plus(payment_identifier.strip()) if payment_identifier else None

        json_input = request.get_json()
        if not json_input:
            return jsonify(message=MSG_BAD_REQUEST_NO_JSON_BODY), 400

        corp_name = json_input.get('corpName', None)
        business_number = json_input.get('businessNumber', None)
        recognition_date_time = json_input.get('recognitionDateTime', None)
        filing_identifier = json_input.get('filingIdentifier', None)
        filing_date_time = json_input.get('filingDateTime', None)
        file_name = json_input.get('fileName', None)

        req = PaymentReceiptInput(
            corp_name=corp_name,
            business_number=business_number,
            recognition_date_time=recognition_date_time,
            filing_identifier=filing_identifier,
            filing_date_time=filing_date_time,
            file_name=file_name
        )

        try:
            receipt = get_receipt(payment_identifier, req)
        except Exception as err:
            return jsonify(message=MSG_SERVER_ERROR + ' ' + str(err)), 500

        if not receipt:
            return jsonify(message=MSG_NOT_FOUND), 404

        return send_file(receipt, mimetype='application/pdf', as_attachment=True)


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
        payment_identifier = unquote_plus(payment_identifier.strip()) if payment_identifier else None

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


