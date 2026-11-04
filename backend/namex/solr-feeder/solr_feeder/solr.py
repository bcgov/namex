# Copyright © 2023 Province of British Columbia
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
"""Manages Namex solr update."""
import os

import requests
from flask import current_app

from solr_feeder.services.auth import get_search_bearer_token
from solr_feeder.utilities.converters import convert_solr_doc

__all__ = ['update_core']

_SOLR_INSTANCE = os.getenv('SOLR_FEEDER_SOLR_INSTANCE', 'http://localhost:8393/solr')
_SOLR_URL = _SOLR_INSTANCE + '/{}/update/json'


def update_core(core_name: str, json_string: str):
    """Update the core with the given data."""
    current_app.logger.debug('json Solr command: %s', json_string)

    converted_request = convert_solr_doc(json_string)

    bearer_token, token_err = get_search_bearer_token()
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json',
    }

    solr_api_url = current_app.config['SOLR_API_URL'].rstrip('/') + '/internal/solr/update'

    resp = requests.put(solr_api_url,
                        json=converted_request,
                        headers=headers
                        )

    if resp.status_code > 299:
        current_app.logger.error('Solr update for ' + json_string + ' failed.')
        current_app.logger.error('Failed to update solr', resp.json())

        return {
            'message': f"{core_name} core: {resp.json()['error']['msg']}",
            'status_code': resp.status_code
        }

    return None
