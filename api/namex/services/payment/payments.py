from __future__ import print_function
from pprint import pprint

import openapi_client
from openapi_client.rest import ApiException

from .request_objects.abstract import Serializable


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
    def __init__(self, **kwargs):
        self.payment_identifier = kwargs.get('payment_identifier', None)
        self.payment_info = kwargs.get('payment_info')
        self.filing_info = kwargs.get('filing_info')
        self.business_info = kwargs.get('business_info')


class GetPaymentRequest(Serializable):
    def __init__(self, **kwargs):
        self.payment_identifier = kwargs.get('payment_identifier')


def get_payment(req):
    # Create an instance of the API class
    api_instance = openapi_client.PaymentsApi()

    try:
        # Get Payment
        api_response = api_instance.get_payment(
            req.payment_identifier
        )

        pprint(api_response)
        return api_response

    except ApiException as e:
        print("Exception when calling PaymentsApi->get_payment: %s\n" % e)


def create_payment(req):
    # Create an instance of the API class
    api_instance = openapi_client.PaymentsApi()

    payment_request = {"paymentInfo": {"methodOfPayment": "CC"},
                       "businessInfo": {"businessIdentifier": "CP1234567", "corpType": "CP", "businessName": "ABC Corp",
                                        "contactInfo": {"city": "Victoria", "postal_code": "V8P2P2", "province": "BC",
                                                        "addressLine1": "100 Douglas Street", "country": "CA"}},
                       "filingInfo": {"filingTypes": [{"filingTypeCode": "OTADD", "filingDescription": "TEST"},
                                                      {"filingTypeCode": "OTANN"}]}}  # PaymentRequest

    try:
        # Create payment records
        api_response = api_instance.create_payment(
            req.payment_request
        )

        pprint(api_response)
        return api_response

    except ApiException as e:
        print("Exception when calling PaymentsApi->create_payment: %s\n" % e)


def update_payment(req):
    # Create an instance of the API class
    api_instance = openapi_client.PaymentsApi()

    payment_request = {"paymentInfo": {"methodOfPayment": "CC"},
                       "businessInfo": {"businessIdentifier": "CP1234567", "corpType": "CP", "businessName": "ABC Corp",
                                        "contactInfo": {"city": "Victoria", "postalCode": "V8P2P2", "province": "BC",
                                                        "addressLine1": "100 Douglas Street", "country": "CA"}},
                       "filingInfo": {"filingTypes": [{"filingTypeCode": "OTADD", "filingDescription": "TEST"},
                                                      {"filingTypeCode": "OTANN"}]}}  # PaymentRequest

    try:
        # Update payment records
        api_response = api_instance.update_payment(
            req.payment_identifier,
            req.payment_request
        )

        pprint(api_response)
        return api_response

    except ApiException as e:
        print("Exception when calling PaymentsApi->update_payment: %s\n" % e)
