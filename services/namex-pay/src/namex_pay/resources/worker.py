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

"""
import re
import time
from dataclasses import dataclass
from enum import Enum
from http import HTTPStatus
from typing import Optional

import google.oauth2.id_token as id_token
from cachecontrol import CacheControl
from flask import Blueprint, current_app, request
from google.auth.transport.requests import Request
from namex import nro
from namex.models import db, Event, Payment, Request as RequestDAO, State, User  # noqa:I001; import orders
from namex.services import EventRecorder, queue, is_reapplication_eligible  # noqa:I005;
from queue_common.messages import create_cloud_event_msg  # noqa:I005
from queue_common.service import QueueServiceManager
from queue_common.service_utils import QueueException, logger

from sentry_sdk import capture_message
from simple_cloudevent import SimpleCloudEvent

from namex_pay.services import queue
from namex_pay.services.logging import structured_log
from namex_pay.utils import datetime, timedelta

bp = Blueprint("worker", __name__)

NAME_REQUEST_LIFESPAN_DAYS = 56  # TODO this should be defined as a lookup from somewhere
NAME_REQUEST_EXTENSION_PAD_HOURS = 12  # TODO this should be defined as a lookup from somewhere

class PaymentState(Enum):
    """Render all the payment states we know what to do with."""

    APPROVED = 'APPROVED'
    COMPLETED = 'COMPLETED'
    TRANSACTION_FAILED = 'TRANSACTION_FAILED'


@bp.route("/", methods=("POST",))
def worker():
    """Process the incoming cloud event.

    Flow
    --------
    1. Get cloud event
    2. Get filing and payment information
    3. Process payment

    Decisions on returning a 2xx or failing value to
    the Queue should be noted here:
    - Empty or garbaled messages are knocked off the Q
    - If the Filing is already marked paid, skip and knock off Q
    - Once the filing is marked paid, no errors should escape to the Q
    - If there's no matching filing, put back on Q
    """
    session = Session()
    cached_session = CacheControl(session)

    if len(verify_res := verify_jwt(request, cached_session)) > 0:
        return f"{verify_res}\n", HTTPStatus.UNAUTHORIZED

    structured_log(request, "INFO", f"Incoming raw msg: {request.data}")

    # 1. Get cloud event
    # ##
    if not (ce := queue.get_simple_cloud_event(request)):
        #
        # Decision here is to return a 200,
        # so the event is removed from the Queue
        return {}, HTTPStatus.OK

    structured_log(request, "INFO", f"received ce: {str(ce)}")
    structured_log(request, "INFO", f"Incoming raw msg: {request.headers}")


    # 2. Get payment information
    # ##
    if not (payment_token := get_payment_token(ce)) or payment_token.status_code != "COMPLETED":
    # no payment info, or not a payment COMPLETED token, take off Q
        return {}, HTTPStatus.OK

    # 3. Process payment 
    # ##
    with current_app.app_context():
        structured_log(request, "INFO", f"process namex payment for pay-id: {payment_token.id}")
        process_payment(ce)

    structured_log(request, "INFO", f"completed ce: {str(ce)}")
    return {}, HTTPStatus.OK

@dataclass
class PaymentToken:
    """Payment Token class"""

    id: Optional[str] = None
    status_code: Optional[str] = None
    filing_identifier: Optional[str] = None
    corp_type_code: Optional[str] = None


def verify_jwt(request, cached_session):
    try:
        msg = ''
        if current_app.config.get("DEBUG_REQUEST"):
            structured_log(request, "INFO", f"Headers: {request.headers}")

        # Get the Cloud Pub/Sub-generated JWT in the "Authorization" header.
        bearer_token = request.headers.get("Authorization")
        token = bearer_token.split(" ")[1]

        claim = id_token.verify_oauth2_token(
            token, Request(session=cached_session), audience=current_app.config.get("NAMEX_SUB_AUDIENCE")
        )

        if claim['email'] != current_app.config.get("NAMEX_SUB_SA_EMAIL") or not claim['email_verified']:
            msg = f'Wrong service account email provided={current_app.config.get("NAMEX_SUB_SA_EMAIL")}'
    except Exception as e:
        msg = f"Invalid token: {e}\n"
    finally:
        return msg


def get_payment_token(ce: SimpleCloudEvent):
    """Return a PaymentToken if enclosed in the cloud event."""
    if (
        (ce.type == "payment")
        and (data := ce.data)
        and isinstance(data, dict)
        and (payment_token := data.get("paymentToken", {}))
    ):
        converted = dict_keys_to_snake_case(payment_token)
        pt = PaymentToken(**converted)
        return pt
    return None


def dict_keys_to_snake_case(d: dict):
    """Convert the keys of a dict to snake_case"""
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    converted = {}
    for k, v in d.items():
        converted[pattern.sub("_", k).lower()] = v
    return converted


# async def update_payment_record(payment: Payment) -> Optional[Payment]:
def update_payment_record(payment: Payment) -> Optional[Payment]:

    """Update the payment record in the database.

    Alter the NR state as required based on the payment action.
    Payment NR Action - One of [COMPLETE, UPGRADE, REAPPLY]
    COMPLETE - set NR to DRAFT IFF nr.state == PENDING_PAYMENT
    UPGRADE - set the nr.priority to True/'Y'
    REAPPLY - add REAPPLY_EXTENSION to expiry date of NR IFF it hasn't expired
    """
    if payment.payment_completion_date:
        msg = f'Queue Issue: Duplicate, payment already processed for payment.id={payment.id}'
        structured_log(request, message=msg)
        capture_message(msg)
        return None

    payment_action = payment.payment_action
    nr: RequestDAO = RequestDAO.find_by_id(payment.nrId)

    match payment_action:
        case Payment.PaymentActions.CREATE.value:
            create_payment(nr, payment)
        case Payment.PaymentActions.RESUBMIT.value:
            create_payment(nr, payment)
        case Payment.PaymentActions.UPGRADE.value:
            upgrade_payment(nr, payment)
        case Payment.PaymentActions.REAPPLY.value:
            reapply_payment(nr, payment)
        case _:
            msg = f'Queue Issue: Unknown action:{payment_action} for payment.id={payment.id}'
            structured_log(request, message=msg)
            capture_message(msg)
            raise Exception(f'Unknown action:{payment_action} for payment.id={payment.id}')


def reapply_payment(nr, payment):
    if nr.stateCd != State.APPROVED \
        and nr.expirationDate + timedelta(hours=NAME_REQUEST_EXTENSION_PAD_HOURS) < datetime.utcnow():
        msg = f'Queue Issue: Failed attempt to extend NR for payment.id={payment.id} '\
            'nr.state{nr.stateCd}, nr.expires:{nr.expirationDate}'
        structured_log(request, message=msg)
        capture_message(msg)
        raise Exception(msg)
    if is_reapplication_eligible(nr.expriationDate):
        # to avoid duplicate expiration date calculated
        nr.expirationDate = nr.expirationDate + timedelta(days=NAME_REQUEST_LIFESPAN_DAYS)
    payment.payment_completion_date = datetime.utcnow()
    payment.payment_status_code = State.COMPLETED

    nr.save_to_db()
    payment.save_to_db()
    return payment


def create_payment(nr, payment):
    # pylint: disable=R1705
    if nr.stateCd == State.PENDING_PAYMENT:
        nr.stateCd = State.DRAFT
        nr.save_to_db()
    payment.payment_completion_date = datetime.utcnow()
    payment.payment_status_code = State.COMPLETED
    payment.save_to_db()
    return payment


def upgrade_payment(nr, payment):
    if nr.stateCd == State.PENDING_PAYMENT:
        msg = f'Queue Issue: Upgrading a non-DRAFT NR for payment.id={payment.id}'
        structured_log(request, message=msg)
        capture_message(msg)
        raise Exception(msg)

    nr.priorityCd = 'Y'
    nr.priorityDate = datetime.utcnow()
    payment.payment_completion_date = datetime.utcnow()
    payment.payment_status_code = State.COMPLETED
    nr.save_to_db()
    payment.save_to_db()
    return payment


# async def furnish_receipt_message(payment: Payment):  # pylint: disable=redefined-outer-name
def furnish_receipt_message(payment: Payment):  # pylint: disable=redefined-outer-name
    """Send receipt info to the mail queue if it hasn't yet been done."""
    if payment.furnished is True:
        msg = f'Queue Issue: Duplicate, already furnished receipt for payment.id={payment.id}'
        structured_log(request, message=msg)
        capture_message(msg)
        return

    nr = None
    msg = f'Start of the furnishing of receipt for payment record:{payment.as_dict()}'
    structured_log(request, message=msg)
    try:
        payment.furnished = True
        payment.save_to_db()
    except Exception as err:  # noqa: B902; bare exception to catch all
        raise Exception('Unable to alter payment record.') from err

    try:
        nr = RequestDAO.find_by_id(payment.nrId)
        cloud_event_msg = SimpleCloudEvent(
        source=__name__[: __name__.find(".")],
        subject="namerequest",
        type="bc.registry.names.request",
        data={
            'request': {
                'header': {'nrNum': nr.nrNum},
                'paymentToken': payment.payment_token,
                'statusCode': nr.stateCd
            }}
        )
        msg = f'About to publish email for payment.id={payment.id}'
        # structured_log(message=msg)
        with current_app.app_context():
            namex_topic = current_app.config.get("NAMEX_RECEIPT_TOPIC", None)
            payload = queue.to_queue_message(cloud_event_msg)
            queue.publish(topic=namex_topic, payload=payload)  # noqa: F841

    except Exception as err:  # noqa: B902; bare exception to catch all
        payment.furnished = False
        payment.save_to_db()
        msg = f'Reset payment furnish status payment.id={payment.id}'
        structured_log(request, message=msg)
        raise Exception(err)


