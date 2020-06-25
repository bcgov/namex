from __future__ import print_function
from pprint import pprint

import openapi_client
# Other stuff you can import...
# from openapi_client.models import Receipt
# from openapi_client.rest import ApiException

from . import PAYMENT_SVC_URL, PAYMENT_SVC_AUTH_URL, AUTH_SVC_CLIENT_ID, PAYMENT_SVC_CLIENT_SECRET
from namex.utils.util import get_client_credentials

from .request_objects.abstract import Serializable


class GetReceiptRequest(Serializable):
    def __init__(self, **kwargs):
        self.payment_identifier = kwargs.get('payment_identifier')


def get_receipt(payment_identifier):
    # Create an instance of the API class
    api_instance = openapi_client.ReceiptsApi()

    authenticated, token = get_client_credentials(PAYMENT_SVC_AUTH_URL, AUTH_SVC_CLIENT_ID, PAYMENT_SVC_CLIENT_SECRET)
    if not authenticated:
        raise Exception('Client credentials request failed')
    api_instance.api_client.set_default_header('Authorization', 'Bearer ' + token)

    # Set API host URI
    api_instance.api_client.configuration.host = PAYMENT_SVC_URL

    try:
        # Get receipt for the payment
        api_response = api_instance.get_receipt(payment_identifier)

        pprint(api_response)
        return api_response

    except Exception as e:
        print("Exception when calling ReceiptsApi->get_receipt: %s\n" % e)
