import json

import requests
from flask import current_app, jsonify
from flask_restx import Namespace, Resource, cors

from namex.utils.api_resource import handle_exception
from namex.utils.auth import MSG_CLIENT_CREDENTIALS_REQ_FAILED, cors_preflight, get_client_credentials
from namex.utils.logging import setup_logging


setup_logging()  # Important to do this first

MSG_BAD_REQUEST_NO_JSON_BODY = 'No JSON data provided'
MSG_SERVER_ERROR = 'Server Error!'
MSG_NOT_FOUND = 'Resource not found'

class ColinServiceException(Exception):
    def __init__(self, wrapped_err=None, message="COLIN API exception.", status_code=500):
        self.err = wrapped_err
        self.colin_error_code = None
        self.status_code = status_code

        if wrapped_err and hasattr(wrapped_err, 'status'):
            # Map HTTP status if the wrapped error has an HTTP status code
            self.status_code = wrapped_err.status if wrapped_err.status else status_code

        if wrapped_err and hasattr(wrapped_err, 'error_code'):
            # Map COLIN error code if the wrapped error has a COLIN error code
            self.error_code = int(wrapped_err.error_code)

        if wrapped_err and hasattr(wrapped_err, 'internal_error_code'):
            # Map COLIN error code if the wrapped error has a COLIN error code
            self.colin_error_code = int(wrapped_err.internal_error_code)

        if self.colin_error_code is not None:
            self.message = message if message else str(self.colin_error_code) + ': ' + wrapped_err['internal_error_message']
        elif wrapped_err:
            self.message = '{msg}\r\n\r\n{desc}'.format(msg=message, desc=str(wrapped_err))
        else:
            self.message = message

        super().__init__(self.message)


# Register a local namespace for the NR reserve
colin_api = Namespace('colin', description='COLIN API')


@cors_preflight('POST, GET')
@colin_api.route('/<string:corp_num>', strict_slashes=False, methods=['POST', 'OPTIONS'])
@colin_api.route('/<string:corp_num>', strict_slashes=False, methods=['GET', 'OPTIONS'])
@colin_api.doc(params={
    'corp_num': 'Incorporation Number - This field is required'
})
class ColinApi(Resource):
    @cors.crossdomain(origin='*')
    def post(self, corp_num):
        colin_url = f'{current_app.config.get("COLIN_SVC_URL")}/corporations/{corp_num}'
        response, status_code = _init(colin_url, corp_num)
        return response, status_code

    def get(self, corp_num):
        colin_url = f'{current_app.config.get("COLIN_SVC_URL")}/corporations/business/{corp_num}'
        response, status_code = _init(colin_url, corp_num)
        return response, status_code

def _init(colin_url, corp_num):
    try:
        SBC_SVC_AUTH_URL = current_app.config.get('SBC_SVC_AUTH_URL', '')
        SBC_SVC_AUTH_CLIENT_ID = current_app.config.get('SBC_SVC_AUTH_CLIENT_ID', '')
        SBC_SVC_CLIENT_SECRET = current_app.config.get('SBC_SVC_CLIENT_SECRET', '')
        authenticated, token = get_client_credentials(SBC_SVC_AUTH_URL, SBC_SVC_AUTH_CLIENT_ID, SBC_SVC_CLIENT_SECRET)
        if not authenticated:
            raise ColinServiceException(message=MSG_CLIENT_CREDENTIALS_REQ_FAILED)

        # Get the profile
        print(f'\nCalling COLIN API using [corp_num: {corp_num}]')
        headers = {
            # 'x-api-key': COLIN_SVC_API_KEY,
            # 'Accept': 'application/xml'
            'Authorization': 'Bearer ' + token
        }

        print(colin_url)
        print(repr(headers))
        response = requests.get(
            colin_url,
            headers=headers
        )

        content = json.loads(response.text)
        if response.status_code != 200:
            return jsonify(content.get('message')), response.status_code
        return jsonify(content), response.status_code
    except ColinServiceException as err:
        return handle_exception(err, err.message, err.status_code)
    except Exception as err:
        return handle_exception(err, 'Internal Server Error', 500)
