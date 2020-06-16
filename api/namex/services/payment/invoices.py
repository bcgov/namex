from __future__ import print_function
from pprint import pprint

import openapi_client
from openapi_client.rest import ApiException

from .request_objects.abstract import Serializable

PAYMENTS_API_HOST = 'http://localhost:4010'


class GetInvoiceRequest(Serializable):
    def __init__(self, **kwargs):
        self.payment_identifier = kwargs.get('payment_identifier')
        self.invoice_id = kwargs.get('invoice_id')


class GetInvoicesRequest(Serializable):
    def __init__(self, **kwargs):
        self.payment_identifier = kwargs.get('payment_identifier')


def get_invoice(payment_identifier, invoice_id):
    # Create an instance of the API class
    api_instance = openapi_client.InvoicesApi()
    # Set API host URI
    api_instance.api_client.configuration.host = PAYMENTS_API_HOST

    try:
        # Get Invoice
        api_response = api_instance.get_invoice(payment_identifier, invoice_id)

        pprint(api_response)
        return api_response

    except Exception as e:
        print("Exception when calling InvoicesApi->get_invoice: %s\n" % e)


def get_invoices(payment_identifier):
    # Create an instance of the API class
    api_instance = openapi_client.InvoicesApi()
    # Set API host URI
    api_instance.api_client.configuration.host = PAYMENTS_API_HOST

    try:
        # Get Invoices
        api_response = api_instance.get_invoices(payment_identifier)

        pprint(api_response)
        return api_response

    except Exception as e:
        print("Exception when calling InvoicesApi->get_invoices: %s\n" % e)
