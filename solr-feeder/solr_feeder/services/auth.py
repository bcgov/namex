# Copyright © 2022 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This manages all of the authentication and authorization service."""
import logging
from http import HTTPStatus
from typing import Tuple

import requests
from requests import exceptions
from flask import current_app


def get_bearer_token() -> Tuple[str, dict]:
    """Get a valid Bearer token for the service to use."""
    token_url = current_app.config.get('KEYCLOAK_AUTH_TOKEN_URL')
    client_id = current_app.config.get('KEYCLOAK_SERVICE_ACCOUNT_ID')
    client_secret = current_app.config.get('KEYCLOAK_SERVICE_ACCOUNT_SECRET')
    auth_api_timeout = current_app.config.get('AUTH_API_TIMEOUT')

    data = 'grant_type=client_credentials'

    # get service account token
    try:
        res = requests.post(url=token_url,
                            data=data,
                            headers={'content-type': 'application/x-www-form-urlencoded'},
                            auth=(client_id, client_secret),
                            timeout=auth_api_timeout)
        if res.status_code != HTTPStatus.OK:
            return None, {'message': res.json(), 'status_code': res.status_code}

        return res.json().get('access_token'), None
    except (exceptions.ConnectionError, exceptions.Timeout) as err:
        logging.error('AUTH api connection failure: %s', err)
        return None, {'message': 'AUTH connection failure', 'status_code': HTTPStatus.GATEWAY_TIMEOUT}
    except Exception as err:  # noqa: B902
        logging.error('AUTH service failure: %s', err.with_traceback(None))
        return None, {'message': 'AUTH service error', 'status_code': HTTPStatus.INTERNAL_SERVER_ERROR}
