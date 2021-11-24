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
"""Tests to ensure names processors function as intended."""
from unittest import mock
from unittest.mock import patch
import requests
import pytest

from namex.models import Request as RequestDAO
from namex.utils import queue_util
from solr_names_updater import worker  # noqa: I001
from solr_names_updater.names_processors.names import get_nr_ids_to_delete_from_solr

from . import create_queue_mock_message, create_nr, MockResponse, create_request_state_change_message # noqa: I003


@pytest.mark.parametrize(
    ['message_payload', 'names', 'names_state', 'expected_names_to_add_to_solr', 'not_expected_names_to_add_to_solr'],
    [
        (
            create_request_state_change_message('APPROVED', 'DRAFT'),
            ['TEST NAME 1', 'TEST NAME 2', 'TEST NAME 3'],
            ['APPROVED', 'CONDITION', 'APPROVED'],
            ['TEST NAME 1', 'TEST NAME 2', 'TEST NAME 3'],
            []
        ),
        (
            create_request_state_change_message('APPROVED', 'DRAFT'),
            ['TEST NAME 1'],
            ['APPROVED'],
            ['TEST NAME 1'],
            []
        ),
        (
            create_request_state_change_message('CONDITIONAL', 'DRAFT'),
            ['TEST NAME 1'],
            ['APPROVED'],
            ['TEST NAME 1'],
            []
        ),
        (
            create_request_state_change_message('APPROVED', 'DRAFT'),
            ['TEST NAME 1', 'TEST NAME 2', 'TEST NAME 3'],
            ['APPROVED', 'NOT_EXAMINED', 'REJECTED'],
            ['TEST NAME 1'],
            ['TEST NAME 2', 'TEST NAME 3']
        ),
        (
            create_request_state_change_message('CANCELLED', 'DRAFT'),
            ['TEST NAME 1'],
            ['APPROVED'],
            [],
            []
        ),
        (
            create_request_state_change_message('EXPIRED', 'DRAFT'),
            ['TEST NAME 1'],
            ['APPROVED'],
            [],
            []
        ),
    ]
)
async def test_should_add_names_to_solr(
        app,
        db,
        session,
        message_payload,
        names: list,
        names_state: list,
        expected_names_to_add_to_solr: list,
        not_expected_names_to_add_to_solr: list):
    """Assert that names are added to solr."""

    queue_util.send_name_request_state_msg = mock.Mock(return_value="True")
    nr_num = message_payload['data']['request']['nrNum']
    nr_new_state = message_payload['data']['request']['newState']
    mock_nr = create_nr(nr_num, nr_new_state, names, names_state)
    mock_msg = create_queue_mock_message(message_payload)
    mock_response = MockResponse({}, 200)

    # mock post method to solr feeder api
    with patch.object(requests, 'post', return_value=mock_response) as mock_solr_feeder_api_post:
        # mock process_names_delete to do nothing in order to isolate testing relevant to this test
        with patch.object(worker, 'process_names_delete', return_value=True):
            # mock process_possible_conflicts_add to do nothing in order to isolate testing relevant to this test
            with patch.object(worker, 'process_possible_conflicts_add', return_value=True):
                # mock process_possible_conflicts_delete to do nothing in order to isolate testing relevant to this test
                with patch.object(worker, 'process_possible_conflicts_delete', return_value=True):
                    # mock find_by_nr to do nothing in order to isolate testing relevant to this test
                    with patch.object(RequestDAO, 'find_by_nr', return_value=mock_nr):
                        await worker.cb_subscription_handler(mock_msg)

                        if len(expected_names_to_add_to_solr) > 0:
                            assert mock_solr_feeder_api_post.called == True
                            assert 'api/v1/feeds' in mock_solr_feeder_api_post.call_args[0][0]

                            post_json = mock_solr_feeder_api_post.call_args[1]['json']
                            assert post_json['solr_core']
                            assert post_json['solr_core'] == 'names'

                            request_json = post_json['request']

                            for index, expect_name in enumerate(expected_names_to_add_to_solr):
                                assert expect_name in request_json

                            for index, not_expect_name in enumerate(not_expected_names_to_add_to_solr):
                                assert not_expect_name not in request_json
                        else:
                            assert mock_solr_feeder_api_post.called == False


@pytest.mark.parametrize(
    ['state_change_type', 'message_payload', 'new_nr_state', 'previous_nr_state', 'names', 'name_states'],
    [
        (
            'request',
            create_request_state_change_message('CANCELLED', 'APPROVED'),
            'CANCELLED', 'APPROVED',
            ['TEST NAME 1', 'TEST NAME 2', 'TEST NAME 3'],
            ['APPROVED', 'CONDITION', 'REJECTED']
        ),
        (
            'request',
            create_request_state_change_message('RESET', 'APPROVED'),
            'HOLD', 'APPROVED',
            ['TEST NAME 1', 'TEST NAME 2', 'TEST NAME 3'],
            ['APPROVED', 'CONDITION', 'REJECTED']
        ),
        (
            'request',
            create_request_state_change_message('RESET', 'APPROVED'),
            'INPROGRESS', 'APPROVED',
            ['TEST NAME 1', 'TEST NAME 2', 'TEST NAME 3'],
            ['APPROVED', 'CONDITION', 'REJECTED']
        ),
        (
            'request',
            create_request_state_change_message('CONSUMED', 'APPROVED'),
            'CONSUMED', 'APPROVED',
            ['TEST NAME 1', 'TEST NAME 2', 'TEST NAME 3'],
            ['APPROVED', 'CONDITION', 'REJECTED']
        ),

    ]
)
async def test_should_delete_names_from_solr(
        app,
        db,
        session,
        state_change_type,
        message_payload,
        new_nr_state,
        previous_nr_state,
        names: list,
        name_states: list):
    """Assert that names are deleted from Solr."""

    queue_util.send_name_request_state_msg = mock.Mock(return_value="True")
    queue_util.send_name_state_msg = mock.Mock(return_value="True")
    nr_num = message_payload['data'][state_change_type]['nrNum']
    mock_nr = create_nr(nr_num, new_nr_state, names, name_states)
    nr_ids_to_delete_from_solr = get_nr_ids_to_delete_from_solr(mock_nr)
    mock_msg = create_queue_mock_message(message_payload)
    mock_response = MockResponse({}, 200)

    # mock post method to solr feeder api
    with patch.object(requests, 'post', return_value=mock_response) as mock_solr_feeder_api_post:
        # mock process_possible_conflicts_delete to do nothing in order to isolate testing relevant to this test
        with patch.object(worker, 'process_possible_conflicts_delete', return_value=True):
            # mock find_by_nr to do nothing in order to isolate testing relevant to this test
            with patch.object(RequestDAO, 'find_by_nr', return_value=mock_nr):
                await worker.cb_subscription_handler(mock_msg)

                assert mock_solr_feeder_api_post.called == True
                assert 'api/v1/feeds' in mock_solr_feeder_api_post.call_args[0][0]

                post_json = mock_solr_feeder_api_post.call_args[1]['json']
                assert post_json['solr_core']
                assert post_json['solr_core'] == 'names'

                request_json = post_json['request']

                assert 'delete' in request_json
                assert len(nr_ids_to_delete_from_solr) > 0
                request_json = post_json['request']
                for nr_id in nr_ids_to_delete_from_solr:
                    assert nr_id in request_json
