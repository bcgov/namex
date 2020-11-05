from pprint import pprint

from .client import SBCPaymentClient
from .exceptions import SBCPaymentException
from .models.abstract import Serializable


class GetInvoiceRequest(Serializable):
    def __init__(self, **kwargs):
        self.payment_identifier = kwargs.get('payment_identifier')
        self.invoice_id = kwargs.get('invoice_id')


class GetInvoicesRequest(Serializable):
    def __init__(self, **kwargs):
        self.payment_identifier = kwargs.get('payment_identifier')


def get_invoice(invoice_id):
    try:
        # Create an instance of the API class
        api_instance = SBCPaymentClient()
        # Get Invoice
        api_response = api_instance.get_invoice(invoice_id)

        pprint(api_response)
        return api_response

    except Exception as err:
        raise SBCPaymentException(err)


def get_invoices(payment_identifier):
    try:
        # Create an instance of the API class
        api_instance = SBCPaymentClient()
        # Get Invoices
        api_response = api_instance.get_invoices(payment_identifier)

        pprint(api_response)
        return api_response

    except Exception as err:
        raise SBCPaymentException(err)
