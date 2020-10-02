from flask import send_file, jsonify
from flask_restplus import Resource, cors
from flask_jwt_oidc import AuthError

from namex.utils.logging import setup_logging
from namex.utils.auth import cors_preflight
from namex.utils.api_resource import handle_exception

from namex.models import Request as RequestDAO, Payment as PaymentDAO

from namex.services.payment.exceptions import SBCPaymentException, SBCPaymentError, PaymentServiceError
from namex.services.payment.payments import get_payment
from namex.services.payment.receipts import get_receipt

from .api_namespace import api as payment_api

from openapi_client.models import PaymentReceiptInput

setup_logging()  # It's important to do this first

MSG_BAD_REQUEST_NO_JSON_BODY = 'No JSON data provided'
MSG_SERVER_ERROR = 'Server Error!'
MSG_NOT_FOUND = 'Resource not found'
MSG_ERROR_CREATING_RESOURCE = 'Could not create / update resource'


def validate_request():
    return True


@payment_api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@cors_preflight('GET')
@payment_api.route('/<int:payment_id>/receipt', strict_slashes=False, methods=['GET', 'OPTIONS'])
@payment_api.doc(params={
    'payment_id': ''
})
class PaymentReceipt(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @payment_api.response(200, 'Success', '')
    # @marshal_with()
    def get(payment_id):
        try:
            payment = PaymentDAO.query.get(payment_id)
            # Find the existing name request
            nr_model = RequestDAO.query.get(payment.nrId)

            if not nr_model:
                # Should this be a 400 or 404... hmmm
                return jsonify(message='{nr_id} not found'.format(nr_id=payment.nrId)), 400

            payment_response = get_payment(payment.payment_token)
            # TODO: Make sure we pick the right one... use the first choice
            corp_name = nr_model.names.all()[0].name

            req = PaymentReceiptInput(
                corp_name=corp_name,
                business_number=None,
                recognition_date_time=None,
                filing_identifier=None,
                filing_date_time=payment_response.created_on,
                file_name=None
            )

            receipt_response = get_receipt(payment.payment_token, req)

            if not receipt_response:
                return jsonify(message=MSG_NOT_FOUND), 404  # TODO: What if we have a record?

            return send_file(receipt_response, mimetype='application/pdf', as_attachment=True)

        except PaymentServiceError as err:
            return handle_exception(err, err.message, 500)
        except SBCPaymentException as err:
            return handle_exception(err, err.message, err.status_code)
        except SBCPaymentError as err:
            return handle_exception(err, err.message, 500)
        except Exception as err:
            return handle_exception(err, err, 500)
