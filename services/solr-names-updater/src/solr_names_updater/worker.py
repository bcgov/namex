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
"""The unique worker functionality for this service is contained here.

The entry-point is the **cb_subscription_handler**

The design and flow leverage a few constraints that are placed upon it
by NATS Streaming and using AWAIT on the default loop.
- NATS streaming queues require one message to be processed at a time.
- AWAIT on the default loop effectively runs synchronously

If these constraints change, the use of Flask-SQLAlchemy would need to change.
Flask-SQLAlchemy currently allows the base model to be changed, or reworking
the model to a standalone SQLAlchemy usage with an async engine would need
to be pursued.
"""
import json
import os

import nats
from flask import Flask
from namex.models import db
from namex.models import Request as RequestDAO
from queue_common.service import QueueServiceManager
from queue_common.service_utils import QueueException, logger
from requests import RequestException
from sentry_sdk import capture_message
from sqlalchemy.exc import OperationalError
from urllib3.exceptions import NewConnectionError

from config import get_named_config  # pylint: disable=import-error
from solr_names_updater.names_processors.names import (  # noqa: I001
    process_add_to_solr as process_names_add,  # noqa: I001
    process_delete_from_solr as process_names_delete  # noqa: I001
)  # noqa: I001
from solr_names_updater.names_processors.possible_conflicts import (  # noqa: I001
    process_add_to_solr as process_possible_conflicts_add,  # noqa: I001
    process_delete_from_solr as process_possible_conflicts_delete  # noqa: I001, I005
)  # noqa: I001


qsm = QueueServiceManager()  # pylint: disable=invalid-name
APP_CONFIG = get_named_config(os.getenv('DEPLOYMENT_ENV', 'production'))
FLASK_APP = Flask(__name__)
FLASK_APP.config.from_object(APP_CONFIG)
db.init_app(FLASK_APP)


def is_names_event_msg_type(msg: dict):
    """Check message is of type nr state change."""
    if msg and msg.get('type', '') == 'bc.registry.names.events':
        return True

    return False


def is_processable(msg: dict):
    """Determine if message is processable using message type of msg."""
    nr_num = msg.get('nrNum', None)
    nr = RequestDAO.find_by_nr(nr_num)
    if msg and is_names_event_msg_type(msg) and nr.entity_type_cd not in ('FR', 'GP'):
        return True

    return False


async def process_names_event_message(msg: dict, flask_app: Flask):
    """Update solr accordingly based on incoming nr state changes."""
    if not flask_app or not msg:
        raise QueueException('Flask App or msg not available.')

    with flask_app.app_context():
        logger.debug('entering processing of nr event msg: %s', msg)
        request_state_change = msg.get('data').get('request', None)

        if request_state_change:
            new_state = request_state_change.get('newState')
            if new_state in ('APPROVED', 'CONDITIONAL'):
                process_names_add(request_state_change)
                process_possible_conflicts_add(request_state_change)
            elif new_state in ('CANCELLED', 'RESET', 'CONSUMED'):
                process_names_delete(request_state_change)
                process_possible_conflicts_delete(request_state_change)
            else:
                logger.debug('no names processing required for request state change message %s', msg)
        else:
            logger.debug('skipping - no matching state change message %s', msg)


async def cb_subscription_handler(msg: nats.aio.client.Msg):
    """Use Callback to process Queue Msg objects.

    This is the callback handler that gets called when a message is placed on the queue.
    If an exception is thrown and not handled, the message is not marked as consumed
    on the queue. It eventually times out and another worker can grab it.

    In some cases we want to consume the message and capture our failure on Sentry
    to be handled manually by staff.
    """
    try:
        logger.info('Received raw message seq:%s, data=  %s', msg.sequence, msg.data.decode())
        nr_state_change_msg = json.loads(msg.data.decode('utf-8'))
        logger.debug('Extracted nr event msg: %s', nr_state_change_msg)

        if is_processable(nr_state_change_msg):
            logger.debug('Begin process_nr_state_change for nr_event_msg: %s', nr_state_change_msg)
            await process_names_event_message(nr_state_change_msg, FLASK_APP)
            logger.debug('Completed process_nr_state_change for nr_event_msg: %s', nr_state_change_msg)
        else:
            # Skip processing of message as it isn't a message type this queue listener processes
            logger.debug('Skipping processing of nr event message as message type is not supported: %s',
                         nr_state_change_msg)
    except OperationalError as err:  # message goes back on the queue
        logger.error('Queue Blocked - Database Issue: %s', json.dumps(nr_state_change_msg), exc_info=True)
        raise err  # We don't want to handle the error, as a DB down would drain the queue
    except (RequestException, NewConnectionError) as err:  # message goes back on the queue
        logger.error('Queue Blocked - HTTP Connection Issue: %s', json.dumps(nr_state_change_msg), exc_info=True)
        raise err  # We don't want to handle the error, as a http connection error would drain the queue
    except (QueueException, KeyError, Exception):  # pylint: disable=broad-except # noqa B902
        # Catch Exception so that any error is still caught and the message is removed from the queue
        capture_message('Queue Error:' + json.dumps(nr_state_change_msg), level='error')
        logger.error('Queue Error: %s', json.dumps(nr_state_change_msg), exc_info=True)