# async def process_payment(pay_msg: dict):
def process_payment(ce: SimpleCloudEvent):
    """Render the payment status."""
    structured_log(ce, 'DEBUG', 'entering process payment')

    pay_msg = get_payment_token(ce)

    if pay_msg.status_code == PaymentState.TRANSACTION_FAILED.value:
        # TODO: The customer has cancelled out of paying, so we could note this better
        # technically the payment for this service is still pending
        structured_log(pay_msg, 'ERROR', 'Failed transaction on queue')
        return

    complete_payment_status = [PaymentState.COMPLETED.value, PaymentState.APPROVED.value]
    if pay_msg.status_code in complete_payment_status:  # pylint: disable=R1702
        msg = f'COMPLETED transaction on queue:{pay_msg}'
        structured_log(request, message=msg)
        if payment_token := pay_msg.id:
            payment = None
            counter = 1
            while not payment and counter <= 5:
                payment = Payment.find_by_payment_token(payment_token)
                counter += 1
                if not payment:
                    time.sleep(0.2)

            if not payment:
                msg = f'Queue Error: Unable to find payment record for :{pay_msg}'
                structured_log(request, message=msg)
                capture_message(f'Queue Error: Unable to find payment record for :{pay_msg}', level='error')
                raise Exception(msg)

            if update_payment := update_payment_record(payment):
                payment = update_payment
                # record event
                nr = RequestDAO.find_by_id(payment.nrId)
                # TODO: create a namex_pay user for this
                user = User.find_by_username('name_request_service_account')
                EventRecorder.record(
                    user,
                    Event.NAMEX_PAY + f' [payment completed] { payment.payment_action }',
                    nr,
                    nr.json()
                )
                # try to update NRO otherwise send a sentry msg for OPS
                if payment.payment_action in \
                        [payment.PaymentActions.UPGRADE.value, payment.PaymentActions.REAPPLY.value]:
                    change_flags = {
                        'is_changed__request': True,
                        'is_changed__previous_request': False,
                        'is_changed__applicant': False,
                        'is_changed__address': False,
                        'is_changed__name1': False,
                        'is_changed__name2': False,
                        'is_changed__name3': False,
                        'is_changed__nwpta_ab': False,
                        'is_changed__nwpta_sk': False,
                        'is_changed__request_state': False,
                        'is_changed_consent': False
                    }
                    warnings = nro.change_nr(nr, change_flags)
                    if warnings:
                        msg = f'Queue Error: Unable to update NRO :{warnings}'
                        # structured_log(message=msg)
                        capture_message(
                            f'Queue Error: Unable to update NRO for {nr} {payment.payment_action} :{warnings}',
                            level='error'
                        )

            furnish_receipt_message(payment)
        else:
            msg = f'Queue Error: Missing id :{pay_msg}'
            structured_log(request, message=msg)
            capture_message(f'Queue Error: Missing id :{pay_msg}', level='error')

        return