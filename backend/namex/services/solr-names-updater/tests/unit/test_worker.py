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
# from contextlib import suppress
import base64
import json
from unittest import mock
from unittest.mock import patch

import pytest
from namex.utils import queue_util

from solr_names_updater.resources import worker  # noqa: I001

from . import create_nr, helper_create_cloud_event  # noqa: I003


@pytest.mark.parametrize(
    ['testname','message_payload','nr_entity','assert_value'],[
     ('Sole Prop Approved', helper_create_cloud_event('APPROVED', 'DRAFT'), 'FR', False),
     ('Sole Prop Conditional', helper_create_cloud_event('CONDITIONAL', 'DRAFT'),'FR', False),
     ('Sole Prop Cancelled', helper_create_cloud_event('CANCELLED', 'DRAFT'), 'FR', False),
     ('Sole Prop Consumed', helper_create_cloud_event('CONSUMED', 'DRAFT'), 'FR', False),
     ('Gen Part Approved', helper_create_cloud_event('APPROVED', 'DRAFT'),   'GP', False),
     ('Gen Part Conditional', helper_create_cloud_event('CONDITIONAL', 'DRAFT'), 'GP', False),
     ('Gen Part Cancelled', helper_create_cloud_event('CANCELLED', 'DRAFT'), 'GP', False),
     ('Gen Part Consumed', helper_create_cloud_event('CONSUMED', 'DRAFT'), 'GP', False),
     ('CORPORATION Approved', helper_create_cloud_event('APPROVED', 'DRAFT'), 'CR', True),
     ('CORPORATION Conditional', helper_create_cloud_event('CONDITIONAL', 'DRAFT'), 'CR', True),
     ('CORPORATION Cancelled', helper_create_cloud_event('CANCELLED', 'DRAFT'), 'CR', True),
     ('CORPORATION Consumed', helper_create_cloud_event('CONSUMED', 'DRAFT'), 'CR', True)
    ])
def test_sp_gp_names_not_processed_to_solr(
        testname,
        client,
        message_payload,
        nr_entity,
        assert_value):
    """Assert that names are added to solr."""
    queue_util.send_name_request_state_msg = mock.Mock(return_value='True')

    data_json = json.loads(base64.b64decode(message_payload['message']['data']).decode('utf-8'))
    nr_num = data_json['data']['request']['nrNum']

    nr_new_state = data_json['data']['request']['newState']
    create_nr(nr_num, nr_new_state, ['TEST NAME 1'], ['APPROVED'], nr_entity)

    with patch.object(worker, 'process_names_event_message', return_value=True) as mock_process_names_evt_func:
        rv = client.post('/', json=message_payload)
        assert mock_process_names_evt_func.called == assert_value
