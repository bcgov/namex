from __future__ import print_function
from pprint import pprint

import json
import openapi_client
from openapi_client import ApiException
# Other stuff you can import...
# from openapi_client.models import Transaction
# from openapi_client.rest import ApiException

from namex.utils.auth import get_client_credentials, MSG_CLIENT_CREDENTIALS_REQ_FAILED

from . import PAYMENT_SVC_URL, PAYMENT_SVC_AUTH_URL, PAYMENT_SVC_AUTH_CLIENT_ID, PAYMENT_SVC_CLIENT_SECRET
from .utils import set_api_client_auth_header, set_api_client_request_host
from .exceptions import SBCPaymentException, SBCPaymentError, PaymentServiceError

from .request_objects.abstract import Serializable


class CreateTransactionRequest(Serializable):
    def __init__(self, **kwargs):
        self.payment_identifier = kwargs.get('payment_identifier')
        self.redirect_uri = kwargs.get('redirect_uri')


class GetTransactionRequest(Serializable):
    def __init__(self, **kwargs):
        self.payment_identifier = kwargs.get('payment_identifier')
        self.transaction_identifier = kwargs.get('transaction_identifier')
        self.receipt_number = kwargs.get('receipt_number')


class GetTransactionsRequest(Serializable):
    def __init__(self, **kwargs):
        self.payment_identifier = kwargs.get('payment_identifier')


class UpdateTransactionRequest(Serializable):
    def __init__(self, **kwargs):
        self.payment_identifier = kwargs.get('payment_identifier')
        self.transaction_identifier = kwargs.get('transaction_identifier')
        self.receipt_number = kwargs.get('receipt_number')


def create_transaction(req):
    # Create an instance of the API class
    api_instance = openapi_client.TransactionsApi()

    authenticated, token = get_client_credentials(PAYMENT_SVC_AUTH_URL, PAYMENT_SVC_AUTH_CLIENT_ID, PAYMENT_SVC_CLIENT_SECRET)
    if not authenticated:
        raise SBCPaymentException(message=MSG_CLIENT_CREDENTIALS_REQ_FAILED)
    set_api_client_auth_header(api_instance, token)

    # Set API host URI
    set_api_client_request_host(api_instance, PAYMENT_SVC_URL)

    try:
        # Create a transaction
        api_response = api_instance.create_transaction(
            req.payment_identifier,
            req.redirect_uri
        )

        pprint(api_response)
        return api_response

    except ApiException as err:
        print("Exception when calling TransactionsApi->create_transaction: %s\n" % err)
        err_response = json.loads(err.body)
        message = ''
        if err_response.get('detail'):
            message = err_response.get('detail')
        elif err_response.get('message'):
            message = err_response.get('message')
        raise SBCPaymentException(err, message=message)

    except Exception as err:
        print("Exception when calling TransactionsApi->create_transaction: %s\n" % err)
        raise SBCPaymentException(err)


def get_transaction(req):
    # Create an instance of the API class
    api_instance = openapi_client.TransactionsApi()

    authenticated, token = get_client_credentials(PAYMENT_SVC_AUTH_URL, PAYMENT_SVC_AUTH_CLIENT_ID, PAYMENT_SVC_CLIENT_SECRET)
    if not authenticated:
        raise SBCPaymentException(message=MSG_CLIENT_CREDENTIALS_REQ_FAILED)
    set_api_client_auth_header(api_instance, token)

    # Set API host URI
    set_api_client_request_host(api_instance, PAYMENT_SVC_URL)

    try:
        # Get Transaction
        api_response = api_instance.get_transaction(
            req.receipt_number,
            req.payment_identifier,
            req.transaction_identifier
        )

        pprint(api_response)
        return api_response

    except ApiException as err:
        print("Exception when calling TransactionsApi->get_transaction: %s\n" % err)
        err_response = json.loads(err.body)
        message = ''
        if err_response.get('detail'):
            message = err_response.get('detail')
        elif err_response.get('message'):
            message = err_response.get('message')
        raise SBCPaymentException(err, message=message)

    except Exception as err:
        print("Exception when calling TransactionsApi->get_transaction: %s\n" % err)
        raise SBCPaymentException(err)


def get_transactions(req):
    # Create an instance of the API class
    api_instance = openapi_client.TransactionsApi()

    authenticated, token = get_client_credentials(PAYMENT_SVC_AUTH_URL, PAYMENT_SVC_AUTH_CLIENT_ID, PAYMENT_SVC_CLIENT_SECRET)
    if not authenticated:
        raise SBCPaymentException(message=MSG_CLIENT_CREDENTIALS_REQ_FAILED)
    set_api_client_auth_header(api_instance, token)

    # Set API host URI
    set_api_client_request_host(api_instance, PAYMENT_SVC_URL)

    try:
        # Get Transactions
        api_response = api_instance.get_transactions(
            req.payment_identifier
        )

        pprint(api_response)
        return api_response

    except ApiException as err:
        print("Exception when calling TransactionsApi->get_transactions: %s\n" % err)
        err_response = json.loads(err.body)
        message = ''
        if err_response.get('detail'):
            message = err_response.get('detail')
        elif err_response.get('message'):
            message = err_response.get('message')
        raise SBCPaymentException(err, message=message)

    except Exception as err:
        print("Exception when calling TransactionsApi->get_transactions: %s\n" % err)
        raise SBCPaymentException(err)


def update_transaction(req):
    # Create an instance of the API class
    api_instance = openapi_client.TransactionsApi()

    authenticated, token = get_client_credentials(PAYMENT_SVC_AUTH_URL, PAYMENT_SVC_AUTH_CLIENT_ID, PAYMENT_SVC_CLIENT_SECRET)
    if not authenticated:
        raise SBCPaymentException(message=MSG_CLIENT_CREDENTIALS_REQ_FAILED)
    set_api_client_auth_header(api_instance, token)

    # Set API host URI
    set_api_client_request_host(api_instance, PAYMENT_SVC_URL)

    try:
        # Update a transaction
        api_response = api_instance.update_transaction(
            req.payment_identifier,
            req.receipt_number,
            req.transaction_identifier
        )

        pprint(api_response)
        return api_response

    except ApiException as err:
        print("Exception when calling TransactionsApi->update_transaction: %s\n" % err)
        err_response = json.loads(err.body)
        message = ''
        if err_response.get('detail'):
            message = err_response.get('detail')
        elif err_response.get('message'):
            message = err_response.get('message')
        raise SBCPaymentException(err, message=message)

    except Exception as err:
        print("Exception when calling TransactionsApi->update_transaction: %s\n" % err)
        raise SBCPaymentException(err)
