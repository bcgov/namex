from __future__ import print_function
from pprint import pprint

import openapi_client
from openapi_client.rest import ApiException

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

    try:
        # Create a transaction
        api_response = api_instance.create_transaction(
            req.payment_identifier,
            req.redirect_uri
        )

        pprint(api_response)
        return api_response

    except ApiException as e:
        print("Exception when calling TransactionsApi->create_transaction: %s\n" % e)


def get_transaction(req):
    # Create an instance of the API class
    api_instance = openapi_client.TransactionsApi()

    try:
        # Get Transaction
        api_response = api_instance.get_transaction(
            req.receipt_number,
            req.payment_identifier,
            req.transaction_identifier
        )

        pprint(api_response)
        return api_response

    except ApiException as e:
        print("Exception when calling TransactionsApi->get_transaction: %s\n" % e)


def get_transactions(req):
    # Create an instance of the API class
    api_instance = openapi_client.TransactionsApi()

    try:
        # Get Transactions
        api_response = api_instance.get_transactions(
            req.payment_identifier
        )

        pprint(api_response)
        return api_response

    except ApiException as e:
        print("Exception when calling TransactionsApi->get_transactions: %s\n" % e)


def update_transaction(req):
    # Create an instance of the API class
    api_instance = openapi_client.TransactionsApi()

    try:
        # Update a transaction
        api_response = api_instance.update_transaction(
            req.payment_identifier,
            req.receipt_number,
            req.transaction_identifier
        )

        pprint(api_response)
        return api_response

    except ApiException as e:
        print("Exception when calling TransactionsApi->update_transaction: %s\n" % e)
