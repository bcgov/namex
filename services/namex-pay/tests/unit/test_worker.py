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
import base64
import json
from datetime import timedelta
from http import HTTPStatus
import pytest
from freezegun import freeze_time
from namex.models import Payment, Request, State
from simple_cloudevent import SimpleCloudEvent, to_queue_message

from namex_pay.resources.worker import NAME_REQUEST_LIFESPAN_DAYS, get_payment_token
from namex_pay.utils import datetime, timedelta
from tests.unit import nested_session

CLOUD_EVENT = SimpleCloudEvent(
    id="fake-id",
    source="fake-for-tests",
    subject="fake-subject",
    type="payment",
    data={
        "paymentToken": {
            "id": "29590",
            "statusCode": "COMPLETED",
            "filingIdentifier": 12345,
            "corpTypeCode": "BC",
        }
    },
)


#
# This needs to mimic the envelope created by GCP PubSb when call a resource
#
CLOUD_EVENT_ENVELOPE = {
    "subscription": "projects/PUBSUB_PROJECT_ID/subscriptions/SUBSCRIPTION_ID",
    "message": {
        "data": base64.b64encode(to_queue_message(CLOUD_EVENT)).decode("UTF-8"),
        "messageId": "10",
        "attributes": {},
    },
    "id": 1,
}

def test_no_message(client, mocker):
    """Return a 4xx when an no JSON present."""

    mocker.patch("gcp_queue.gcp_auth.verify_jwt", return_value='')

    rv = client.post("/")

    assert rv.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    "test_name,queue_envelope,expected",
    [("invalid", {}, HTTPStatus.OK), ("valid", CLOUD_EVENT_ENVELOPE, HTTPStatus.OK)],
)
def test_simple_cloud_event(client, session, mocker, test_name, queue_envelope, expected):

    mocker.patch("gcp_queue.gcp_auth.verify_jwt", return_value='')
    with nested_session(session):
        request = Request()
        payment = Payment()
        payment.nrId = request.id
        payment._payment_token = 29590
        request.payments = payment
        request.save()

        rv = client.post("/", json=CLOUD_EVENT_ENVELOPE)

        assert rv.status_code == expected

def test_get_payment_token():
    """Test that the payment token is retrieved."""
    from copy import deepcopy

    CLOUD_EVENT_TEMPLATE = {
        "data": {
            "paymentToken": {
                "id": 29590,
                "statusCode": "COMPLETED",
                "filingIdentifier": None,
                "corpTypeCode": None
                }
        },
        "id": 29590,
        "source": "sbc-pay",
        "subject": "BC1234567",
        "time": "2023-07-05T22:04:25.952027",
        "type": "payment",
    }

    # base - should pass
    ce_dict = deepcopy(CLOUD_EVENT_TEMPLATE)
    ce = SimpleCloudEvent(**ce_dict)
    payment_token = get_payment_token(ce)
    assert payment_token
    assert payment_token.id == ce_dict["data"]["paymentToken"]["id"]

    # wrong type
    ce_dict = deepcopy(CLOUD_EVENT_TEMPLATE)
    ce_dict["type"] = "not-a-payment"
    ce = SimpleCloudEvent(**ce_dict)
    payment_token = get_payment_token(ce)
    assert not payment_token


