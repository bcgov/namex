from __future__ import print_function
from pprint import pprint

import openapi_client
from openapi_client.models import Payment
from openapi_client.rest import ApiException

from .request_objects.abstract import Serializable

PAYMENTS_API_HOST = 'http://localhost:4010'


class PaymentInfo(Serializable):
    def __init__(self, **kwargs):
        self.method_of_payment = kwargs.get('method_of_payment', None)


class FilingInfo(Serializable):
    def __init__(self, **kwargs):
        self.corp_type = kwargs.get('corp_type', None)
        self.date = kwargs.get('date', None)
        self.filing_types = kwargs.get('filing_types', None)


class FilingType(Serializable):
    def __init__(self, **kwargs):
        self.filing_type_code = kwargs.get('filing_type_code', None)
        self.priority = kwargs.get('filing_type_code', None)
        self.filing_type_description = kwargs.get('filing_type_description', None)


class BusinessInfo(Serializable):
    def __init__(self, **kwargs):
        self.business_identifier = kwargs.get('business_identifier', None)
        self.business_name = kwargs.get('business_name', None)
        self.contact_info = kwargs.get('contact_info', None)


class ContactInfo(Serializable):
    def __init__(self, **kwargs):
        self.first_name = kwargs.get('first_name', None)
        self.last_name = kwargs.get('last_name', None)
        self.address = kwargs.get('address', None)
        self.city = kwargs.get('city', None)
        self.province = kwargs.get('province', None)
        self.postal_code = kwargs.get('postal_code', None)


class PaymentRequest(Serializable):
    """
    Sample request:
    {
        "payment_info": {
            "method_of_payment": "CC"
        },
        "business_info": {
            "business_identifier": "CP1234567",
            "corp_type": "CP",
            "business_name": "ABC Corp",
            "contact_info": {
                "city": "Victoria",
                "postal_code": "V8P2P2",
                "province": "BC",
                "address_line1": "100 Douglas Street",
                "country": "CA"
            }
        },
        "filing_info": {
            "filing_types": [
                {
                    "filing_type_code": "OTADD",
                    "filing_description": "TEST"
                },
                {
                    "filing_type_code": "OTANN"
                }
            ]
        }
    }
    """
    def __init__(self, **kwargs):
        self.payment_info = kwargs.get('payment_info')
        self.filing_info = kwargs.get('filing_info')
        self.business_info = kwargs.get('business_info')


class GetPaymentRequest(Serializable):
    def __init__(self, **kwargs):
        self.payment_identifier = kwargs.get('payment_identifier')


def get_payment(payment_identifier):
    # Create an instance of the API class
    api_instance = openapi_client.PaymentsApi()
    # Set API host URI
    api_instance.api_client.configuration.host = PAYMENTS_API_HOST

    try:
        # Get Payment
        api_response = api_instance.get_payment(payment_identifier)

        pprint(api_response)
        return api_response

    except Exception as e:
        print("Exception when calling PaymentsApi->get_payment: %s\n" % e)


def create_payment(model):
    # Create an instance of the API class
    api_instance = openapi_client.PaymentsApi()
    # Set API host URI
    api_instance.api_client.configuration.host = PAYMENTS_API_HOST

    try:
        # Create payment records
        api_response = api_instance.create_payment(model)

        pprint(api_response)
        return api_response

    except Exception as e:
        print("Exception when calling PaymentsApi->create_payment: %s\n" % e)


def update_payment(payment_identifier, model):
    # Create an instance of the API class
    api_instance = openapi_client.PaymentsApi()
    # Set API host URI
    api_instance.api_client.configuration.host = PAYMENTS_API_HOST

    try:
        # Update payment records
        api_response = api_instance.update_payment(payment_identifier, model)

        pprint(api_response)
        return api_response

    except Exception as e:
        print("Exception when calling PaymentsApi->update_payment: %s\n" % e)
