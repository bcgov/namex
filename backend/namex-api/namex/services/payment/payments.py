from http import HTTPStatus

from flask import current_app

from .client import SBCPaymentClient
from .exceptions import SBCPaymentException
from .models import PaymentInvoice, PaymentRefundInvoice


def get_payment(payment_identifier):
    try:
        api_instance = SBCPaymentClient()
        api_response = api_instance.get_payment(payment_identifier)
        current_app.logger.debug(api_response)
        return PaymentInvoice(**api_response)

    except Exception as err:
        raise SBCPaymentException(err)


def create_payment(model, headers):
    try:
        data = model
        api_instance = SBCPaymentClient()
        api_response = api_instance.create_payment(data, headers)
        current_app.logger.debug(api_response)
        return PaymentInvoice(**api_response)

    except Exception as err:
        if err.status_code == HTTPStatus.BAD_REQUEST:
            raise SBCPaymentException(err, err.detail, HTTPStatus.PAYMENT_REQUIRED)

        raise SBCPaymentException(err)


def refund_payment(payment_identifier, model=None):
    try:
        data = model
        api_instance = SBCPaymentClient()
        api_response = api_instance.refund_payment(payment_identifier, data)
        current_app.logger.debug(
            'services refund_payment response',
            payment_identifier=payment_identifier,
            api_response=api_response,
        )
        return PaymentRefundInvoice(**api_response) if api_response else None

    except Exception as err:
        raise SBCPaymentException(err)


def cancel_payment(payment_identifier):
    try:
        api_instance = SBCPaymentClient()
        api_response = api_instance.cancel_payment(payment_identifier)
        current_app.logger.debug(api_response)
    except Exception as err:
        raise SBCPaymentException(err)