@pytest.mark.parametrize(
    'test_name,action_code,start_request_state,end_request_state,'
    'start_priority,end_priority,'
    'start_datetime,days_after_start_datetime,'
    'start_payment_state,end_payment_state,'
    'start_payment_date,end_payment_has_value,'
    'error', [
        ('draft',  # test name
         Payment.PaymentActions.CREATE.value,  # payment action [CREATE|UPGRADE|REAPPLY|RESUBMIT]
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
        ('already draft', Payment.PaymentActions.CREATE.value, State.DRAFT, State.DRAFT, 'N', 'N', datetime.utcnow(), 0, 'COMPLETED', 'COMPLETED', None, 'is not', None),
        ('resubmit', Payment.PaymentActions.RESUBMIT.value, State.PENDING_PAYMENT, State.DRAFT, 'N', 'N', datetime.utcnow(), 0, None, 'COMPLETED', None, 'is not', None),
        ('resubmit draft', Payment.PaymentActions.RESUBMIT.value, State.DRAFT, State.DRAFT, 'N', 'N', datetime.utcnow(), 0, 'COMPLETED', 'COMPLETED', None, 'is not', None),
        ('upgrade', Payment.PaymentActions.UPGRADE.value, State.DRAFT, State.DRAFT, 'N', 'Y', datetime.utcnow(), 0, 'PENDING_PAYMENT', 'COMPLETED', None, 'is not', None),
        ('re-upgrade', Payment.PaymentActions.UPGRADE.value, State.DRAFT, State.DRAFT, 'Y', 'Y', datetime.utcnow(), 0, 'PENDING_PAYMENT', 'COMPLETED', None, 'is not', None),
        ('extend ', Payment.PaymentActions.REAPPLY.value, State.DRAFT, State.DRAFT, 'N', 'N',
         datetime.utcnow() + timedelta(days=3), NAME_REQUEST_LIFESPAN_DAYS, 'PENDING_PAYMENT', 'COMPLETED', None, 'is not', None),
        ('extend expired', Payment.PaymentActions.REAPPLY.value, State.DRAFT, State.DRAFT, 'N', 'N',
         datetime.utcnow() - timedelta(days=(NAME_REQUEST_LIFESPAN_DAYS + 3)), NAME_REQUEST_LIFESPAN_DAYS, 'PENDING_PAYMENT', 'PENDING_PAYMENT',
         None, 'is',
         Exception),
    ])
def test_update_payment_record(app,
                                     session,
                                     client,
                                     mocker,
                                     test_name,
                                     action_code,
                                     start_request_state, end_request_state,
                                     start_priority, end_priority,
                                     start_datetime, days_after_start_datetime,
                                     start_payment_state, end_payment_state,
                                     start_payment_date, end_payment_has_value,
                                     error,
                                     queue_publish
                                     ):
    """Assert that the update_payment_record works as expected."""
    mocker.patch("namex.utils.queue_util.send_name_request_state_msg")
    mocker.patch("namex.utils.queue_util.publish_email_notification")

    from namex.models import Payment, Request

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

        payment_token = {"paymentToken": {"id": PAYMENT_TOKEN, "statusCode": "COMPLETED", "filingIdentifier": None, "corpTypeCode": None}}

        message = helper_create_cloud_event_envelope(source="sbc-pay", subject="payment", data=payment_token)

        mocker.patch("gcp_queue.gcp_auth.verify_jwt", return_value='')

        if error:  # expecting it to raise an error
            with pytest.raises(error):
                client.post("/", json=message)
        else:
            rv = client.post("/", json=message)

            # Check
            topics = queue_publish['topics']
            msg = queue_publish['msg']

            assert rv.status_code == HTTPStatus.OK
            assert len(topics) == 1
            mailer = app.config.get("NAMEX_RECEIPT_TOPIC")
            assert mailer in topics

            email_pub = json.loads(msg.decode("utf-8").replace("'",'"'))

            # Verify message that would be sent to the emailer pubsub
            assert email_pub['type'] == 'bc.registry.names.request'
            assert email_pub['source'] == 'namex_pay'
            assert email_pub['subject'] == 'namerequest'
            assert email_pub['data']['request']['header']['nrNum'] == NR_NUMBER
            assert email_pub['data']['request']['paymentToken'] == PAYMENT_TOKEN
            assert email_pub['data']['request']['statusCode'] == State.DRAFT

            nr_final = Request.find_by_nr(NR_NUMBER)
            payments = nr_final.payments

            payment_final = payments[0]

            assert nr_final.stateCd == end_request_state
            assert nr_final.priorityCd == end_priority
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
         Payment.PaymentActions.CREATE.value,  # payment action [CREATE|UPGRADE|REAPPLY]
         State.PENDING_PAYMENT,  # start state of NR
         'N',  # start state of Priority
         None,  # start of frozen time
         None,  # start_payment_completion_state
         None,  # start_payment_date
         ),
         ])
def test_process_payment(app,
                        session,
                        client,
                        mocker,
                        test_name,
                        action_code,
                        start_request_state,
                        start_priority,
                        start_datetime,
                        start_payment_state,
                        start_payment_date,
                        queue_publish
                        ):
    from namex.models import Payment, Request, State

    mocker.patch("namex.utils.queue_util.send_name_request_state_msg")
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

    # Test
    payment_token = {"paymentToken": {"id": PAYMENT_TOKEN, "statusCode": "COMPLETED", "filingIdentifier": None, "corpTypeCode": None}}
    
    message = helper_create_cloud_event_envelope(source="sbc-pay", subject="payment", data=payment_token)

    mocker.patch("gcp_queue.gcp_auth.verify_jwt", return_value='')

    rv = client.post("/", json=message)

    topics = queue_publish['topics']
    msg = queue_publish['msg']
    # Check
    assert rv.status_code == HTTPStatus.OK
    assert len(topics) == 1
    mailer = app.config.get("NAMEX_RECEIPT_TOPIC")
    assert mailer in topics

    # Get modified data
    nr_from_db = Request.find_by_nr(NR_NUMBER)
    # check it out
    assert nr_from_db.nrNum == NR_NUMBER
    assert nr_from_db.stateCd == State.DRAFT

    payments = nr_from_db.payments
    payments[0].payment_status_code == State.COMPLETED
    payments[0].payment_token == PAYMENT_TOKEN

    email_pub = json.loads(msg.decode("utf-8").replace("'",'"'))

    # Verify message that would be sent to the emailer pubsub
    assert email_pub['type'] == 'bc.registry.names.request'
    assert email_pub['source'] == 'namex_pay'
    assert email_pub['subject'] == 'namerequest'
    assert email_pub['data']['request']['header']['nrNum'] == NR_NUMBER
    assert email_pub['data']['request']['paymentToken'] == PAYMENT_TOKEN
    assert email_pub['data']['request']['statusCode'] == State.DRAFT


def helper_create_cloud_event_envelope(
    cloud_event_id: str = None,
    source: str = "fake-for-tests",
    subject: str = "fake-subject",
    type: str = "payment",
    data: dict = {},
    pubsub_project_id: str = "PUBSUB_PROJECT_ID",
    subscription_id: str = "SUBSCRIPTION_ID",
    message_id: int = 1,
    envelope_id: int = 1,
    attributes: dict = {},
    ce: SimpleCloudEvent = None,
):
    if not data:
        data = {
            "paymentToken": {
                "id": "29590",
                "statusCode": "COMPLETED",
                "filingIdentifier": 12345            }
        }
    if not ce:
        ce = SimpleCloudEvent(id=cloud_event_id, source=source, subject=subject, type=type, data=data)
    #
    # This needs to mimic the envelope created by GCP PubSb when call a resource
    #
    envelope = {
        "subscription": f"projects/{pubsub_project_id}/subscriptions/{subscription_id}",
        "message": {
            "data": base64.b64encode(to_queue_message(ce)).decode("UTF-8"),
            "messageId": str(message_id),
            "attributes": attributes,
        },
        "id": envelope_id,
    }
    return envelope