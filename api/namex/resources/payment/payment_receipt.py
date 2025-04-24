from flask import jsonify, make_response, send_file
from flask_jwt_oidc import AuthError
from flask_restx import Resource
from pytz import timezone

from namex.models import Payment as PaymentDAO
from namex.models import Request as RequestDAO
from namex.services.payment.exceptions import PaymentServiceError, SBCPaymentError, SBCPaymentException
from namex.services.payment.models import ReceiptRequest
from namex.services.payment.receipts import generate_receipt, get_receipt
from namex.utils.api_resource import handle_exception
from namex.utils.auth import cors_preflight

from .api_namespace import api as payment_api

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
@payment_api.doc(params={'payment_id': ''})
class PaymentReceipt(Resource):
    @staticmethod
    @payment_api.response(201, 'Created', '')
    def post(payment_id):
        try:
            payment = PaymentDAO.query.get(payment_id)
            # Find the existing name request
            nr_model = RequestDAO.query.get(payment.nrId)

            if not nr_model:
                # Should this be a 400 or 404... hmmm
                return make_response(jsonify(message='{nr_id} not found'.format(nr_id=nr_model.id)), 400)

            receipt_info = get_receipt(payment.payment_token)
            name_choice = RequestDAO.find_name_by_choice(nr_model.id, 1)
            if not name_choice:
                return make_response(
                    jsonify(message='Could not find name choice for {nr_id}'.format(nr_id=nr_model.id)), 400
                )

            tz_aware_submission_date = nr_model.submittedDate.replace(tzinfo=timezone('UTC'))
            localized_submission_date = tz_aware_submission_date.astimezone(timezone('US/Pacific'))
            receipt_req = ReceiptRequest(
                corpName=name_choice.name,
                filingDateTime=localized_submission_date.strftime('%B %-d, %Y at %-I:%M %P Pacific time'),
            )

            receipt_response = generate_receipt(payment.payment_token, receipt_req)

            if not receipt_response:
                return make_response(jsonify(message=MSG_NOT_FOUND), 404)

            return send_file(
                receipt_response,
                as_attachment=True,
                download_name='payment-receipt-{id}.pdf'.format(id=receipt_info.get('receiptNumber')),
            )

        except PaymentServiceError as err:
            return handle_exception(err, err.message, 500)
        except SBCPaymentException as err:
            return handle_exception(err, err.message, err.status_code)
        except SBCPaymentError as err:
            return handle_exception(err, err.message, 500)
        except Exception as err:
            return handle_exception(err, err, 500)

    @staticmethod
    @payment_api.response(200, 'Success', '')
    def get(payment_id):
        try:
            payment = PaymentDAO.query.get(payment_id)
            # Find the existing name request
            nr_model = RequestDAO.query.get(payment.nrId)

            if not nr_model:
                # Should this be a 400 or 404... hmmm
                return make_response(jsonify(message='{nr_id} not found'.format(nr_id=nr_model.id)), 400)

            receipt_response = get_receipt(payment.payment_token)
            if receipt_response is None:
                return make_response(jsonify(message=MSG_NOT_FOUND), 404)  # TODO: What if we have a record?

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
