from pprint import pprint

from .client import SBCPaymentClient
from .models import PaymentInvoice
from .exceptions import SBCPaymentException


def get_payment(payment_identifier):
    try:
        api_instance = SBCPaymentClient()
        api_response = api_instance.get_payment(payment_identifier)
        pprint(api_response)
        return PaymentInvoice(**api_response)

    except Exception as err:
        raise SBCPaymentException(err)


def create_payment(model):
    try:
        data = model
        api_instance = SBCPaymentClient()
        api_response = api_instance.create_payment(data)
        pprint(api_response)
        return PaymentInvoice(**api_response)

    except Exception as err:
        raise SBCPaymentException(err)


def refund_payment(payment_identifier, model=None):
    try:
        data = model
        api_instance = SBCPaymentClient()
        api_response = api_instance.refund_payment(payment_identifier, data)
        pprint(api_response)
        return PaymentInvoice(**api_response)

    except Exception as err:
        raise SBCPaymentException(err)
