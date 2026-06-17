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
from structured_logging import StructuredLogging

from solr_names_updater.names_processors import (
    convert_to_solr_conformant_datetime_str,  # noqa: I001
    find_name_by_name_states,  # noqa: I001
    post_to_solr_feeder,  # noqa: I001; noqa: I001
)

# noqa: I003, I005

logger = StructuredLogging.get_logger()

def process_add_to_solr(state_change_msg: dict):  # pylint: disable=too-many-locals, , too-many-branches
    """Process possible conflicts update via Solr feeder api."""
    logger.info(f'Processing add to solr for state_change_msg: {state_change_msg}')
    nr_num = state_change_msg.get('nrNum')
    nr = RequestDAO.find_by_nr(nr_num)
    send_to_solr_add(nr)


def process_delete_from_solr(state_change_msg: dict):  # pylint: disable=too-many-locals, , too-many-branches
    """Process possible conflicts state update via Solr feeder api.

    The new Solr does not support deleting documents. Instead of removing the record,
    the NR state is updated so the conflict search excludes it (only ACTIVE/APPROVED/
    CONDITION are returned as conflicts).
    """
    logger.info(f'Processing state update from solr for state_change_msg: {state_change_msg}') # noqa: S608
    nr_num = state_change_msg.get('nrNum')
    nr = RequestDAO.find_by_nr(nr_num)
    send_to_solr_state_update(nr)


def send_to_solr_add(nr: RequestDAO):
    """Send json payload to add possible conflict to solr for NR."""
    name_states = [NameState.APPROVED.value, NameState.CONDITION.value]  # pylint: disable=no-member
    names = find_name_by_name_states(nr.id, name_states)
    name = names[0]
    jur = nr.xproJurisdiction if nr.xproJurisdiction else 'BC'
    payload_dict = construct_payload_dict(nr, name, jur)

    resp = post_to_solr_feeder(payload_dict)
    if resp.status_code != 200:
        logger.error(f'failed to add possible conflict to solr for {nr.nrNum}, status code: {resp.status_code}, error reason: {resp.reason}, error details: {resp.text}')


def send_to_solr_state_update(nr: RequestDAO):
    """Send json payload to update the possible conflict NR state in solr.

    The new Solr does not support deleting documents, so a delete is converted to a
    state update. The NR's current state (e.g. CANCELLED, EXPIRED, CONSUMED, RESET) is
    sent so the conflict search filters the record out based on its state.
    """
    name_states = [NameState.APPROVED.value, NameState.CONDITION.value]  # pylint: disable=no-member
    names = find_name_by_name_states(nr.id, name_states)
    if not names:
        logger.info(f'no approved/condition name found for {nr.nrNum}, skipping solr state update')
        return

    name = names[0]
    jur = nr.xproJurisdiction if nr.xproJurisdiction else 'BC'
    payload_dict = construct_payload_dict(nr, name, jur, nr.stateCd)

    resp = post_to_solr_feeder(payload_dict)
    if resp.status_code != 200:
        logger.error(f'failed to update possible conflict state in solr for {nr.nrNum}, status code: {resp.status_code}, error reason: {resp.reason}, error details: {resp.text}')


def construct_payload_dict(nr: RequestDAO, name, jur, state_type_cd=None):
    """Construct json payload used to invoke solr feeder endpoint for a given NR.

    When state_type_cd is provided it overrides the name state. This is used to update
    the NR state for records that were previously deleted in the old Solr (e.g. on
    cancel/expire/consume/reset); otherwise the name state is used (add/approve flow).
    """
    payload_dict = {'solr_core': 'possible.conflicts'}
    payload_request = {}
    start_date = convert_to_solr_conformant_datetime_str(nr.submittedDate)
    payload_request['add'] = {
        'doc': {
            'id': nr.nrNum,
            'sub_type': nr.requestTypeCd,
            'name': name.name,
            'state_type_cd': state_type_cd if state_type_cd else name.state,
            'source': nr.source,
            'start_date': start_date,
            'jurisdiction': jur
        }
    }

    payload_request['commit'] = {}
    request_str = json.dumps(payload_request)
    payload_dict['request'] = request_str
    return payload_dict
