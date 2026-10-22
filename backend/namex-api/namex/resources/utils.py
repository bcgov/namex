import requests
from dateutil import parser
from flask import current_app

from namex.exceptions import EntityServiceException
from namex.utils.auth import get_client_credentials


class DateUtils:
    @staticmethod
    def parse_date(date_str):
        return parser.parse(date_str)

    @staticmethod
    def parse_date_string(date_str, output_date_format):
        parsed_date = parser.parse(date_str)
        return parsed_date.strftime(output_date_format)


class EntityUtils:
    @staticmethod
    def get_entity_token():
        """Retrieve the authentication token for the entity service."""
        auth_url = current_app.config.get('ENTITY_SVC_AUTH_URL', '')
        client_id = current_app.config.get('ENTITY_SERVICE_ACCOUNT_CLIENT_ID', '')
        client_secret = current_app.config.get('ENTITY_SERVICE_ACCOUNT_CLIENT_SECRET', '')

        authenticated, token = get_client_credentials(auth_url, client_id, client_secret)
        if not authenticated:
            raise EntityServiceException('Client credentials request failed.')
        return token

    @staticmethod
    def make_authenticated_request(endpoint):
        """Make an authenticated GET request to the given endpoint."""
        token = EntityUtils.get_entity_token()
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

        response = requests.get(endpoint, headers=headers)
        return response
