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
"""The Test Suites to ensure that the worker is operating correctly."""
from datetime import timedelta
from namex.models import Request, State, Payment
import json

import pytest
from freezegun import freeze_time
from queue_common.service_utils import QueueException
import namex_pay

from namex_pay.utils.datetime import datetime, timedelta
from namex_pay.worker import NAME_REQUEST_LIFESPAN_DAYS


def test_extract_payment_token():
    """Assert that the payment token can be extracted from the Queue delivered Msg."""
    from namex_pay.worker import extract_message
    from stan.aio.client import Msg
    import stan.pb.protocol_pb2 as protocol

    # setup
    token = {'paymentToken': {'id': 1234, 'statusCode': 'COMPLETED'}}
    msg = Msg()
    msg.proto = protocol.MsgProto
    msg.proto.data = json.dumps(token).encode('utf-8')

    # test and verify
    assert extract_message(msg) == token


@pytest.mark.parametrize(
    'test_name,action_code,start_request_state,end_request_state,'
    'start_priority,end_priority,'
    'start_datetime,days_after_start_datetime,'
    'start_payment_state,end_payment_state,'
    'start_payment_date,end_payment_has_value,'
    'error', [
        ('draft',  # test name
         Payment.PaymentActions.CREATE.value,  # payment action [CREATE|UPGRADE|REAPPLY]
         State.PENDING_PAYMENT,  # start state of NR
         State.DRAFT,           # end state of NR
         'N',  # start state of Priority
         'N',  # end state of Priority
         None,  # start of frozen time
         NAME_REQUEST_LIFESPAN_DAYS,  # days after frozen time
         None,  # start_payment_completion_state
         'COMPLETED',  # end_payment_completion_state
         None,  # start_payment_date
         'is not',  # end_payment_has_value
         None  # error
         ),
        ('already draft', Payment.PaymentActions.CREATE.value, State.DRAFT, State.DRAFT, 'N', 'N', datetime.utcnow(), 0, 'COMPLETED', 'COMPLETED', None, 'is', None),
        ('upgrade', Payment.PaymentActions.UPGRADE.value, State.DRAFT, State.DRAFT, 'N', 'Y', datetime.utcnow(), 0, 'PENDING_PAYMENT', 'COMPLETED', None, 'is not', None),
        ('re-upgrade', Payment.PaymentActions.UPGRADE.value, State.DRAFT, State.DRAFT, 'Y', 'Y', datetime.utcnow(), 0, 'PENDING_PAYMENT', 'COMPLETED', None, 'is not', None),
        ('extend ', Payment.PaymentActions.REAPPLY.value, State.DRAFT, State.DRAFT, 'N', 'N',
         datetime.utcnow() + timedelta(days=3), NAME_REQUEST_LIFESPAN_DAYS, 'PENDING_PAYMENT', 'COMPLETED', None, 'is not', None),
        ('extend expired', Payment.PaymentActions.REAPPLY.value, State.DRAFT, State.DRAFT, 'N', 'N',
         datetime.utcnow() - timedelta(days=(NAME_REQUEST_LIFESPAN_DAYS + 3)), NAME_REQUEST_LIFESPAN_DAYS, 'PENDING_PAYMENT', 'PENDING_PAYMENT',
         None, 'is',
         QueueException),
    ])
@pytest.mark.asyncio
async def test_update_payment_record(app, session,
                                     test_name,
                                     action_code,
                                     start_request_state, end_request_state,
                                     start_priority, end_priority,
                                     start_datetime, days_after_start_datetime,
                                     start_payment_state, end_payment_state,
                                     start_payment_date, end_payment_has_value,
                                     error
                                     ):
    """Assert that the update_payment_record works as expected."""
    from namex.models import Request, State, Payment
    from namex_pay.worker import update_payment_record

    print(test_name)

    now = datetime.utcnow()

    with freeze_time(now):
        # setup
        PAYMENT_TOKEN = 'dog'
        NR_NUMBER = 'NR B000001'
        name_request = Request()
        name_request.nrNum = NR_NUMBER
        name_request.stateCd = start_request_state
        name_request._source = 'NRO'
        name_request.expirationDate = start_datetime
        name_request.priorityCd = start_priority
        name_request.save_to_db()

        payment = Payment()
        payment.nrId = name_request.id
        payment._payment_token = PAYMENT_TOKEN
        payment._payment_status_code = start_payment_state
        payment.payment_action = action_code
        payment.furnished = False
        payment._payment_completion_date = start_payment_date
        payment.save_to_db()

        # run test
        if error:  # expecting it to raise an error
            with pytest.raises(error):
                await update_payment_record(payment)
        else:
            # else it was processable
            if not (payment_final := await update_payment_record(payment)):
                payment_final = payment

            nr_final = Request.find_by_nr(NR_NUMBER)

            assert nr_final.stateCd == end_request_state
            assert nr_final.priorityCd == end_priority
            assert nr_final.expirationDate == (start_datetime or now) + timedelta(days=days_after_start_datetime)
            assert eval(f'payment_final.payment_completion_date {end_payment_has_value} None')
            assert payment_final.payment_status_code == end_payment_state


@pytest.mark.parametrize(
    'test_name,action_code,start_request_state,'
    'start_priority,'
    'start_datetime,'
    'start_payment_state,'
    'start_payment_date,'
    , [
        ('draft',  # test name
         Payment.PaymentActions.CREATE.value,  # payment action [COMPLETE|UPGRADE|REAPPLY]
         State.PENDING_PAYMENT,  # start state of NR
         'N',  # start state of Priority
         None,  # start of frozen time
         None,  # start_payment_completion_state
         None,  # start_payment_date
         ),
         ])
async def test_process_payment(app, session, mocker,
                                     test_name,
                                     action_code,
                                     start_request_state,
                                     start_priority,
                                     start_datetime,
                                     start_payment_state,
                                     start_payment_date,
                                     ):
    from namex.models import Request, State, Payment
    from namex_pay.worker import process_payment, FLASK_APP

    # setup
    PAYMENT_TOKEN = 'dog'
    NR_NUMBER = 'NR B000001'
    name_request = Request()
    name_request.nrNum = NR_NUMBER
    name_request.stateCd = start_request_state
    name_request._source = 'NRO'
    name_request.expirationDate = start_datetime
    name_request.priorityCd = start_priority
    name_request.save_to_db()

    payment = Payment()
    payment.nrId = name_request.id
    payment._payment_token = PAYMENT_TOKEN
    payment._payment_status_code = start_payment_state
    payment.payment_action = action_code
    payment.furnished = False
    payment._payment_completion_date = start_payment_date
    payment.save_to_db()

    # setup mock and patch
    msg=None
    def catch(qsm,cloud_event_msg):
        nonlocal msg
        msg=cloud_event_msg

    mocker.patch('namex_pay.worker.publish_email_message', side_effect=catch)

    # Test
    pay_msg = {"paymentToken": {"id": PAYMENT_TOKEN, "statusCode": "COMPLETED", "filingIdentifier": None}}
    await process_payment(pay_msg,FLASK_APP)

    print (msg)
    # Verify message that would be sent to the email server
    assert msg['type'] == 'bc.registry.names.request'
    assert msg['source'] == '/requests/NR B000001'
    assert msg['datacontenttype'] == 'application/json'
    assert msg['identifier'] == 'NR B000001'
    assert msg['data']['request']['header']['nrNum'] == NR_NUMBER
    assert msg['data']['request']['paymentToken'] == PAYMENT_TOKEN
    assert msg['data']['request']['statusCode'] == 'DRAFT'
