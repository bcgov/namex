import json

import requests
from flask import current_app, jsonify, make_response
from flask_restx import Namespace, Resource, cors

from namex.utils.api_resource import handle_exception
from namex.utils.auth import MSG_CLIENT_CREDENTIALS_REQ_FAILED, cors_preflight, get_client_credentials
from namex.utils.logging import setup_logging


setup_logging()  # Important to do this first

MSG_BAD_REQUEST_NO_JSON_BODY = 'No JSON data provided'
MSG_SERVER_ERROR = 'Server Error!'
MSG_NOT_FOUND = 'Resource not found'
MSG_COULD_NOT_FIND_CORP = 'Error: Could not find corporation details'


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


@cors_preflight('GET')
@colin_api.route('/<string:corp_num>', strict_slashes=False, methods=['GET', 'OPTIONS'])
@colin_api.doc(params={
    'corp_num': 'Incorporation Number - This field is required'
})
class ColinApi(Resource):
    def get(self, corp_num):
        colin_url = f'{current_app.config.get("COLIN_SVC_URL")}/businesses/{corp_num}/public'
        response = _init(colin_url)

        business_info = response.get('business', {})

        response_dict = {
            'identifier': business_info.get('identifier', corp_num),
            'legalName': business_info.get('legalName'),
            'legalType': business_info.get('legalType'),
            'corpState': business_info.get('corpStateClass'),
            'status': business_info.get('status'),
            'jurisdiction': business_info.get('jurisdiction'),
            'homeIdentifier': business_info.get('homeJurisdictionNumber')
        }

        return make_response(jsonify(response_dict), 200)


def _init(colin_url):
    try:
        SBC_SVC_AUTH_URL = current_app.config.get('SBC_SVC_AUTH_URL', '')
        SBC_SVC_AUTH_CLIENT_ID = current_app.config.get('SBC_SVC_AUTH_CLIENT_ID', '')
        SBC_SVC_CLIENT_SECRET = current_app.config.get('SBC_SVC_CLIENT_SECRET', '')
        authenticated, token = get_client_credentials(SBC_SVC_AUTH_URL, SBC_SVC_AUTH_CLIENT_ID, SBC_SVC_CLIENT_SECRET)
        if not authenticated:
            raise ColinServiceException(message=MSG_CLIENT_CREDENTIALS_REQ_FAILED)

        # Get the profile
        headers = {
            'Authorization': 'Bearer ' + token
        }

        response = requests.get(
            colin_url,
            headers=headers
        )

        if response.status_code != 200:
            raise ColinServiceException(message="Failed to fetch data", status_code=response.status_code)
        return response.json()
    except ColinServiceException as err:
        return handle_exception(err, err.message, err.status_code)
    except Exception as err:
        return handle_exception(err, 'Internal Server Error', 500)
