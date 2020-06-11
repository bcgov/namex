from __future__ import print_function
from pprint import pprint

import openapi_client
from openapi_client.rest import ApiException

from .request_objects.abstract import Serializable


class GetReceiptRequest(Serializable):
    def __init__(self, **kwargs):
        self.payment_identifier = kwargs.get('payment_identifier')


def get_receipt(req):
    # Create an instance of the API class
    api_instance = openapi_client.ReceiptsApi()

    try:
        # Get receipt for the payment
        api_response = api_instance.get_receipt(
            req.payment_identifier
        )

        pprint(api_response)
        return api_response

    except ApiException as e:
        print("Exception when calling ReceiptsApi->get_receipt: %s\n" % e)
