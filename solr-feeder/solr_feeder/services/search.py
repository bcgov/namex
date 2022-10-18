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
"""Manages search-api interactions."""
import logging
from http import HTTPStatus
from typing import Dict

import requests
from requests import exceptions
from flask import current_app

from .auth import get_bearer_token


def update_search(payload: Dict[str, str]):
    """Update the registries search solr core."""
    try:
        token, error = get_bearer_token()
        if error:
            return error
        headers = {'Authorization': 'Bearer ' + token}
        solr_update_url = f'{current_app.config["SEARCH_API_URL"]}/internal/solr/update'
        timeout = current_app.config["SEARCH_API_TIMEOUT"]
        res = requests.put(url=solr_update_url, headers=headers, json=payload, timeout=timeout)
        if res.status_code != HTTPStatus.OK:
            return {'message': res.json(), 'status_code': res.status_code}

    except (exceptions.ConnectionError, exceptions.Timeout) as err:
        logging.error('SEARCH connection failure %s', err)
        return {'message': 'SEARCH connection failure.', 'status_code': HTTPStatus.GATEWAY_TIMEOUT}
    except Exception as err:  # noqa: B902
        logging.error('SEARCH service error %s', err.with_traceback(None))
        return {'message': 'SEARCH service error.', 'status_code': HTTPStatus.INTERNAL_SERVER_ERROR}
