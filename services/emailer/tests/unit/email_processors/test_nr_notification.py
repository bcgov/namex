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
"""The Unit Tests for the name request expiry email processor."""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import pytest
from sbc_common_components.utils.enums import QueueMessageTypes

from namex_emailer.constants.notification_options import Option
from namex_emailer.email_processors import nr_notification
from namex_emailer.services.helpers import as_legislation_timezone, format_as_report_string
from tests import MockResponse

from .. import helper_create_cloud_event

default_legal_name = "TEST COMP"
default_names_array = [{"name": default_legal_name, "state": "NE"}]


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
    app, option, nr_number, subject, expiration_date, refund_value, expected_legal_name, names, mocker
):
    """Assert that the nr notification can be processed."""
    with app.app_context():
        nr_json = {
            "expirationDate": expiration_date,
            "names": names,
            "legalType": "BC",
            "applicants": {"emailAddress": "test@test.com", "phoneNumber": "555-555-5555"},
            "request_action_cd": "NEW",
            "nrNum": nr_number,
        }
        nr_response = MockResponse(nr_json, 200)
        mocker.patch("namex_emailer.email_processors.nr_notification.query_nr_number", return_value=nr_response)
        email_msg = {"request": {"nrNum": nr_number, "option": option, "refundValue": refund_value}}
        message = helper_create_cloud_event(
            data=email_msg,
            type=QueueMessageTypes.NAMES_MESSAGE_TYPE.value,
        )
        email = nr_notification.process(
            message,
            option,
        )

        assert email["content"]["subject"] == f"{nr_number} - {subject}"

        assert "test@test.com" in email["recipients"]
        assert email["content"]["body"]
        if option == Option.REFUND.value:
            assert f"${refund_value} CAD" in email["content"]["body"]
        assert email["content"]["attachments"] == []

        if option == Option.BEFORE_EXPIRY.value:
            assert nr_number in email["content"]["body"]
            assert expected_legal_name in email["content"]["body"]
            exp_date = datetime.fromisoformat(expiration_date)
            exp_date_tz = as_legislation_timezone(exp_date)
            assert_expiration_date = format_as_report_string(exp_date_tz)
            assert assert_expiration_date in email["content"]["body"]

        if option == Option.EXPIRED.value:
            assert nr_number in email["content"]["body"]
            assert expected_legal_name in email["content"]["body"]


def test_legislation_timezone_offsets():
    utc = ZoneInfo("UTC")
    van = ZoneInfo("America/Vancouver")
    la = ZoneInfo("America/Los_Angeles")
    nov = datetime(2026, 11, 1, 9, 1, tzinfo=utc)
    jan = datetime(2026, 1, 15, 20, 0, tzinfo=utc)
    assert nov.astimezone(van).utcoffset().total_seconds() == -7 * 3600
    assert nov.astimezone(la).utcoffset().total_seconds() == -8 * 3600
    assert jan.astimezone(van).utcoffset().total_seconds() == -8 * 3600


def test_as_legislation_timezone(app):
    with app.app_context():
        app.config["LEGISLATIVE_TIMEZONE"] = "America/Vancouver"
        nov = datetime(2026, 11, 15, 6, 59, tzinfo=timezone.utc)
        jan = datetime(2026, 1, 15, 7, 59, tzinfo=timezone.utc)
        assert as_legislation_timezone(nov).strftime("%z") == "-0700"
        assert as_legislation_timezone(jan).strftime("%z") == "-0800"
        assert as_legislation_timezone(nov.replace(tzinfo=None)).strftime("%z") == "-0700"
        assert format_as_report_string(nov) == "November 14, 2026 at 11:59 pm Pacific time"
        assert format_as_report_string(jan) == "January 14, 2026 at 11:59 pm Pacific time"
