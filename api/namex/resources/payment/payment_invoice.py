from flask import make_response, jsonify
from flask_restplus import Resource, cors, fields, marshal_with, marshal
from flask_jwt_oidc import AuthError

from namex.utils.logging import setup_logging
from namex.utils.auth import cors_preflight
from namex.utils.api_resource import clean_url_path_param, handle_exception

from namex.services.payment.exceptions import SBCPaymentException, SBCPaymentError, PaymentServiceError
from namex.services.payment.invoices import get_invoices, get_invoice

from .api_namespace import api as payment_api

setup_logging()  # It's important to do this first

MSG_BAD_REQUEST_NO_JSON_BODY = 'No JSON data provided'
MSG_SERVER_ERROR = 'Server Error!'
MSG_NOT_FOUND = 'Resource not found'
MSG_ERROR_CREATING_RESOURCE = 'Could not create / update resource'


def validate_request(request):
    return True


# Define our DTO models
# Custom model types
payment_invoice_schema = payment_api.model('PaymentInvoice', {
    'id': fields.String,
    'referenceNumber': fields.String,
    'statusCode': fields.String,
    'createdBy': fields.String,
    'createdOn': fields.String
})


@payment_api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
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
        try:
            payment_identifier = clean_url_path_param(payment_identifier)

            invoices = get_invoices(payment_identifier)

            if not invoices:
                return jsonify(message=MSG_NOT_FOUND), 404

            data = jsonify(invoices.to_dict())
            response = make_response(data, 200)
            return response

        except PaymentServiceError as err:
            return handle_exception(err, err.message, 500)
        except SBCPaymentException as err:
            return handle_exception(err, err.message, 500)
        except SBCPaymentError as err:
            return handle_exception(err, err.message, err.status_code)
        except Exception as err:
            return handle_exception(err, err, 500)


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
        try:
            payment_identifier = clean_url_path_param(payment_identifier)
            invoice_id = invoice_id if invoice_id else None

            invoice = get_invoice(payment_identifier, invoice_id)

            if not invoice:
                return jsonify(message=MSG_NOT_FOUND), 404

            data = jsonify(invoice.to_dict())
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
