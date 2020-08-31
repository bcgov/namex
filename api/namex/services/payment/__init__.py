import os

PAYMENT_SVC_URL = os.getenv('PAYMENT_SVC_URL')

PAYMENT_SVC_AUTH_URL = os.getenv('PAYMENT_SVC_AUTH_URL')
PAYMENT_SVC_AUTH_CLIENT_ID = os.getenv('PAYMENT_SVC_AUTH_CLIENT_ID')
PAYMENT_SVC_CLIENT_SECRET = os.getenv('PAYMENT_SVC_CLIENT_SECRET')


class PaymentServiceException(Exception):
    pass


