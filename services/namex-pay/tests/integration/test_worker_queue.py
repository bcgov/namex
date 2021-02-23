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
"""Test Suite to ensure the worker routines are working as expected."""
import asyncio
import datetime
import json
import random
from flask.signals import Namespace

import pytest
from queue_common.service_utils import subscribe_to_queue

from .utils import helper_add_payment_to_queue


# Sanity check, this just exercises the queue config to send/receive
# messages on a subject
# if this can't run, the other functional integration tests will fail.
@pytest.mark.asyncio
async def test_queue_config_sanity(app, session, stan_server, event_loop, client_id, entity_stan, future):
    """Assert that payment tokens can be retrieved and decoded from the Queue."""
    import uuid
    import dpath.util
    from namex_pay.worker import APP_CONFIG
    # Call back for the subscription
    msgs = []

    async def cb_handler(msg):
        nonlocal msgs
        nonlocal future
        msgs.append(msg)
        if len(msgs) == 10:
            future.set_result(True)

    file_handler_subject = str(uuid.uuid4())

    await subscribe_to_queue(entity_stan,
                             file_handler_subject,
                             f'entity_queue.{file_handler_subject}',
                             f'entity_durable_name.{file_handler_subject}',
                             cb_handler)

    # add payment tokens to queue
    for i in range(0, 5):
        payload = {'paymentToken': {'id': 1234 + i, 'statusCode': 'COMPLETED'}}
        await entity_stan.publish(subject=file_handler_subject,
                                  payload=json.dumps(payload).encode('utf-8'))
    try:
        await asyncio.wait_for(future, 2, loop=event_loop)
    except Exception as err:  # noqa B902; just in tests
        print(err)

    # check the payment tokens were retrieved from the queue
    assert len(msgs) == 5
    for i in range(0, 5):
        m = msgs[i]
        assert 'paymentToken' in m.data.decode('utf-8')
        assert 'COMPLETED' == dpath.util.get(json.loads(m.data.decode('utf-8')),
                                             'paymentToken/statusCode')
        assert m.sequence == i + 1


# Ensure payment messages can get on/off the Queue
@pytest.mark.asyncio
async def test_get_queued_payment_tokens(stan_server, event_loop, client_id, entity_stan, future):
    """Assert that payment tokens can be retrieved and decoded from the Queue."""
    import dpath.util
    from .utils import subscribe_to_queue
    # Call back for the subscription
    msgs = []

    async def cb(msg):
        nonlocal msgs
        nonlocal future
        msgs.append(msg)
        if len(msgs) == 10:
            future.set_result(True)

    entity_subject = await subscribe_to_queue(entity_stan, cb)

    # add payment tokens to queue
    for i in range(0, 5):
        payload = {'paymentToken': {'id': 1234 + i, 'statusCode': 'COMPLETED'}}
        await entity_stan.publish(subject=entity_subject,
                                  payload=json.dumps(payload).encode('utf-8'))
    try:
        await asyncio.wait_for(future, 1, loop=event_loop)
    except Exception as err:  # noqa B902; just in tests
        print(err)

    # check the payment tokens were retrieved from the queue
    assert len(msgs) == 5
    for i in range(0, 5):
        m = msgs[i]
        assert 'paymentToken' in m.data.decode('utf-8')
        assert 'COMPLETED' == dpath.util.get(json.loads(m.data.decode('utf-8')),
                                             'paymentToken/statusCode')
        assert m.sequence == i + 1


# Ensure receipts get sent to the mail queue and
# that the payment record is marked as furnished
@pytest.mark.asyncio
async def test_furnish_receipt_message(app, session, stan_server, event_loop, client_id, entity_stan, future):
    """Assert that events are placed on the email queue and the payment is marked furnished."""
    from queue_common.messages import create_cloud_event_msg
    from queue_common.service import ServiceWorker
    from queue_common.service_utils import subscribe_to_queue
    from namex_pay.worker import APP_CONFIG, furnish_receipt_message, qsm
    from namex.models import Request, State, Payment

    print('test vars')
    print(app, session, stan_server, event_loop, client_id, entity_stan, future)
    # setup
    PAYMENT_TOKEN = 'dog'
    NR_NUMBER = 'NR B000001'
    name_request = Request()
    name_request.nrNum = NR_NUMBER
    name_request.stateCd = State.DRAFT
    name_request._source = 'NRO'
    name_request.save_to_db()

    payment = Payment()
    payment.nrId = name_request.id
    payment._payment_token = PAYMENT_TOKEN
    payment._payment_status_code = 'COMPLETED'
    payment.furnished = False
    payment.save_to_db()

    # file handler callback
    msgs = []
    s = ServiceWorker()
    s.sc = entity_stan
    qsm.service = s

    async def cb_handler(msg):
        nonlocal msgs
        nonlocal future
        msgs.append(msg)
        print('call back recvd')
        if len(msgs) == 1:
            future.set_result(True)

    file_handler_subject = APP_CONFIG.EMAIL_PUBLISH_OPTIONS['subject']
    print(f'file_handler_subject:{file_handler_subject}')

    await subscribe_to_queue(entity_stan,
                             file_handler_subject,
                             f'entity_queue.{file_handler_subject}',
                             f'entity_durable_name.{file_handler_subject}',
                             cb_handler)

    print(payment.as_dict())
    # sanity check
    assert name_request.id
    assert payment.nrId == name_request.id

    # test
    await furnish_receipt_message(qsm, payment)

    try:
        await asyncio.wait_for(future, 1, loop=event_loop)
    except Exception as err:
        print(err)

    # results
    processed_payment = Payment.find_by_payment_token(PAYMENT_TOKEN)

    # verify
    assert processed_payment.furnished
    assert len(msgs) == 1
    cloud_event = json.loads(msgs[0].data.decode('utf-8'))
    assert cloud_event['identifier'] == NR_NUMBER
