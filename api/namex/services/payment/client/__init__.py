import json
import os
import tempfile
from enum import Enum
from functools import wraps

import requests
from flask import current_app


MSG_CLIENT_CREDENTIALS_REQ_FAILED = 'Client credentials request failed'
MSG_INVALID_HTTP_VERB = 'Invalid HTTP verb'


class ApiClientException(Exception):
    def __init__(self, wrapped_err=None, body=None, message='Exception', status_code=500):
        self.body = body
        self.err = wrapped_err
        if wrapped_err:
            self.message = '{msg}\r\n\r\n{desc}'.format(msg=message, desc=str(wrapped_err))
        else:
            self.message = message
        # Map HTTP status if the wrapped error has an HTTP status code
        self.status_code = wrapped_err.status if wrapped_err and hasattr(wrapped_err, 'status') else status_code
        super().__init__(self.message)


class ApiClientError(ApiClientException):
    def __init__(self, wrapped_err=None, message='API client error'):
        super().__init__(wrapped_err, message)


class ApiRequestError(Exception):
    def __init__(self, response=None, message='API request failed'):
        self.status_code = response.status_code
        info = json.loads(response.text)
        self.detail = detail = info.get('detail')
        self.title = title = info.get('title')
        self.invalid_params = info.get('invalidParams')

        error_msg = None
        if title and detail and (title != detail):
            error_msg = '{title}: {detail}'.format(title=self.title, detail=self.detail)
        if title and not detail or (title and title == detail):
            error_msg = '{title}'.format(title=title)
        else:
            error_msg = message

        super().__init__(error_msg)


class ApiAuthError(Exception):
    def __init__(self, response=None, message='API authentication error'):
        super().__init__(response, response.get('error_description', message))


