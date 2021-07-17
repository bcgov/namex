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
    """Provides services to cloud event message services"""
    
    @staticmethod
    async def sendNameRequestStateEvent(nr_num, old_nr_num, state_cd, old_state_cd):
        event_loop = asyncio.get_event_loop()
        qsm = QueueServiceManager()  # pylint: disable=invalid-name
        await qsm.run(loop=event_loop,
                      config=Config,
                      callback=cb_subscription_handler)
        cloud_event_msg = create_cloud_event_msg(msg_id=str(uuid.uuid4()),
                                                msg_type='bc.registry.names.request',
                                                source=f'/requests/{nr_num}',
                                                time=datetime.
                                                utcfromtimestamp(time.time()).
                                                replace(tzinfo=timezone.utc).
                                                isoformat(),
                                                identifier=nr_num,
                                                json_data_body={
                                                    'request': {
                                                        'nrNum': nr_num,
                                                        'oldNrNum': old_nr_num,
                                                        'newState': state_cd,
                                                        'previousState': old_state_cd
                                                    }}
                                                )
        await CloudEventMessageService.publish_name_state_message(qsm, cloud_event_msg)
        await qsm.close()


    @staticmethod
    async def publish_name_state_message(qsm: QueueServiceManager,  # pylint: disable=redefined-outer-name
                                         cloud_event_msg: dict):
        """Publish the name state message onto the NATS subject."""
        logger.debug('publish to queue, subject:%s, event:%s', Config.NATS_SUBJECT, cloud_event_msg)
        await qsm.service.publish(subject=Config.NATS_SUBJECT,
                                  msg=cloud_event_msg)

async def cb_subscription_handler(msg: nats.aio.client.Msg):
    """Just a dummy func to satisfy QueueServiceManager as legal-api does not subscribe to any subject at the moment."""
