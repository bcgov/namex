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
"""The Test Suites to ensure that the worker is operating correctly."""
import json
from datetime import timedelta
from unittest import mock
from unittest.mock import patch

import pytest
from freezegun import freeze_time

from namex.models import Request as RequestDAO
from namex.utils import queue_util
from queue_common.service_utils import QueueException
from solr_names_updater import worker # noqa: I001
from . import create_queue_mock_message, create_nr, MockResponse, create_request_state_change_message # noqa: I003

@pytest.mark.parametrize(
    ['testname','message_payload','nr_entity','assert_value'],[
     ('Sole Prop Approved', create_request_state_change_message('APPROVED', 'DRAFT'), 'FR', False),
     ('Sole Prop Conditional', create_request_state_change_message('CONDITIONAL', 'DRAFT'),'FR', False),
     ('Sole Prop Cancelled', create_request_state_change_message('CANCELLED', 'DRAFT'), 'FR', False),
     ('Sole Prop Reset', create_request_state_change_message('RESET', 'DRAFT'), 'FR', False),
     ('Sole Prop Consumed', create_request_state_change_message('CONSUMED', 'DRAFT'), 'FR', False),
     ('Sole Prop Expired', create_request_state_change_message('EXPIRED', 'DRAFT'), 'FR', False),
     ('Gen Part Approved', create_request_state_change_message('APPROVED', 'DRAFT'),   'GP', False),
     ('Gen Part Conditional', create_request_state_change_message('CONDITIONAL', 'DRAFT'), 'GP', False),
     ('Gen Part Cancelled', create_request_state_change_message('CANCELLED', 'DRAFT'), 'GP', False),
     ('Gen Part Reset', create_request_state_change_message('RESET', 'DRAFT'), 'GP', False),
     ('Gen Part Consumed', create_request_state_change_message('CONSUMED', 'DRAFT'), 'GP', False),
     ('Gen Part Expired', create_request_state_change_message('EXPIRED', 'DRAFT'), 'GP', False),
     ('CORPORATION Approved', create_request_state_change_message('APPROVED', 'DRAFT'), 'CR', True),
     ('CORPORATION Conditional', create_request_state_change_message('CONDITIONAL', 'DRAFT'), 'CR', True),
     ('CORPORATION Cancelled', create_request_state_change_message('CANCELLED', 'DRAFT'), 'CR', True),
     ('CORPORATION Reset', create_request_state_change_message('RESET', 'DRAFT'), 'CR', True),
     ('CORPORATION Consumed', create_request_state_change_message('CONSUMED', 'DRAFT'), 'CR', True),
     ('CORPORATION Expired', create_request_state_change_message('EXPIRED', 'DRAFT'), 'CR', True)
    ])
async def test_sp_gp_names_not_processed_to_solr(
        testname,
        message_payload,
        nr_entity,
        assert_value):
    """Assert that names are added to solr."""

    queue_util.process_names_event_message = mock.Mock(return_value="True")
    mock_msg = create_queue_mock_message(message_payload)
    mock_nr = mock.Mock()
    mock_nr.entity_type_cd = nr_entity

    # mock process_names_event_message to do nothing in order to isolate testing relevant to this test
    with patch.object(worker, 'process_names_event_message', return_value=True) as mock_process_names_evt_func:
        # mock find_by_nr to do nothing in order to isolate testing relevant to this test
        with patch.object(RequestDAO, 'find_by_nr', return_value=mock_nr):
            await worker.cb_subscription_handler(mock_msg)

            assert mock_process_names_evt_func.called == assert_value