def with_authentication(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        PAYMENT_SVC_AUTH_URL = current_app.config.get('PAYMENT_SVC_AUTH_URL')
        PAYMENT_SVC_AUTH_CLIENT_ID = current_app.config.get('PAYMENT_SVC_AUTH_CLIENT_ID')
        PAYMENT_SVC_CLIENT_SECRET = current_app.config.get('PAYMENT_SVC_CLIENT_SECRET')

        authenticated, token = self.get_client_credentials(
            PAYMENT_SVC_AUTH_URL, PAYMENT_SVC_AUTH_CLIENT_ID, PAYMENT_SVC_CLIENT_SECRET
        )
        if not authenticated:
            raise ApiAuthError(message=MSG_CLIENT_CREDENTIALS_REQ_FAILED)
        self.set_api_client_auth_header(token)
        # Set API host URI
        self.set_api_client_request_host(current_app.config.get('PAYMENT_SVC_URL'))
        return func(self, *args, **kwargs)

    return wrapper


def log_api_error_response(err, func_call_name='function'):
    current_app.logger.error('Error when calling {func}'.format(func=func_call_name))


class HttpVerbs(Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'
    PATCH = 'patch'
    OPTIONS = 'options'
    HEAD = 'head'


class ClientConfig:
    def __init__(self, config=None):
        if config:
            self.host = config.get('host', '')
            self.prefix = config.get('prefix', '')
            self.temp_path = config.get('temp_path', '')

    """
    The host name
    """
    _host = None
    """
    Versioning prefix like /api/v1 or whatever
    """
    _prefix = None
    """
    Temp path for file downloads
    """
    _temp_path = None

    @property
    def host(self):
        return self._host if self._host else ''

    @host.setter
    def host(self, val):
        self._host = val

    @property
    def prefix(self):
        return self._prefix if self._prefix else ''

    @prefix.setter
    def prefix(self, val):
        self._prefix = val

    @property
    def temp_path(self):
        return self._temp_path

    @temp_path.setter
    def temp_path(self, val):
        self._temp_path = val


class BaseClient:
    def __init__(self, **kwargs):
        self.configuration = kwargs.get(
            'configuration',
            ClientConfig(
                {
                    'host': current_app.config.get('PAYMENT_SVC_URL'),
                    'prefix': current_app.config.get('PAYMENT_SVC_VERSION', '/api/v1'),
                    'temp_path': None,
                }
            ),
        )
        self.headers = {}

    @staticmethod
    def get_client_credentials(auth_url, client_id, secret):
        auth = requests.post(
            auth_url,
            auth=(client_id, secret),
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': secret},
        )

        # Return the auth response if an error occurs
        if auth.status_code != 200:
            # TODO: This is mocked out
            # return True, 'asdf-asdf-asdf-adsf'
            return False, auth.json()

        token = dict(auth.json())['access_token']
        return True, token

    def set_api_client_auth_header(self, token):
        self.set_api_client_request_header('Authorization', 'Bearer ' + token)

    def set_api_client_request_header(self, key, value):
        self.set_default_header(key, value)

    def set_api_client_request_host(self, url):
        # Set API host URI
        self.configuration.host = url

    def set_api_client_request_prefix(self, url):
        # Set API prefix
        self.configuration.prefix = url

    def set_api_client_temp_path(self, url):
        # Set API prefix
        self.configuration.temp_path = url

    def set_default_header(self, key, val):
        self.headers[key] = val

    def build_url(self, path):
        if self.configuration.prefix:
            return self.configuration.host + self.configuration.prefix + '/' + path
        return self.configuration.host + '/' + path

    def call_api(self, method, url, params=None, data=None, headers=None):
        try:
            if method not in HttpVerbs:
                raise ApiClientError(message=MSG_INVALID_HTTP_VERB)
            if not headers or 'Authorization' not in headers:
                PAYMENT_SVC_AUTH_URL = current_app.config.get('PAYMENT_SVC_AUTH_URL')
                PAYMENT_SVC_AUTH_CLIENT_ID = current_app.config.get('PAYMENT_SVC_AUTH_CLIENT_ID')
                PAYMENT_SVC_CLIENT_SECRET = current_app.config.get('PAYMENT_SVC_CLIENT_SECRET')
                authenticated, token = self.get_client_credentials(
                    PAYMENT_SVC_AUTH_URL, PAYMENT_SVC_AUTH_CLIENT_ID, PAYMENT_SVC_CLIENT_SECRET
                )
                if not authenticated:
                    raise ApiAuthError(token, message=MSG_CLIENT_CREDENTIALS_REQ_FAILED)
                headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

            if type(headers.get('Account-Id', '')) != str:
                headers['Account-Id'] = str(headers['Account-Id'])

            url = self.build_url(url)
            if data:
                response = requests.request(
                    method.value,
                    url,
                    params=params,
                    # Dump and load to serialize dates
                    json=json.loads(json.dumps(data, default=str)) if data else None,
                    headers=headers,
                )
            else:
                response = requests.request(method.value, url, params=params, headers=headers)

            if not response or not response.ok:
                raise ApiRequestError(response)

            if response and response.headers.get('Content-Type') == 'application/json':
                return json.loads(response.text)
            elif response and response.headers.get('Content-Type') == 'application/pdf':
                return self.deserialize_file(response)
        except (ApiRequestError, ApiAuthError, ApiClientError) as err:
            log_api_error_response(err, func_call_name='call_api {method} ({url})'.format(url=url, method=method.value))
            raise err

        except Exception as ex:
            raise ex

    def deserialize_file(self, response):
        """
        Deserializes body to file
        Saves response body into a file in a temporary folder.
        :param response:
        :return: str File path
        """
        fd, path = tempfile.mkstemp(dir=self.configuration.temp_path)
        os.close(fd)
        os.remove(path)

        with open(path, 'wb') as f:
            f.write(response.content)

        return path


class SBCPaymentClient(BaseClient):
    def calculate_fees(self, corp_type, filing_type_code, jurisdiction=None, date=None, priority=None, headers=None):
        request_url = 'fees/{corp_type}/{filing_type_code}'
        request_url = request_url.format(corp_type=corp_type, filing_type_code=filing_type_code)

        params = {}
        if jurisdiction:
            params['jurisdiction'] = jurisdiction
        if date:
            params['date'] = date
        if priority:
            params['priority'] = priority

        return self.call_api(HttpVerbs.GET, request_url, params=params, headers=headers)

    def create_payment(self, data, headers=None):
        request_url = 'payment-requests'
        return self.call_api(HttpVerbs.POST, request_url, data=data, headers=headers)

    def get_payment(self, invoice_id, headers=None):
        request_url = 'payment-requests/{invoice_id}'
        request_url = request_url.format(invoice_id=invoice_id)
        return self.call_api(HttpVerbs.GET, request_url, headers=headers)

    def refund_payment(self, invoice_id, data):
        request_url = 'payment-requests/{invoice_id}/refunds'
        request_url = request_url.format(invoice_id=invoice_id)
        response = None
        try:
            response = self.call_api(HttpVerbs.POST, request_url, data=data)
        except ApiRequestError:  # ROUTING_SLIP_REFUND and NO_FEE_REFUND return http 400.
            return response

        return response

    def generate_receipt(self, invoice_id, data):
        request_url = 'payment-requests/{invoice_id}/receipts'
        request_url = request_url.format(invoice_id=invoice_id)
        return self.call_api(HttpVerbs.POST, request_url, data=data)

    def get_receipt(self, invoice_id):
        request_url = 'payment-requests/{invoice_id}/receipts'
        request_url = request_url.format(invoice_id=invoice_id)
        return self.call_api(HttpVerbs.GET, request_url)

    def cancel_payment(self, invoice_id):
        request_url = 'payment-requests/{invoice_id}'
        request_url = request_url.format(invoice_id=invoice_id)
        return self.call_api(HttpVerbs.DELETE, request_url)
