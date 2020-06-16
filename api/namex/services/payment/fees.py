from __future__ import print_function
from pprint import pprint

import openapi_client
from openapi_client.rest import ApiException

from .request_objects.abstract import Serializable

PAYMENTS_API_HOST = 'http://localhost:4010'


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
    # Set API host URI
    api_instance.api_client.configuration.host = PAYMENTS_API_HOST

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
