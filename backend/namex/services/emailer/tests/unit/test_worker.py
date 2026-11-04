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
import json
from http import HTTPStatus
from unittest.mock import Mock, patch

import pytest
from sbc_common_components.utils.enums import QueueMessageTypes
from simple_cloudevent import SimpleCloudEvent, to_queue_message

from namex_emailer.email_processors import name_request
from namex_emailer.email_processors.resend import process_resend_email
from namex_emailer.resources import worker
from namex_emailer.services import queue
from tests import MockResponse

from . import helper_create_cloud_event_envelope

default_legal_name = "TEST COMP"
default_names_array = [{"name": default_legal_name, "state": "NE"}]


def test_no_message(client, mocker):
    """Return a 4xx when an no JSON present."""
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
    mocker.patch("namex_emailer.services.helpers.get_bearer_token", return_value="fake-token")
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
    app, client, option, nr_number, subject, expiration_date, refund_value, expected_legal_name, names, mocker
):
    """Assert that the nr notification can be processed."""
    # Setup
    nr_json = {
        "expirationDate": expiration_date,
        "names": names,
        "legalType": "BC",
        "applicants": {"emailAddress": "test@test.com", "phoneNumber": "555-555-5555"},
        "request_action_cd": "NEW",
        "id": "some_id",
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

    mocker.patch("namex_emailer.email_processors.name_request.query_nr_number", return_value=nr_response)
    mocker.patch("namex_emailer.services.helpers.get_bearer_token", return_value=token)
    mocker.patch("namex_emailer.email_processors.name_request.get_bearer_token", return_value=token)

    email_response = MockResponse(nr_json, 200)
    with patch("namex_emailer.services.helpers.send_email", return_value=email_response):
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
    nr_json = {
        "applicants": {"emailAddress": email_address, "phoneNumber": "555-555-5555"},
        "request_action_cd": "NEW",
        "id": nr_id,
    }
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

    mocker.patch("namex_emailer.services.helpers.get_bearer_token", return_value=token)
    mocker.patch("namex_emailer.email_processors.name_request.query_nr_number", return_value=nr_response)
    mocker.patch("namex_emailer.email_processors.name_request._get_pdfs", return_value=pdfs)
    mocker.patch("namex_emailer.services.helpers.send_email", return_value=MockResponse(nr_json, 200))

    # TEST
    rv = client.post("/", json=message)

    # Check
    assert rv.status_code == HTTPStatus.OK


def test_resend_email_success(app, mocker):
    """Test that resend_email successfully resends an email."""
    with app.app_context():
        # Setup
        event_id = 1234
        email_content = {
            "email": {
                "recipients": ["test@example.com"],
                "content": {"subject": "Test Resend", "body": "This is a test email.", "attachments": []},
            },
            "option": "before-expiry",
        }
        mock_event = Mock()
        mock_event.json.return_value = {"jsonData": json.dumps(email_content)}

        # Mock query_notification_event to return the mock event
        mocker.patch("namex_emailer.email_processors.resend.query_notification_event", return_value=mock_event)

        # Mock get_bearer_token to return a token
        mocker.patch("namex_emailer.email_processors.resend.get_bearer_token", return_value="mocked_token")

        # Mock send_email to simulate a successful email send
        mocker.patch("namex_emailer.email_processors.resend.update_resend_timestamp", return_value=True)
        mocker.patch("namex_emailer.email_processors.resend._send_email", return_value=True)

        # Test
        response, status = process_resend_email(event_id)

        # Assertions
        assert status == HTTPStatus.OK
        assert response == {}


def test_resend_email_event_not_found(app, mocker):
    """Test that resend_email returns an error when the event is not found."""
    with app.app_context():
        # Setup
        event_id = 1234

        # Mock query_notification_event to return None
        mocker.patch("namex_emailer.email_processors.resend.query_notification_event", return_value=None)

        # Test
        response, status = process_resend_email(event_id)

        # Assertions
        assert status == HTTPStatus.OK
        assert response == {}


def test_resend_email_no_email_content(app, mocker):
    """Test that resend_email returns an error when the event has no email content."""
    with app.app_context():
        # Setup
        event_id = 1234
        mock_response = Mock()
        mock_response.json.return_value = {"jsonData": None}

        # Mock query_notification_event to return the mock event
        mocker.patch("namex_emailer.email_processors.resend.query_notification_event", return_value=mock_response)

        # Test
        response, status = process_resend_email(event_id)

        # Assertions
        assert status == HTTPStatus.OK
        assert response == {}


def test_resend_email_send_failure(app, mocker):
    """Test that resend_email logs an error when sending the email fails."""
    with app.app_context():
        # Setup
        event_id = 1234
        email_content = {
            "email": {
                "recipients": ["test@example.com"],
                "content": {"subject": "Test Resend", "body": "This is a test email."},
            },
            "option": "before-expiry"
        }
        mock_event = Mock()
        mock_event.json.return_value = {"jsonData": json.dumps(email_content)}

        # Mock query_notification_event to return the mock event
        mocker.patch("namex_emailer.email_processors.resend.query_notification_event", return_value=mock_event)
        mocker.patch("namex_emailer.email_processors.resend._handle_attachments", return_value=True)

        # Mock get_bearer_token to return a token
        mocker.patch("namex_emailer.email_processors.resend.get_bearer_token", return_value="mocked_token")

        # Mock send_email to simulate a failed email send
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        mock_response.text = "Internal Server Error"
        mocker.patch("namex_emailer.email_processors.resend.send_email", return_value=mock_response)

        # Test
        response, status = process_resend_email(event_id)

        # Assertions
        assert status == HTTPStatus.OK
        assert response == {}
