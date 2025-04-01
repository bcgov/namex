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


__all__ = ['update_core']


_SOLR_INSTANCE = os.getenv('SOLR_FEEDER_SOLR_INSTANCE', 'http://localhost:8393/solr')
_SOLR_URL = _SOLR_INSTANCE + '/{}/update/json'


def update_core(core_name: str, json_string: str):
    """Update the core with the given data."""
    current_app.logger.debug('json Solr command: %s', json_string)

    response = requests.post(_SOLR_URL.format(core_name),
                             data=json_string,
                             timeout=current_app.config['NAMEX_SOLR_TIMEOUT'])

    # By the way, if your request is mangled, Solr will sometimes happily return a 200 with a responseHeader['status']
    # value of 0 (meaning all is good).
    if response.status_code != 200:
        current_app.logger.error('%s core: %s', core_name, response.json())

        return {
            'message': f"{core_name} core: {response.json()['error']['msg']}",
            'status_code': response.status_code
        }

    return None
