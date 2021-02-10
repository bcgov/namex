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
import time
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

import nats
from flask import Flask
from namex.models import db, Payment, Request as RequestDAO  # noqa:I001; import orders
from queue_common.messages import create_cloud_event_msg  # noqa:I005
from queue_common.service import QueueServiceManager
from queue_common.service_utils import QueueException, logger
from sentry_sdk import capture_message
from sqlalchemy.exc import OperationalError

from namex_pay import config


class PaymentState(Enum):
    """Render all the payment states we know what to do with."""

    COMPLETED = 'COMPLETED'
    TRANSACTION_FAILED = 'TRANSACTION_FAILED'


def extract_message(msg: nats.aio.client.Msg) -> Optional[dict]:
    """Return a dict of the json string in the Msg.data."""
    try:
        return json.loads(msg.data.decode('utf-8'))
    except (TypeError, json.decoder.JSONDecodeError):
        return None


async def publish_email_message(qsm: QueueServiceManager,  # pylint: disable=redefined-outer-name
                                cloud_event_msg: dict):
    """Publish the email message onto the NATS emailer subject."""
    print(f"publish to queue, subject:{APP_CONFIG.EMAIL_PUBLISH_OPTIONS['subject']}")
    await qsm.service.publish(subject=APP_CONFIG.EMAIL_PUBLISH_OPTIONS['subject'],
                              msg=cloud_event_msg)


async def furnish_receipt_message(qsm: QueueServiceManager, payment: Payment):  # pylint: disable=redefined-outer-name
    """Send receipt info to the mail queue if it hasn't yet been done."""
    if payment.furnished == 'Y':
        capture_message(f'Queue Issue: Duplicate, already furnished receipt for payment.id={payment.id}')
        return

    nr = None

    try:
        payment.furnished = True
        payment.save_to_db()
    except Exception as err:  # noqa: B902; bare exception to catch all
        raise Exception('Unable to alter payment record.') from err

    try:
        nr = RequestDAO.find_by_id(payment.nrId)
        cloud_event_msg = create_cloud_event_msg(msg_id=str(uuid.uuid4()),
                                                 msg_type='bc.registry.names.request',
                                                 source=f'/requests/{nr.nrNum}',
                                                 time=datetime.
                                                 utcfromtimestamp(time.time()).
                                                 replace(tzinfo=timezone.utc).
                                                 isoformat(),
                                                 identifier=nr.nrNum,
                                                 json_data_body={
                                                     'request': {
                                                         'header': {'nrNum': nr.nrNum},
                                                         'paymentToken': payment.payment_token,
                                                         'statusCode': nr.stateCd
                                                     }}
                                                 )
        await publish_email_message(qsm, cloud_event_msg)
    except Exception as err:  # noqa: B902; bare exception to catch all
        payment.furnished = False
        payment.save_to_db()
        raise QueueException(f'Unable to furnish NR info. {err}') from err


async def process_payment(pay_msg: dict, flask_app: Flask):
    """Render the payment status."""
    if not flask_app or not pay_msg:
        raise QueueException('Flask App or token not available.')

    with flask_app.app_context():

        # capture_message(f'Queue Issue: Unable to find payment.id={payment_id} to place on email queue')
        # return

        if pay_msg.get('paymentToken', {}).get('statusCode') == PaymentState.TRANSACTION_FAILED.value:
            # TODO: The customer has cancelled out of paying, so we could note this better
            # technically the payment for this service is still pending
            return

        if pay_msg.get('paymentToken', {}).get('statusCode') == PaymentState.COMPLETED.value:

            if payment_token := pay_msg.get('paymentToken', {}).get('id'):
                if payment := Payment.find_by_payment_token(payment_token):

                    await furnish_receipt_message(qsm, payment)
                else:
                    capture_message(f'Queue Error: Unable to find payment record for :{pay_msg}', level='error')
            else:
                capture_message(f'Queue Error: Missing id :{pay_msg}', level='error')

            return

        # if we're here and haven't been able to action it,
        # then we've received an unknown token
        # Capture it to the log and remove it rom the queue
        logger.error('Unknown payment token given: %s', payment_token)
        capture_message(
            f'Queue Error: Unknown paymentToken:{payment_token}',
            level='error')


qsm = QueueServiceManager()  # pylint: disable=invalid-name
APP_CONFIG = config.get_named_config(os.getenv('DEPLOYMENT_ENV', 'production'))
FLASK_APP = Flask(__name__)
FLASK_APP.config.from_object(APP_CONFIG)
db.init_app(FLASK_APP)


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
        if not (pay_msg := extract_message(msg)):
            capture_message('Queue Error: no message on queue', level='error')
            logger.debug('Queue Error: no message on queue')
        else:

            logger.debug('Extracted pay_msg: %s', pay_msg)
            await process_payment(pay_msg, FLASK_APP)

    except OperationalError as err:  # message goes back on the queue
        logger.error('Queue Blocked - Database Issue: %s', json.dumps(pay_msg), exc_info=True)
        raise err  # We don't want to handle the error, as a DB down would drain the queue
    except (QueueException, KeyError, Exception):  # pylint: disable=broad-except # noqa B902
        # Catch Exception so that any error is still caught and the message is removed from the queue
        capture_message('Queue Error:' + json.dumps(pay_msg), level='error')
        logger.error('Queue Error: %s', json.dumps(pay_msg), exc_info=True)
