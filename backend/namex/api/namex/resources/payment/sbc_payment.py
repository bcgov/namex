from flask import jsonify, make_response
from flask_jwt_oidc import AuthError
from flask_restx import Resource

from namex.services.payment.exceptions import PaymentServiceError, SBCPaymentError, SBCPaymentException
from namex.services.payment.payments import get_payment
from namex.utils.api_resource import clean_url_path_param, handle_exception
from namex.utils.auth import cors_preflight

from .api_namespace import api as payment_api

MSG_BAD_REQUEST_NO_JSON_BODY = 'No JSON data provided'
MSG_SERVER_ERROR = 'Server Error!'
MSG_NOT_FOUND = 'Resource not found'


def validate_request(request):
    return True


@payment_api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@cors_preflight('GET, PUT')
@payment_api.route('/sbc-pay/<string:payment_identifier>', strict_slashes=False, methods=['GET', 'PUT', 'OPTIONS'])
class SBCPayment(Resource):
    @staticmethod
    # @jwt.requires_auth
    @payment_api.doc(
        description='Fetch SBC Pay payment details using the given payment identifier',
        params={'payment_identifier': 'Unique identifier for the SBC payment'},
        responses={
            200: 'Payment record fetched successfully',
            404: 'Payment record not found',
            500: 'Internal server error',
        },
    )
    # @marshal_with(payment_response_schema)
    def get(payment_identifier):
        try:
            payment_identifier = clean_url_path_param(payment_identifier)

            payment = get_payment(payment_identifier)

            if not payment:
                return make_response(jsonify(message=MSG_NOT_FOUND), 404)

            data = jsonify(payment)
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
@payment_api.route('/sbc-pay/extra', strict_slashes=False, methods=['DELETE', 'OPTIONS'])
class SBCPaymentExtra(Resource):
    @staticmethod
    # @jwt.requires_auth
    # @marshal_with()
    @payment_api.doc(
        description='Stub endpoint for deleting extra SBC payment data. Not yet implemented.',
        responses={
            200: 'Successfully deleted (stub response)',
            501: 'Not implemented',
        },
    )
    def delete():
        pass
