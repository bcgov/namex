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
"""Processing logic to process names updates via Solr feeder api."""
from __future__ import annotations

import json

from namex.constants import NameState
from namex.models import Request as RequestDAO
from queue_common.service_utils import logger

from solr_names_updater.names_processors import (convert_to_solr_conformant_datetime_str,
                                                 convert_to_solr_conformant_json,
                                                 find_name_by_name_states,
                                                 post_to_solr_feeder)


def process_add_to_solr(state_change_msg: dict):  # pylint: disable=too-many-locals, , too-many-branches
    """Process names update via Solr feeder api."""
    logger.debug('names processing: %s', state_change_msg)
    nr_num = state_change_msg.get('nrNum', None)
    nr = RequestDAO.find_by_nr(nr_num)
    send_to_solr_add(nr)


def process_delete_from_solr(state_change_msg: dict):  # pylint: disable=too-many-locals, , too-many-branches
    """Process names update via Solr feeder api."""
    logger.debug('names processing: %s', state_change_msg)
    nr_num = state_change_msg.get('nrNum', None)
    nr = RequestDAO.find_by_nr(nr_num)
    send_to_solr_delete(nr)


def send_to_solr_add(nr: RequestDAO):
    """Send json payload to add names from solr for NR."""
    # pylint: disable=no-member
    name_states = [NameState.APPROVED.value, NameState.REJECTED.value, NameState.CONDITION.value]
    names = find_name_by_name_states(nr.id, name_states)
    jur = nr.xproJurisdiction if nr.xproJurisdiction else 'BC'
    payload_dict = construct_payload_dict(nr, names, jur)
    resp = post_to_solr_feeder(payload_dict)
    if resp.status_code != 200:
        logger.error('failed to add names to solr for %s, status code: %i, error reason: %s, error details: %s',
                     nr.nrNum,
                     resp.status_code,
                     resp.reason,
                     resp.text)


def send_to_solr_delete(nr: RequestDAO):
    """Send json payload to delete names from solr for NR."""
    delete_ids = get_nr_ids_to_delete_from_solr(nr)
    payload_dict = {
        'solr_core': 'names',
        'request': {
            'delete': delete_ids,
            'commit': {}
        }
    }
    request_str = json.dumps(payload_dict['request'])
    payload_dict['request'] = request_str
    resp = post_to_solr_feeder(payload_dict)
    if resp.status_code != 200:
        logger.error('failed to delete names from solr for %s, status code: %i, error reason: %s, error details: %s',
                     nr.nrNum,
                     resp.status_code,
                     resp.reason,
                     resp.text)


def get_nr_ids_to_delete_from_solr(nr: RequestDAO):
    """Generate NR ids to be used to delete names from solr for a NR."""
    nr_num_1 = f'{nr.nrNum}-1'
    nr_num_2 = f'{nr.nrNum}-2'
    nr_num_3 = f'{nr.nrNum}-3'
    keys = [nr_num_1, nr_num_2, nr_num_3]
    return keys


def construct_payload_dict(nr: RequestDAO, names, jur):
    """Construct json payload used to invoke solr feeder endpoint for adding names for a given NR."""
    payload_dict = {'solr_core': 'names'}
    payload_request = {}

    for index, name in enumerate(names):
        key = f'add{index + 1}'
        doc_id = f'{nr.nrNum}-{name.choice}'
        start_date = convert_to_solr_conformant_datetime_str(nr.submittedDate)
        payload_request[key] = {
            'doc': {
                'id': doc_id,
                'name': name.name,
                'nr_num': nr.nrNum,
                'submit_count': nr.submitCount,
                'name_state_type_cd': name.state,
                'start_date': start_date,
                'jurisdiction': jur
            }
        }

    payload_request['commit'] = {}
    request_str = json.dumps(payload_request)
    request_str = convert_to_solr_conformant_json(request_str)
    payload_dict['request'] = request_str
    return payload_dict
