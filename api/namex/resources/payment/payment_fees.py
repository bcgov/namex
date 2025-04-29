from flask import jsonify, make_response, request
from flask_jwt_oidc import AuthError
from flask_restx import Resource, fields

from namex.services.payment.exceptions import PaymentServiceError, SBCPaymentError, SBCPaymentException
from namex.services.payment.fees import CalculateFeesRequest, calculate_fees
from namex.utils.api_resource import handle_exception
from namex.utils.auth import cors_preflight

from .api_namespace import api as payment_api

MSG_BAD_REQUEST_NO_JSON_BODY = 'No JSON data provided'
MSG_SERVER_ERROR = 'Server Error!'
MSG_NOT_FOUND = 'Resource not found'


def validate_request(request):
    return True


# Define our request objects
# Snake case as these are GET params
calculate_fees_request_schema = payment_api.model(
    'CalculateFeesRequest',
    {
        'corp_type': fields.String,
        'filing_type_code': fields.String,
        'jurisdiction': fields.String,
        'date': fields.String,
        'priority': fields.String,
    },
)


@payment_api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@cors_preflight('POST')
@payment_api.route('/fees', strict_slashes=False, methods=['POST', 'OPTIONS'])
class PaymentFees(Resource):
    @staticmethod
    @payment_api.expect(calculate_fees_request_schema)
    @payment_api.response(200, 'Success')
    @payment_api.response(400, 'Bad Request')
    @payment_api.response(500, 'Internal Server Error')
    @payment_api.doc(params={})
    def post():
        try:
            json_input = request.get_json()
            if not json_input:
                return make_response(jsonify(message=MSG_BAD_REQUEST_NO_JSON_BODY), 400)

            corp_type = json_input.get(
                'corp_type', 'NRO'
            )  # TODO: Maybe use a constant for this, it's the default corp_type, and I am not aware of a situation where it would be changed...
            filing_type_code = json_input.get(
                'filing_type_code'
            )  # TODO: Maybe throw an error if these don't exist, we can't really get fees without them
            jurisdiction = json_input.get(
                'jurisdiction', None
            )  # TODO: Maybe throw an error if these don't exist, we can't really get fees without them
            date = json_input.get('date', None)
            priority = json_input.get('priority', None)
            headers = json_input.get('headers', None)

            # Params are snake_case for this POST
            req = CalculateFeesRequest(
                corp_type=corp_type,
                filing_type_code=filing_type_code,
                jurisdiction=jurisdiction,
                date=date,
                priority=priority,
                headers=headers,
            )

            fees = calculate_fees(req)
            data = jsonify(fees)
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
