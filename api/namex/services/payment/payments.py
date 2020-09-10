from __future__ import print_function
from pprint import pprint

import openapi_client
# Other stuff you can import...
# from openapi_client.models import Payment
# from openapi_client.rest import ApiException

from namex.utils.auth import get_client_credentials, MSG_CLIENT_CREDENTIALS_REQ_FAILED

from . import PAYMENT_SVC_URL, PAYMENT_SVC_AUTH_URL, PAYMENT_SVC_AUTH_CLIENT_ID, PAYMENT_SVC_CLIENT_SECRET
from .utils import set_api_client_auth_header, set_api_client_request_host
from .exceptions import SBCPaymentException, SBCPaymentError, PaymentServiceError

from .request_objects.abstract import Serializable


class Payment(Serializable):
    """
    Sample request:
    {
        "paymentInfo": {
            "methodOfPayment": "CC"
        },
        "businessInfo": {
            "businessIdentifier": "CP1234567",
            "corpType": "NRO",
            "businessName": "ABC Corp",
            "contactInfo": {
                "city": "Victoria",
                "postalCode": "V8P2P2",
                "province": "BC",
                "addressLine1": "100 Douglas Street",
                "country": "CA"
            }
        },
        "filingInfo": {
            "filingTypes": [
                {
                    "filingTypeCode": "ABC",
                    "filingDescription": "TEST"
                },
                {
                    "filingTypeCode": "ABC"
                    ...
                }
            ]
        }
    }
    """
    def __init__(self, **kwargs):
        self.paymentInfo = kwargs.get('paymentInfo')
        self.filingInfo = kwargs.get('filingInfo')
        self.businessInfo = kwargs.get('businessInfo')


class PaymentInfo(Serializable):
    def __init__(self, **kwargs):
        self.methodOfPayment = kwargs.get('methodOfPayment', None)


class FilingInfo(Serializable):
    def __init__(self, **kwargs):
        self.corpType = kwargs.get('corpType', None)
        self.date = kwargs.get('date', None)
        self.filingTypes = kwargs.get('filingTypes', None)


class FilingType(Serializable):
    def __init__(self, **kwargs):
        self.filingTypeCode = kwargs.get('filingTypeCode', None)
        self.priority = kwargs.get('filingTypeCode', None)
        self.filingTypeDescription = kwargs.get('filingTypeDescription', None)


class BusinessInfo(Serializable):
    def __init__(self, **kwargs):
        self.businessIdentifier = kwargs.get('businessIdentifier', None)
        self.businessName = kwargs.get('businessName', None)
        self.contactInfo = kwargs.get('contactInfo', None)


class ContactInfo(Serializable):
    def __init__(self, **kwargs):
        self.firstName = kwargs.get('firstName', None)
        self.lastName = kwargs.get('lastName', None)
        self.address = kwargs.get('address', None)
        self.city = kwargs.get('city', None)
        self.province = kwargs.get('province', None)
        self.postalCode = kwargs.get('postalCode', None)


class GetPaymentRequest(Serializable):
    def __init__(self, **kwargs):
        self.payment_identifier = kwargs.get('payment_identifier')


class CreatePaymentRequest(Payment):
    pass


class UpdatePaymentRequest(Payment):
    pass


def get_payment(payment_identifier):
    # Create an instance of the API class
    api_instance = openapi_client.PaymentsApi()

    authenticated, token = get_client_credentials(PAYMENT_SVC_AUTH_URL, PAYMENT_SVC_AUTH_CLIENT_ID, PAYMENT_SVC_CLIENT_SECRET)
    if not authenticated:
        raise SBCPaymentException(MSG_CLIENT_CREDENTIALS_REQ_FAILED)
    set_api_client_auth_header(api_instance, token)

    # Set API host URI
    set_api_client_request_host(api_instance, PAYMENT_SVC_URL)

    try:
        # Get Payment
        api_response = api_instance.get_payment(payment_identifier)

        pprint(api_response)
        return api_response

    except Exception as e:
        print("Exception when calling PaymentsApi->get_payment: %s\n" % e)
        raise


def create_payment(model):
    # Create an instance of the API class
    api_instance = openapi_client.PaymentsApi()

    authenticated, token = get_client_credentials(PAYMENT_SVC_AUTH_URL, PAYMENT_SVC_AUTH_CLIENT_ID, PAYMENT_SVC_CLIENT_SECRET)
    if not authenticated:
        raise SBCPaymentException(MSG_CLIENT_CREDENTIALS_REQ_FAILED)
    set_api_client_auth_header(api_instance, token)

    # Set API host URI
    set_api_client_request_host(api_instance, PAYMENT_SVC_URL)

    try:
        # Create payment records
        api_response = api_instance.create_payment(model)

        pprint(api_response)
        return api_response

    except Exception as e:
        print("Exception when calling PaymentsApi->create_payment: %s\n" % e)
        raise


def update_payment(payment_identifier, model):
    # Create an instance of the API class
    api_instance = openapi_client.PaymentsApi()

    authenticated, token = get_client_credentials(PAYMENT_SVC_AUTH_URL, PAYMENT_SVC_AUTH_CLIENT_ID, PAYMENT_SVC_CLIENT_SECRET)
    if not authenticated:
        raise SBCPaymentException(MSG_CLIENT_CREDENTIALS_REQ_FAILED)
    set_api_client_auth_header(api_instance, token)

    # Set API host URI
    set_api_client_request_host(api_instance, PAYMENT_SVC_URL)

    try:
        # Update payment records
        api_response = api_instance.update_payment(payment_identifier, model)

        pprint(api_response)
        return api_response

    except Exception as e:
        print("Exception when calling PaymentsApi->update_payment: %s\n" % e)
        raise
