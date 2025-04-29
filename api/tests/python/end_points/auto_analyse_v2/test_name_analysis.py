# Copyright © 2020 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Provides end points to submit, retrieve and cancel a name analysis request.
"""

from http import HTTPStatus
from unittest.mock import patch

import requests

from .configuration import ENDPOINT_PATH


class MockResponse:
    """Mock response class"""

    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        """Returns the json."""
        return self.json_data


def test_auto_analyze_post(client):
    """Test to ensure that post endpoint works as expected."""
    headers = {'content-type': 'application/json'}
    request_json = {'name': 'ADEA HEATING INC.', 'location': 'BC', 'entity_type_cd': 'CR', 'request_action_cd': 'NEW'}
    post_name_analysis_response = {
        'header': {'uuid': 'sdf321421344', 'state': 'running', 'processed': 10, 'total': 200},
        'analysis': {'issues': []},
    }
    mock_response = MockResponse(post_name_analysis_response, HTTPStatus.CREATED)
    with patch.object(requests, 'post', return_value=mock_response):
        response = client.post(ENDPOINT_PATH, json=request_json, headers=headers)
        response_json = response.json
        assert response.status_code == HTTPStatus.CREATED
        assert response_json['header']
        assert response_json['header']['state']
        assert response_json['header']['processed']
        assert response_json['header']['total']
        assert response_json['analysis']


def test_auto_analyze_get(client):
    """Test to ensure that get endpoint works as expected."""
    identifier = 'sdf321421344'
    get_name_analysis_response = {
        'header': {'uuid': identifier, 'state': 'completed', 'processed': 200, 'total': 200},
        'analysis': {'header': 'Available', 'status': 'Available', 'issues': []},
    }
    mock_response = MockResponse(get_name_analysis_response, HTTPStatus.OK)
    with patch.object(requests, 'get', return_value=mock_response):
        response = client.get(f'{ENDPOINT_PATH}/{identifier}')
        response_json = response.json
        assert response.status_code == HTTPStatus.OK
        assert response_json['header']
        assert response_json['header']['state']
        assert response_json['header']['processed']
        assert response_json['header']['total']
        assert response_json['analysis']


def test_auto_analyze_delete(client):
    """Test to ensure that delete endpoint works as expected."""
    identifier = 'sdf321421344'
    delete_name_analysis_response = {}
    mock_response = MockResponse(delete_name_analysis_response, HTTPStatus.OK)
    with patch.object(requests, 'delete', return_value=mock_response):
        response = client.delete(f'{ENDPOINT_PATH}/{identifier}')
        assert response.status_code == HTTPStatus.OK
