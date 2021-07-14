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

import asyncio
from datetime import datetime, timedelta, timezone
import json
import time
import uuid
import nats
from typing import Optional
from sentry_sdk import capture_message

from queue_common.messages import create_cloud_event_msg
from queue_common.service import QueueServiceManager
from queue_common.service_utils import QueueException, logger
from config import Config


class CloudEventMessageService(object):
    """Provides services to cloud event message services
    """
    @staticmethod
    async def sendNameRequestStateEvent(nrNum, stateCd, payment_token=None):
        event_loop = asyncio.get_event_loop()
        qsm = QueueServiceManager()  # pylint: disable=invalid-name
        await qsm.run(loop=event_loop,
                        config=Config,
                        callback=cb_subscription_handler)
        cloud_event_msg = create_cloud_event_msg(msg_id=str(uuid.uuid4()),
                                                msg_type='bc.registry.names.request',
                                                source=f'/requests/{nrNum}',
                                                time=datetime.
                                                utcfromtimestamp(time.time()).
                                                replace(tzinfo=timezone.utc).
                                                isoformat(),
                                                identifier=nrNum,
                                                json_data_body={
                                                    'request': {
                                                        'header': {'nrNum': nrNum},
                                                        'statusCode': stateCd,
                                                        **({'paymentToken': payment_token} if payment_token is not None else {})
                                                    }}
                                                )
        await CloudEventMessageService.publish_name_state_message(qsm, cloud_event_msg)
        await qsm.close()


    @staticmethod
    async def publish_name_state_message(qsm: QueueServiceManager,  # pylint: disable=redefined-outer-name
                                   cloud_event_msg: dict):
        """Publish the name state message onto the NATS emailer subject."""
        logger.debug('publish to queue, subject:%s, event:%s', Config.NATS_SUBJECT, cloud_event_msg)
        await qsm.service.publish(subject=Config.NATS_SUBJECT,
                                  msg=cloud_event_msg)


def extract_message(msg: nats.aio.client.Msg) -> Optional[dict]:
    """Return a dict of the json string in the Msg.data."""
    try:
        return json.loads(msg.data.decode('utf-8'))
    except (TypeError, json.decoder.JSONDecodeError):
        return None


async def cb_subscription_handler(msg: nats.aio.client.Msg):
    """Use Callback to process Queue Msg objects.

    This is the callback handler that gets called when a message is placed on the queue.
    If an exception is thrown and not handled, the message is not marked as consumed
    on the queue. It eventually times out and another worker can grab it.

    In some cases we want to consume the message and capture our failure on Sentry
    to be handled manually by staff.

    This call MUST BE IDEMPOTENT and unroll any partial changes in failures.
    """
    try:
        logger.info('Received raw message seq:%s, data=  %s', msg.sequence, msg.data.decode())
        if not (rec_msg := extract_message(msg)):
            capture_message('Queue Error: no message on queue', level='error')
            logger.debug('Queue Error: no message on queue')
        else:
            logger.debug('Message received: %s', rec_msg)

    except (QueueException, KeyError, Exception):  # pylint: disable=broad-except # noqa B902
        # Catch Exception so that any error is still caught and the message is removed from the queue
        capture_message('Queue Error:' + json.dumps(rec_msg), level='error')
        logger.error('Queue Error: %s', json.dumps(rec_msg), exc_info=True)
