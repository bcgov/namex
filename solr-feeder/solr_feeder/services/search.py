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

import requests
from requests import exceptions

from .auth import get_bearer_token


def update_search(url: str, payload: dict[str, str], timeout: int, token: str):
    """Update solr core."""
    try:
        headers = {'Authorization': 'Bearer ' + token}

        res = requests.put(url=url, headers=headers, json=payload, timeout=timeout)
        if res.status_code != HTTPStatus.OK:
            return {'message': res.json(), 'status_code': res.status_code}

    except (exceptions.ConnectionError, exceptions.Timeout) as err:
        logging.error('%s connection failure %s', url, err)
        return {'message': f'{url} connection failure.', 'status_code': HTTPStatus.GATEWAY_TIMEOUT}
    except Exception as err:  # noqa: B902
        logging.error('%s service error %s', url, err.with_traceback(None))
        return {'message': f'{url} service error.', 'status_code': HTTPStatus.INTERNAL_SERVER_ERROR}
