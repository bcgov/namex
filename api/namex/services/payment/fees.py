from __future__ import print_function
from pprint import pprint

import openapi_client
# Other stuff you can import...
# from openapi_client.models import Fees
# from openapi_client.rest import ApiException

from . import PAYMENT_SVC_URL, PAYMENT_SVC_AUTH_URL, AUTH_SVC_CLIENT_ID, PAYMENT_SVC_CLIENT_SECRET
from namex.utils.util import get_client_credentials

from .request_objects.abstract import Serializable


class CalculateFeesRequest(Serializable):
    def __init__(self, **kwargs):
        self.corp_type = kwargs.get('corp_type')
        self.filing_type_code = kwargs.get('filing_type_code')
        self.jurisdiction = kwargs.get('jurisdiction', None)
        self.date = kwargs.get('date', None)
        self.priority = kwargs.get('priority', None)


def calculate_fees(req):
    # Create an instance of the API class
    api_instance = openapi_client.FeesApi()

    authenticated, token = get_client_credentials(PAYMENT_SVC_AUTH_URL, AUTH_SVC_CLIENT_ID, PAYMENT_SVC_CLIENT_SECRET)
    if not authenticated:
        raise Exception('Client credentials request failed')
    api_instance.api_client.set_default_header('Authorization', 'Bearer ' + token)

    # Set API host URI
    api_instance.api_client.configuration.host = PAYMENT_SVC_URL

    try:
        # Calculate Fees
        api_response = api_instance.calculate_fees(
            req.corp_type,
            req.filing_type_code,
            jurisdiction=req.jurisdiction,
            date=req.date,
            priority=req.priority
        )

        pprint(api_response)
        return api_response

    except Exception as e:
        print("Exception when calling FeesApi->calculate_fees: %s\n" % e)
