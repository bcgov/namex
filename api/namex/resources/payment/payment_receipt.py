from flask import request, send_file, jsonify
from flask_restplus import Resource, cors, fields, marshal_with, marshal
from flask_jwt_oidc import AuthError

from namex.utils.logging import setup_logging
from namex.utils.auth import cors_preflight
from namex.utils.api_resource import clean_url_path_param, handle_exception

from namex.services.payment.exceptions import SBCPaymentException, SBCPaymentError, PaymentServiceError
from namex.services.payment.receipts import get_receipt

from .api_namespace import api as payment_api

from openapi_client.models import PaymentReceiptInput

setup_logging()  # It's important to do this first

MSG_BAD_REQUEST_NO_JSON_BODY = 'No JSON data provided'
MSG_SERVER_ERROR = 'Server Error!'
MSG_NOT_FOUND = 'Resource not found'
MSG_ERROR_CREATING_RESOURCE = 'Could not create / update resource'


def validate_request(request):
    return True


@payment_api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
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
        try:
            payment_identifier = clean_url_path_param(payment_identifier)

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

            receipt = get_receipt(payment_identifier, req)

            if not receipt:
                return jsonify(message=MSG_NOT_FOUND), 404

            return send_file(receipt, mimetype='application/pdf', as_attachment=True)

        except PaymentServiceError as err:
            return handle_exception(err, err.message, 500)
        except SBCPaymentException as err:
            return handle_exception(err, err.message, 500)
        except SBCPaymentError as err:
            return handle_exception(err, err.message, 500)
        except Exception as err:
            return handle_exception(err, err, 500)
