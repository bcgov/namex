from flask import send_file, make_response, jsonify
from flask_restx import Resource, cors
from flask_jwt_oidc import AuthError

from namex.utils.logging import setup_logging
from namex.utils.auth import cors_preflight
from namex.utils.api_resource import handle_exception

from namex.models import Request as RequestDAO, Payment as PaymentDAO

from namex.services.payment.exceptions import SBCPaymentException, SBCPaymentError, PaymentServiceError
from namex.services.payment.receipts import get_receipt, generate_receipt
from namex.services.payment.models import ReceiptRequest

from .api_namespace import api as payment_api

setup_logging()  # It's important to do this first

MSG_BAD_REQUEST_NO_JSON_BODY = 'No JSON data provided'
MSG_SERVER_ERROR = 'Server Error!'
MSG_NOT_FOUND = 'Resource not found'


def validate_request():
    return True


@payment_api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@cors_preflight('GET, POST')
@payment_api.route('/<int:payment_id>/receipt', strict_slashes=False, methods=['GET', 'POST', 'OPTIONS'])
@payment_api.doc(params={
    'payment_id': ''
})
class PaymentReceipt(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    @payment_api.response(201, 'Created', '')
    def post(payment_id):
        try:
            payment = PaymentDAO.query.get(payment_id)
            # Find the existing name request
            nr_model = RequestDAO.query.get(payment.nrId)

            if not nr_model:
                # Should this be a 400 or 404... hmmm
                return jsonify(message='{nr_id} not found'.format(nr_id=nr_model.id)), 400

            receipt_info = get_receipt(payment.payment_token)
            name_choice = RequestDAO.find_name_by_choice(nr_model.id, 1)
            if not name_choice:
                return jsonify(message='Could not find name choice for {nr_id}'.format(nr_id=nr_model.id)), 400

            receipt_req = ReceiptRequest(
                corpName=name_choice.name,
                filingDateTime=payment.payment_completion_date.strftime('%d %b %Y, %-I:%M %p')
            )

            receipt_response = generate_receipt(payment.payment_token, receipt_req)

            if not receipt_response:
                return jsonify(message=MSG_NOT_FOUND), 404

            return send_file(
                receipt_response,
                as_attachment=True,
                attachment_filename='payment-receipt-{id}.pdf'.format(id=receipt_info.get('receiptNumber')))

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
    @payment_api.response(200, 'Success', '')
    def get(payment_id):
        try:
            payment = PaymentDAO.query.get(payment_id)
            # Find the existing name request
            nr_model = RequestDAO.query.get(payment.nrId)

            if not nr_model:
                # Should this be a 400 or 404... hmmm
                return jsonify(message='{nr_id} not found'.format(nr_id=nr_model.id)), 400

            receipt_response = get_receipt(payment.payment_token)

            if not receipt_response:
                return jsonify(message=MSG_NOT_FOUND), 404  # TODO: What if we have a record?

            response = make_response(receipt_response, 200)
            return response

        except PaymentServiceError as err:
            return handle_exception(err, err.message, 500)
        except SBCPaymentException as err:
            return handle_exception(err, err.message, err.status_code)
        except SBCPaymentError as err:
            return handle_exception(err, err.message, 500)
        except Exception as err:
            return handle_exception(err, err, 500)
