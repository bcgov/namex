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
    """Process names update via Solr feeder api."""
    # structured_log(state_change_msg)
    nr_num = state_change_msg.get('nrNum', None)
    nr = RequestDAO.find_by_nr(nr_num)
    send_to_solr_add(nr)


def process_delete_from_solr(state_change_msg: dict):  # pylint: disable=too-many-locals, , too-many-branches
    """Update the NR state in Solr.

    The new Solr does not delete documents. Cancel, expire, consume, and reset
    send the NR's current state so search filters the record out.
    """
    nr_num = state_change_msg.get('nrNum', None)
    nr = RequestDAO.find_by_nr(nr_num)
    send_to_solr_state_update(nr)


def _name_state_code(name_state: str) -> str:
    if name_state == NameState.CONDITION.value:  # pylint: disable=no-member
        return 'C'
    return 'A'


def send_to_solr_add(nr: RequestDAO):
    """Send json payload to add names to solr for NR."""
    # pylint: disable=no-member
    name_states = [NameState.APPROVED.value, NameState.CONDITION.value]
    names = find_name_by_name_states(nr.id, name_states)
    if not names:
        logger.info(f'no approved/condition name found for {nr.nrNum}, skipping solr add')
        return
    jur = nr.xproJurisdiction if nr.xproJurisdiction else 'BC'
    payload_dict = construct_payload_dict(nr, names, jur)
    resp = post_to_solr_feeder(payload_dict)
    if resp.status_code != 200:
        logger.error(f'failed to add names to solr for {nr.nrNum}, status code: {resp.status_code}, error reason: {resp.reason}, error details: {resp.text}')


def send_to_solr_state_update(nr: RequestDAO):
    """Send the NR's current state so the existing Solr document is updated, not deleted."""
    name_states = [NameState.APPROVED.value, NameState.CONDITION.value]  # pylint: disable=no-member
    names = find_name_by_name_states(nr.id, name_states)
    if not names:
        logger.info(f'no approved/condition name found for {nr.nrNum}, skipping solr state update')
        return
    jur = nr.xproJurisdiction if nr.xproJurisdiction else 'BC'
    payload_dict = construct_payload_dict(nr, names, jur, nr.stateCd)
    resp = post_to_solr_feeder(payload_dict)
    if resp.status_code != 200:
        logger.error(f'failed to update name state in solr for {nr.nrNum}, status code: {resp.status_code}, error reason: {resp.reason}, error details: {resp.text}')


def construct_payload_dict(nr: RequestDAO, names, jur, state_type_cd=None):
    """Construct json payload used to invoke solr feeder endpoint for a given NR.

    One add document carries every approved or conditional name. state_type_cd
    overrides the name state when the NR itself is cancelled, expired, consumed, or reset.
    """
    payload_dict = {'solr_core': 'names'}
    start_date = convert_to_solr_conformant_datetime_str(nr.submittedDate)
    payload_request = {
        'add': {
            'doc': {
                'id': nr.nrNum,
                'sub_type': nr.requestTypeCd,
                'source': nr.source or 'NAMEREQUEST',
                'state_type_cd': state_type_cd if state_type_cd else names[0].state,
                'start_date': start_date,
                'jurisdiction': jur,
                'names': [
                    {
                        'choice': name.choice,
                        'name': name.name,
                        'name_state': _name_state_code(name.state),
                        'submit_count': nr.submitCount
                    }
                    for name in names
                ]
            }
        },
        'commit': {}
    }
    payload_dict['request'] = json.dumps(payload_request)
    return payload_dict
