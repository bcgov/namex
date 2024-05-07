# Copyright © 2023 Province of British Columbia
#
# Licensed under the BSD 3 Clause License, (the "License");
# you may not use this file except in compliance with the License.
# The template for the license can be found here
#    https://opensource.org/license/bsd-3-clause/
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""The Test Suites to ensure that the worker is operating correctly."""
import base64
from http import HTTPStatus
from unittest.mock import patch

import pytest
from sbc_common_components.utils.enums import QueueMessageTypes
from simple_cloudevent import SimpleCloudEvent, to_queue_message

from namex_emailer.email_processors import name_request
from namex_emailer.resources import worker
from namex_emailer.services import queue
from tests import MockResponse
from . import helper_create_cloud_event_envelope

default_legal_name = 'TEST COMP'
default_names_array = [{'name': default_legal_name, 'state': 'NE'}]


def test_no_message(client, mocker):
    """Return a 4xx when an no JSON present."""
    mocker.patch('gcp_queue.gcp_auth.verify_jwt', return_value='')
    rv = client.post("/")

    assert rv.status_code == HTTPStatus.OK


CLOUD_EVENT = SimpleCloudEvent(
    id="fake-id",
    source="fake-for-tests",
    subject="fake-subject",
    type="email",
    data={"email": {"filingId": "BC1234567", "type": "bn", "option": "COMPLETED"}},
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


@pytest.mark.parametrize(
    "test_name,queue_envelope,expected",
    [("invalid", {}, HTTPStatus.OK), ("valid", CLOUD_EVENT_ENVELOPE, HTTPStatus.OK)],
)
def test_simple_cloud_event(client, test_name, queue_envelope, expected, mocker):
    mocker.patch('gcp_queue.gcp_auth.verify_jwt', return_value='')
    rv = client.post("/", json=CLOUD_EVENT_ENVELOPE)
    assert rv.status_code == expected


@pytest.mark.parametrize(
    ["option", "nr_number", "subject", "expiration_date", "refund_value", "expected_legal_name", "names"],
    [
        (
            "before-expiry",
            "NR 1234567",
            "Expiring Soon",
            "2021-07-20T00:00:00+00:00",
            None,
            "TEST2 Company Name",
            [{"name": "TEST Company Name", "state": "NE"}, {"name": "TEST2 Company Name", "state": "APPROVED"}],
        ),
        (
            "before-expiry",
            "NR 1234567",
            "Expiring Soon",
            "2021-07-20T00:00:00+00:00",
            None,
            "TEST3 Company Name",
            [{"name": "TEST3 Company Name", "state": "CONDITION"}, {"name": "TEST4 Company Name", "state": "NE"}],
        ),
        (
            "expired",
            "NR 1234567",
            "Expired",
            None,
            None,
            "TEST4 Company Name",
            [{"name": "TEST5 Company Name", "state": "NE"}, {"name": "TEST4 Company Name", "state": "APPROVED"}],
        ),
        (
            "renewal",
            "NR 1234567",
            "Confirmation of Renewal",
            "2021-07-20T00:00:00+00:00",
            None,
            None,
            default_names_array,
        ),
        ("upgrade", "NR 1234567", "Confirmation of Upgrade", None, None, None, default_names_array),
        ("refund", "NR 1234567", "Refund request confirmation", None, "123.45", None, default_names_array),
    ],
)
def test_nr_notification(
    app, client, option, nr_number, subject, expiration_date, refund_value, expected_legal_name, names , mocker
):
    """Assert that the nr notification can be processed."""
    # Setup
    nr_json = {
        "expirationDate": expiration_date,
        "names": names,
        "legalType": "BC",
        "applicants": {"emailAddress": "test@test.com"},
        "id": "some_id"
    }
    nr_response = MockResponse(nr_json, 200)
    token = "token"
    email_msg = {
        "id": "123456789",
        "type": QueueMessageTypes.NAMES_MESSAGE_TYPE.value,
        "source": f"/requests/{nr_number}",
        "data": {"request": {"nrNum": nr_number, "option": option, "refundValue": refund_value}},
    }
    message = helper_create_cloud_event_envelope(data=email_msg)

    mocker.patch('namex_emailer.services.helpers.query_nr_number', return_value=nr_response)
    mocker.patch('namex_emailer.services.helpers.get_bearer_token', return_value=token)
    mocker.patch('gcp_queue.gcp_auth.verify_jwt', return_value='')

    email_response = MockResponse(nr_json, 200)
    with patch.object(worker, "send_email", return_value=email_response):
        with patch.object(queue, "publish", return_value={}):
            # TEST
            rv = client.post("/", json=message)

            # Check
            assert rv.status_code == HTTPStatus.OK


def test_nr_receipt_notification(app, client, mocker):
    """Assert that the nr payment notification can be processed."""
    # Setup
    nr_number = "NR 1234567"
    email_address = "test@test.com"
    nr_id = 12345
    nr_json = {"applicants": {"emailAddress": email_address}, "id": nr_id}
    nr_response = MockResponse(nr_json, 200)
    token = "token"
    payment_token = "1234"
    pdfs = ["test"]
    email_msg = {
        "id": "123456789",
        "type": QueueMessageTypes.NAMES_MESSAGE_TYPE.value,
        "source": f"/requests/{nr_number}",
        "data": {
            "request": {
                "header": {"nrNum": nr_number},
                "paymentToken": payment_token,
                "statusCode": "DRAFT",  # not used
            }
        },
    }
    message = helper_create_cloud_event_envelope(data=email_msg)

    mocker.patch('namex_emailer.services.helpers.query_nr_number', return_value=nr_response)
    mocker.patch('namex_emailer.services.helpers.get_bearer_token', return_value=token)
    mocker.patch('gcp_queue.gcp_auth.verify_jwt', return_value='')
    email_response = MockResponse(nr_json, 200)

    with patch.object(name_request, "_get_pdfs", return_value=pdfs):
        with patch.object(worker, "send_email", return_value=email_response):
            with patch.object(queue, "publish", return_value={}):
                # TEST
                rv = client.post("/", json=message)

                # Check
                assert rv.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    "email_msg",
    [
        ({}),
        (
            {
                "recipients": "",
                "requestBy": "test@test.ca",
                "content": {"subject": "test", "body": "test", "attachments": []},
            }
        ),
        ({"recipients": "", "requestBy": "test@test.ca", "content": {}}),
        (
            {
                "recipients": "",
                "requestBy": "test@test.ca",
                "content": {"subject": "test", "body": {}, "attachments": []},
            }
        ),
        ({"requestBy": "test@test.ca", "content": {"subject": "test", "body": "test", "attachments": []}}),
        ({"recipients": "test@test.ca", "requestBy": "test@test.ca"}),
        (
            {
                "recipients": "test@test.ca",
                "requestBy": "test@test.ca",
                "content": {"subject": "test", "attachments": []},
            }
        ),
    ],
)
def test_send_email_with_incomplete_payload(app, client, email_msg, mocker):
    """Assert that the email not have body can not be processed."""
    # Setup
    message = helper_create_cloud_event_envelope(data=email_msg)
    mocker.patch('gcp_queue.gcp_auth.verify_jwt', return_value='')
    # TEST
    rv = client.post("/", json=message)

    # Check
    assert rv.status_code == HTTPStatus.OK
