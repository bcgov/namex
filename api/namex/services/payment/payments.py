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
        # pay-api returns 402 (previously 400) when an API key request with fees uses a
        # CC / Online Banking account; surface both to the caller as 402 with pay-api's detail.
        if getattr(err, 'status_code', None) in (HTTPStatus.BAD_REQUEST, HTTPStatus.PAYMENT_REQUIRED):
            raise SBCPaymentException(err, getattr(err, 'detail', None) or str(err), HTTPStatus.PAYMENT_REQUIRED)

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
