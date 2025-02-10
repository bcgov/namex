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
"""The unique worker functionality for this service is contained here.
"""

import json
from http import HTTPStatus

from flask import Blueprint, Flask, current_app, request
from gcp_queue.gcp_auth import ensure_authorized_queue_user
from gcp_queue.logging import structured_log
from namex.models import Request as RequestDAO
from namex.services import queue
from requests import RequestException
from sbc_common_components.utils.enums import QueueMessageTypes
from sentry_sdk import capture_message
from sqlalchemy.exc import OperationalError
from urllib3.exceptions import NewConnectionError

from solr_names_updater.names_processors.names import process_add_to_solr as process_names_add  # noqa: I001
from solr_names_updater.names_processors.names import process_delete_from_solr as process_names_delete  # noqa: I001
from solr_names_updater.names_processors.possible_conflicts import (  # noqa: I001
    process_add_to_solr as process_possible_conflicts_add,
)
from solr_names_updater.names_processors.possible_conflicts import (  # noqa: I001, I005
    process_delete_from_solr as process_possible_conflicts_delete,
)

bp = Blueprint("worker", __name__)



@bp.route("/", methods=("POST",))
@ensure_authorized_queue_user
def worker():
    """
    Process the incoming cloud event.
    """
    structured_log(request, "INFO", f"Incoming raw msg: {request.data}")
    ret = {}, HTTPStatus.OK
    if not (ce := queue.get_simple_cloud_event(request)):
        return ret

    structured_log(request, "INFO", f"received ce: {str(ce)}")

    with current_app.app_context():
        try:
            structured_log(f'Extracted nr event msg: {ce}')

            if is_processable(ce):
                structured_log(request, message=f'Begin process_nr_state_change for nr_event_msg: {ce}')
                process_names_event_message(ce, current_app)
                structured_log(request, message=f'Completed process_nr_state_change for nr_event_msg: {ce}')
            elif is_processable_firm(ce):
                structured_log(request, message=f'Begin process_nr_state_change for firm, nr_event_msg: {ce}')
                process_names_event_message_firm(ce, current_app)
                structured_log(request, message=f'Completed process_nr_state_change for firm, nr_event_msg: {ce}')
            else:
                # Skip processing of message as it isn't a message type this queue listener processes
                structured_log(request, message=f'Skipping processing of nr event message as message type is not supported: {ce}')

        except OperationalError as err:  # message goes back on the queue
            structured_log(request, message=f'Queue Blocked - Database Issue: {json.dumps(ce)}', severity='ERROR')
            ret = {}, HTTPStatus.INTERNAL_SERVER_ERROR
            raise err  # We don't want to handle the error, as a DB down would drain the queue
        except (RequestException, NewConnectionError) as err:  # message goes back on the queue
            structured_log(request, message=f'Queue Blocked - HTTP Connection Issue: {json.dumps(ce)}', severity='ERROR')
            ret = {}, HTTPStatus.INTERNAL_SERVER_ERROR
            raise err  # We don't want to handle the error, as a http connection error would drain the queue
        except Exception as e:  # pylint: disable=broad-except # noqa B902
            # Catch Exception so that any error is still caught and the message is removed from the queue
            capture_message('Queue Error:' + e, level='error')
            structured_log(request, message=f'Queue Error: {json.dumps(ce)}', severity='ERROR')
        finally:
            return ret


def is_names_event_msg_type(msg: dict):
    """Check message is of type nr state change."""

    if msg and msg.type == QueueMessageTypes.NAMES_EVENT.value:
            return True

    return False


def is_processable(msg: dict):
    """Determine if message is processable using message type of msg."""
    if msg and is_names_event_msg_type(msg) \
        and (nr_num := msg.data
                            .get('request', {})
                            .get('nrNum', None)) \
        and (nr := RequestDAO.find_by_nr(nr_num)) \
        and nr.entity_type_cd not in ('FR', 'GP'):
        return True

    return False

def is_processable_firm(msg: dict):
    """Determine if message is processible and a firm."""
    if msg and is_names_event_msg_type(msg) \
        and (nr_num := msg.data
                            .get('request', {})
                            .get('nrNum', None)) \
        and (nr := RequestDAO.find_by_nr(nr_num)) \
        and nr.entity_type_cd in ('FR', 'GP'):
        return True

    return False


def process_names_event_message(msg: dict, flask_app: Flask):
    """Update solr accordingly based on incoming nr state changes."""
    if not flask_app or not msg:
        raise Exception('Flask App or msg not available.')

    structured_log( f'entering processing of nr event msg: {msg}')

    request_state_change = msg.data.get('request', None)

    if request_state_change:
        new_state = request_state_change.get('newState')
        if new_state in ('APPROVED', 'CONDITIONAL'):
            process_names_add(request_state_change)
            process_possible_conflicts_add(request_state_change)
        elif new_state in ('CANCELLED', 'RESET', 'CONSUMED', 'EXPIRED'):
            process_names_delete(request_state_change)
            process_possible_conflicts_delete(request_state_change)
        else:
            structured_log(f'no names processing required for request state change message: {msg}')

    else:
        structured_log(f'skipping - no matching state change message: {msg}')


def process_names_event_message_firm(msg: dict, flask_app: Flask):
    """Update solr for the firm accordingly based on incoming nr state changes."""
    if not flask_app or not msg:
        raise Exception('Flask App or msg not available.')

    structured_log( f'entering processing of nr event msg for firm: {msg}')

    request_state_change = msg.data.get('request', None)

    if request_state_change:
        new_state = request_state_change.get('newState')
        if new_state in ('APPROVED', 'CONDITIONAL'):
            process_names_add(request_state_change)
        elif new_state in ('CANCELLED', 'RESET', 'CONSUMED', 'EXPIRED'):
            process_names_delete(request_state_change)
        else:
            structured_log(f'no names processing required for request state change message: {msg}')

    else:
        structured_log(f'skipping - no matching state change message: {msg}')

