from __future__ import print_function

import openapi_client
from openapi_client.rest import ApiException

from .request_objects.abstract import Serializable


class Request(Serializable):
    def __init__(self, **kwargs):
        self.payment_identifier = kwargs.get('payment_identifier')


def delete_api_v1_payment_requests_payment_identifier(req, callback):
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi()

    try:
        api_instance.delete_api_v1_payment_requests_payment_identifier(
            req.payment_identifier
        )

    except Exception as e:
        print("Exception when calling DefaultApi->delete_api_v1_payment_requests_payment_identifier: %s\n" % e)
