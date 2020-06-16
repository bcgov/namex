from __future__ import print_function
from pprint import pprint

import openapi_client
from openapi_client.rest import ApiException

from .request_objects.abstract import Serializable

PAYMENTS_API_HOST = 'http://localhost:4010'


class GetReceiptRequest(Serializable):
    def __init__(self, **kwargs):
        self.payment_identifier = kwargs.get('payment_identifier')


def get_receipt(payment_identifier):
    # Create an instance of the API class
    api_instance = openapi_client.ReceiptsApi()
    # Set API host URI
    api_instance.api_client.configuration.host = PAYMENTS_API_HOST

    try:
        # Get receipt for the payment
        api_response = api_instance.get_receipt(payment_identifier)

        pprint(api_response)
        return api_response

    except Exception as e:
        print("Exception when calling ReceiptsApi->get_receipt: %s\n" % e)
