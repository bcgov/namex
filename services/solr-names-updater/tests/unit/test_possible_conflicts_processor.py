# Copyright © 2019 Province of British Columbia
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
"""Tests to ensure possible conflicts processors function as intended."""
from unittest.mock import patch
import requests

import pytest

from solr_names_updater import worker  # noqa: I001
from solr_names_updater.names_processors.names import get_nr_ids_to_delete_from_solr

from . import create_queue_mock_message, create_nr, MockResponse, create_message  # noqa: I003


# todo add test for adding conflicts when details of what event triggers adding a possible conflicts
#  to solr is sorted out

@pytest.mark.parametrize(
    ['message_payload', 'names', 'names_state'],
    [
        (
            create_message('CANCELLED', 'APPROVED'),
            ['TEST NAME 1', 'TEST NAME 2', 'TEST NAME 3'],
            ['APPROVED', 'CONDITION', 'REJECTED']
        )
    ]
)
async def test_should_delete_possible_conflict_from_solr(
        app,
        db,
        session,
        message_payload,
        names: list,
        names_state: list):
    """Assert that possible conflicts are deleted from Solr."""

    nr_num = message_payload['data']['request']['nrNum']
    nr_new_state = message_payload['data']['request']['newState']
    nr = create_nr(nr_num, nr_new_state, names, names_state)
    mock_msg = create_queue_mock_message(message_payload)
    mock_response = MockResponse({}, 200)

    # mock post method to solr feeder api
    with patch.object(requests, 'post', return_value=mock_response) as mock_solr_feeder_api_post:
        # mock process_names_delete to do nothing in order to isolate testing relevant to this test
        with patch.object(worker, 'process_names_delete', return_value=True):
            await worker.cb_subscription_handler(mock_msg)

            assert mock_solr_feeder_api_post.called == True
            assert 'api/v1/feeds' in mock_solr_feeder_api_post.call_args[0][0]

            post_json = mock_solr_feeder_api_post.call_args[1]['json']
            assert post_json['solr_core']
            assert post_json['solr_core'] == 'possible.conflicts'

            request_json = post_json['request']
            assert f'"delete": ["{nr.nrNum}"]' in request_json
