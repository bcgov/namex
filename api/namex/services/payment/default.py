from __future__ import print_function

import openapi_client
# Other stuff you can import...
# from openapi_client.rest import ApiException

from . import PAYMENT_SVC_URL, PAYMENT_SVC_AUTH_URL, AUTH_SVC_CLIENT_ID, PAYMENT_SVC_CLIENT_SECRET
from namex.utils.util import get_client_credentials

from .request_objects.abstract import Serializable


class Request(Serializable):
    def __init__(self, **kwargs):
        self.payment_identifier = kwargs.get('payment_identifier')


def delete_api_v1_payment_requests_payment_identifier(req, callback):
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi()

    authenticated, token = get_client_credentials(PAYMENT_SVC_AUTH_URL, AUTH_SVC_CLIENT_ID, PAYMENT_SVC_CLIENT_SECRET)
    if not authenticated:
        raise Exception('Client credentials request failed')
    api_instance.api_client.set_default_header('Authorization', 'Bearer ' + token)

    try:
        api_instance.delete_api_v1_payment_requests_payment_identifier(
            req.payment_identifier
        )

    except Exception as e:
        print("Exception when calling DefaultApi->delete_api_v1_payment_requests_payment_identifier: %s\n" % e)
