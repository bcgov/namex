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
"""The Unit Tests and the helper routines."""
import json
from datetime import datetime

from random import randrange
from unittest.mock import Mock

from freezegun import freeze_time

from namex.models import Name, State, Request

from .. import add_years


class Obj:
    """Make a custom object hook used by dict_to_obj."""

    def __init__(self, dict1):
        """Create instance of obj."""
        self.__dict__.update(dict1)


def dict_to_obj(dict1):
    """Convert dict to an object."""
    return json.loads(json.dumps(dict1), object_hook=Obj)


class MockResponse:
    """Mock Response."""

    def __init__(self, json_data, status_code):
        """Mock Response __init__."""
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        """Mock Response json."""
        return self.json_data


def create_queue_mock_message(message_payload: dict):
    """Return a mock message that can be processed by the queue listener."""
    mock_msg = Mock()
    mock_msg.sequence = randrange(1000)
    mock_msg.data = dict_to_obj(message_payload)
    json_msg_payload = json.dumps(message_payload)
    mock_msg.data.decode = Mock(return_value=json_msg_payload)
    return mock_msg


def add_states_to_db(states):
    for code, desc in states:
        state = State(cd=code, description=desc)
        state.save_to_db()

def create_nr(nr_num: str, request_state: str, names: list, names_state: list):

    now = datetime.utcnow()

    with freeze_time(now):

        name_request = Request()
        name_request.nrNum = nr_num
        name_request.stateCd = request_state
        name_request._source = 'NRO'
        name_request.expirationDate = add_years(now, 1)
        # name_request.priorityCd = start_priority
        name_request.save_to_db()

        for index, name in enumerate(names):
            name_state = names_state[index]
            choice = index + 1

            name_obj = Name()
            name_obj.nrId = name_request.id
            name_obj.name = name
            name_obj.state = name_state
            name_obj.choice = choice
            name_obj.name_type_cd = 'CO'
            name_obj.save_to_db()

        return name_request


def create_request_state_change_message(new_state, prev_state):

    return {
        'specversion': '1.0.1',
        'type': 'bc.registry.names.events',
        'source': '/requests/NR 6724165',
        'id': '16fd2706-8baf-433b-82eb-8c7fada847aa',
        'time': '',
        'datacontenttype': 'application/json',
        'identifier': 'NR 6724165',
        'data': {
            'request': {
                'nrNum': 'NR 6724165',
                'newState': new_state,
                'previousState': prev_state
            }
        }
    }
