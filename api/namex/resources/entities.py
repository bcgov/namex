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


class EntityServiceException(Exception):
    """get business info"""

    def __init__(self, wrapped_err=None, message="Entity API exception.", status_code=500):
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
entity_api = Namespace('entity', description='ENTITY API')


@cors_preflight('GET')
@entity_api.route('/<string:corp_num>', methods=['GET', 'OPTIONS'])
@entity_api.doc(params={
    'corp_num': 'Incorporation Number - This field is required'
})
class EntityApi(Resource):
    def get(self, corp_num):
        try:
            auth_url = current_app.config.get('ENTITY_SVC_AUTH_URL', '')
            entity_auth_client_id = current_app.config.get('ENTITY_SERVICE_ACCOUNT_CLIENT_ID', '')
            entity_client_secret = current_app.config.get('ENTITY_SERVICE_ACCOUNT_CLIENT_SECRET', '')
            authenticated, token = get_client_credentials(auth_url, entity_auth_client_id, entity_client_secret)
            if not authenticated:
                raise EntityServiceException(message=MSG_CLIENT_CREDENTIALS_REQ_FAILED)

            # Get the profile
            entity_url = f'{current_app.config.get("ENTITY_SVC_URL")}/businesses/{corp_num}'
            headers = {
                'Authorization': 'Bearer ' + token
            }

            response = requests.get(
                entity_url,
                headers=headers
            )

            content = json.loads(response.text)
            if response.status_code != 200:
                return make_response(jsonify(content.get('message')), response.status_code)
            return make_response(jsonify(content), response.status_code)
        except EntityServiceException as err:
            return handle_exception(err, err.message, err.status_code)
        except Exception as err:
            return handle_exception(err, 'Internal Server Error', 500)
