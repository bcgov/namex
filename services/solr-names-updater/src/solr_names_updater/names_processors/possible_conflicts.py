# Copyright © 2021 Province of British Columbia
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
"""Processing logic to process possible conflict updates via Solr feeder api."""
from __future__ import annotations

import json

from namex.constants import NameState
from namex.models import Request as RequestDAO
from queue_common.service_utils import logger

from solr_names_updater.names_processors import (  # noqa: I001
    convert_to_solr_conformant_datetime_str,  # noqa: I001
    find_name_by_name_states,  # noqa: I001
    post_to_solr_feeder  # noqa: I001
)  # noqa: I001
# noqa: I003, I005


def process_add_to_solr(state_change_msg: dict):  # pylint: disable=too-many-locals, , too-many-branches
    """Process possible conflicts update via Solr feeder api."""
    logger.debug('names processing: %s', state_change_msg)
    nr_num = state_change_msg.get('nrNum')
    nr = RequestDAO.find_by_nr(nr_num)
    send_to_solr_add(nr)


def process_delete_from_solr(state_change_msg: dict):  # pylint: disable=too-many-locals, , too-many-branches
    """Process possible conflicts update via Solr feeder api."""
    logger.debug('names processing: %s', state_change_msg)
    nr_num = state_change_msg.get('nrNum')
    nr = RequestDAO.find_by_nr(nr_num)
    send_to_solr_delete(nr)


def send_to_solr_add(nr: RequestDAO):
    """Send json payload to add possible conflict to solr for NR."""
    name_states = [NameState.APPROVED.value, NameState.CONDITION.value]  # pylint: disable=no-member
    names = find_name_by_name_states(nr.id, name_states)
    name = names[0]
    jur = nr.xproJurisdiction if nr.xproJurisdiction else 'BC'
    payload_dict = construct_payload_dict(nr, name, jur)

    resp = post_to_solr_feeder(payload_dict)
    if resp.status_code != 200:
        logger.error("""failed to add possible conflict to solr for %s,
                    status code: %i, error reason: %s, error details: %s""",
                     nr.nrNum,
                     resp.status_code,
                     resp.reason,
                     resp.text)


def send_to_solr_delete(nr: RequestDAO):
    """Send json payload to delete possible conflict from solr for NR."""
    payload_dict = {
        'solr_core': 'possible.conflicts',
        'request': {
            'delete': [nr.nrNum],
            'commit': {}
        }
    }

    request_str = json.dumps(payload_dict['request'])
    payload_dict['request'] = request_str
    resp = post_to_solr_feeder(payload_dict)
    if resp.status_code != 200:
        logger.error("""failed to delete possible conflict from solr for %s,
                     status code: %i, error reason: %s, error details: %s""",
                     nr.nrNum,
                     resp.status_code,
                     resp.reason,
                     resp.text)


def construct_payload_dict(nr: RequestDAO, name, jur):
    """Construct json payload used to invoke solr feeder endpoint for adding possible conflicts for a given NR."""
    payload_dict = {'solr_core': 'possible.conflicts'}
    payload_request = {}
    start_date = convert_to_solr_conformant_datetime_str(nr.submittedDate)
    payload_request['add'] = {
        'doc': {
            'id': nr.nrNum,
            'name': name.name,
            'state_type_cd': name.state,
            'source': nr.source,
            'start_date': start_date,
            'jurisdiction': jur
        }
    }

    payload_request['commit'] = {}
    request_str = json.dumps(payload_request)
    payload_dict['request'] = request_str
    return payload_dict
