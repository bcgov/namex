
from datetime import datetime, timezone
from unittest.mock import Mock

import pytest
import pytz
import requests

from namex_emailer.constants.notification_options import Option
from namex_emailer.services import helpers

@pytest.fixture(autouse=True)
def clear_bearer_token_cache():
    """Prevent cached tokens from leaking between tests."""
    token_function = helpers.get_bearer_token

    if hasattr(token_function, "cache_clear"):
        token_function.cache_clear()
    elif hasattr(token_function, "__func__"):
        token_function.__func__.cache_clear()

    yield

    if hasattr(token_function, "cache_clear"):
        token_function.cache_clear()
    elif hasattr(token_function, "__func__"):
        token_function.__func__.cache_clear()

@pytest.fixture
def nr_data():
    return {
        "nrNum": "NR 1234567",
        "request_action_cd": "NEW",
        "applicants": [
            {
                "emailAddress": "test@example.com",
                "phoneNumber": "2501234567",
            }
        ],
    }


@pytest.fixture
def email():
    return {
        "recipients": "test@example.com",
        "content": {
            "subject": "Test email",
            "body": "Test body",
            "attachments": [],
        },
    }


@pytest.fixture
def cloud_event():
    return Mock(
        data={
            "request": {
                "nrNum": "NR 1234567",
                "option": Option.APPROVED.value,
            }
        }
    )


class TestGetBearerToken:

    def test_success(self, app, mocker):
        mock_response = Mock()
        mock_response.json.return_value = {
            "access_token": "test-token"
        }

        mocker.patch.object(
            helpers.requests,
            "post",
            return_value=mock_response,
        )

        with app.app_context():
            result = helpers.get_bearer_token()

        assert result == "test-token"

    def test_missing_access_token(self, app, mocker):
        mock_response = Mock()
        mock_response.json.return_value = {}

        mocker.patch.object(
            helpers.requests,
            "post",
            return_value=mock_response,
        )

        with app.app_context():
            result = helpers.get_bearer_token()

        assert result is None

    def test_invalid_json(self, app, mocker):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")

        mocker.patch.object(
            helpers.requests,
            "post",
            return_value=mock_response,
        )

        with app.app_context():
            result = helpers.get_bearer_token()

        assert result is None


class TestTimezoneFunctions:

    def test_naive_datetime(self, app):
        value = datetime(2026, 1, 15, 12, 0)

        with app.app_context():
            result = helpers.as_legislation_timezone(value)

        assert result.tzinfo is not None
        assert result.hour == 4

    def test_aware_datetime(self, app):
        value = datetime(
            2026, 1, 15, 12, 0,
            tzinfo=timezone.utc,
        )

        with app.app_context():
            result = helpers.as_legislation_timezone(value)

        assert result.hour == 4

    def test_summer_datetime(self, app):
        value = datetime(
            2026, 7, 15, 12, 0,
            tzinfo=timezone.utc,
        )

        with app.app_context():
            result = helpers.as_legislation_timezone(value)

        assert result.hour == 5

    def test_format_report_string_am(self, app):
        value = datetime(
            2026, 1, 15, 16, 30,
            tzinfo=timezone.utc,
        )

        with app.app_context():
            result = helpers.format_as_report_string(value)

        assert result == (
            "January 15, 2026 at 8:30 am Pacific time"
        )

    def test_format_report_string_pm(self, app):
        value = datetime(
            2026, 1, 15, 23, 45,
            tzinfo=timezone.utc,
        )

        with app.app_context():
            result = helpers.format_as_report_string(value)

        assert result == (
            "January 15, 2026 at 3:45 pm Pacific time"
        )


class TestGetMagicLink:

    @pytest.mark.parametrize(
        "action,route",
        [
            ("NEW", "incorporateNow"),
            ("MVE", "continueInNow"),
            ("AML", "amalgamateNow"),
        ],
    )
    def test_supported_actions(
        self, app, nr_data, action, route
    ):
        nr_data["request_action_cd"] = action
        app.config["BUSINESS_REGISTRY_URL"] = (
            "https://business.example.com/"
        )

        with app.app_context():
            result = helpers.get_magic_link(nr_data)

        assert result.startswith(
            f"https://business.example.com/{route}/?"
        )
        assert "nr=NR+1234567" in result
        assert "email=test%40example.com" in result
        assert "phone=2501234567" in result

    def test_unknown_action(self, app, nr_data):
        nr_data["request_action_cd"] = "UNKNOWN"
        app.config["BUSINESS_REGISTRY_URL"] = (
            "https://business.example.com/"
        )

        with app.app_context():
            result = helpers.get_magic_link(nr_data)

        assert result.startswith(
            "https://business.example.com/None/?"
        )


class TestGetContactInfo:

    def test_single_applicant(self):
        data = {
            "applicants": {
                "emailAddress": "one@example.com",
                "phoneNumber": "111",
            }
        }

        emails, phones = helpers.get_contact_info(data)

        assert emails == ["one@example.com"]
        assert phones == ["111"]

    def test_multiple_applicants(self):
        data = {
            "applicants": [
                {
                    "emailAddress": "one@example.com",
                    "phoneNumber": "111",
                },
                {
                    "emailAddress": "two@example.com",
                    "phoneNumber": "222",
                },
            ]
        }

        emails, phones = helpers.get_contact_info(data)

        assert emails == [
            "one@example.com",
            "two@example.com",
        ]
        assert phones == ["111", "222"]

    def test_missing_contact_information(self):
        data = {
            "applicants": [
                {
                    "emailAddress": "",
                    "phoneNumber": None,
                },
                {
                    "emailAddress": "two@example.com",
                    "phoneNumber": "",
                },
            ]
        }

        emails, phones = helpers.get_contact_info(data)

        assert emails == ["two@example.com"]
        assert phones == []

    def test_missing_applicants(self):
        emails, phones = helpers.get_contact_info({})

        assert emails == []
        assert phones == []


class TestApiHelpers:

    def test_get_headers(self):
        result = helpers.get_headers("abc123")

        assert result == {
            "Content-Type": "application/json",
            "Authorization": "Bearer abc123",
        }

    def test_query_nr_number(self, app, mocker):
        app.config["NAMEX_SVC_URL"] = "https://namex.example.com"

        mocker.patch.object(
            helpers,
            "get_bearer_token",
            return_value="token",
        )

        mock_get = mocker.patch.object(
            helpers.requests,
            "get",
            return_value="response",
        )

        with app.app_context():
            result = helpers.query_nr_number("NR 1234567")

        assert result == "response"

        mock_get.assert_called_once_with(
            "https://namex.example.com/requests/NR 1234567",
            headers=helpers.get_headers("token"),
        )

    def test_query_notification_event(self, app, mocker):
        app.config["NAMEX_SVC_URL"] = "https://namex.example.com"

        mocker.patch.object(
            helpers,
            "get_bearer_token",
            return_value="token",
        )

        mock_get = mocker.patch.object(
            helpers.requests,
            "get",
            return_value="response",
        )

        with app.app_context():
            result = helpers.query_notification_event("event123")

        assert result == "response"

        mock_get.assert_called_once_with(
            "https://namex.example.com/events/event/event123",
            headers=helpers.get_headers("token"),
        )

    def test_send_email(self, app, mocker, email):
        app.config["NOTIFY_API_URL"] = (
            "https://notify.example.com"
        )

        mock_post = mocker.patch.object(
            helpers.requests,
            "post",
            return_value="response",
        )

        with app.test_request_context("/"):
            result = helpers.send_email(email, "token")

        assert result == "response"
        mock_post.assert_called_once_with(
            "https://notify.example.com",
            json=email,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer token",
            },
        )


class TestUpdateResendTimestamp:

    def test_success(self, app, mocker):
        app.config["NAMEX_SVC_URL"] = (
            "https://namex.example.com"
        )

        mocker.patch.object(
            helpers,
            "get_bearer_token",
            return_value="token",
        )

        response = Mock()
        response.raise_for_status.return_value = None

        mocker.patch.object(
            helpers.requests,
            "patch",
            return_value=response,
        )

        with app.app_context():
            result = helpers.update_resend_timestamp("event123")

        assert result is True

    def test_request_exception(self, app, mocker):
        app.config["NAMEX_SVC_URL"] = (
            "https://namex.example.com"
        )

        mocker.patch.object(
            helpers,
            "get_bearer_token",
            return_value="token",
        )

        mocker.patch.object(
            helpers.requests,
            "patch",
            side_effect=requests.exceptions.RequestException(
                "Connection error"
            ),
        )

        with app.app_context():
            result = helpers.update_resend_timestamp("event123")

        assert result is False


class TestExtractEventData:

    def test_valid_event(self, cloud_event):
        nr_num, option = helpers._extract_event_data(
            cloud_event
        )

        assert nr_num == "NR 1234567"
        assert option == Option.APPROVED.value

    def test_missing_nr_number(self, cloud_event):
        cloud_event.data["request"]["nrNum"] = None

        result = helpers._extract_event_data(cloud_event)

        assert result == (None, None)

    def test_invalid_option(self, cloud_event):
        cloud_event.data["request"]["option"] = "INVALID"

        result = helpers._extract_event_data(cloud_event)

        assert result == (None, None)

    def test_missing_option(self, cloud_event):
        del cloud_event.data["request"]["option"]

        result = helpers._extract_event_data(cloud_event)

        assert result == (None, None)


class TestPrepareEventJson:

    def test_regular_notification(self, email):
        result = helpers._prepare_event_json(
            "NR 1234567",
            Option.RENEWAL.value,
            email,
        )

        assert result["option"] == Option.RENEWAL.value
        assert result["email"] is email

    def test_decision_event(self, app, mocker, email):
        email["content"]["attachments"] = [
            {
                "fileName": "report.pdf",
                "fileBytes": "original-bytes",
            }
        ]

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "nrNum": "NR 1234567"
        }

        mocker.patch.object(
            helpers,
            "query_nr_number",
            return_value=mock_response,
        )

        with app.app_context():
            result = helpers._prepare_event_json(
                "NR 1234567",
                Option.APPROVED.value,
                email,
            )

        assert result["nr_model"]["nrNum"] == "NR 1234567"
        assert result["email"]["content"]["attachments"][0][
            "fileBytes"
        ] == "<placeholder-for-pdf-report-bytes>"

        # Original email must not be modified.
        assert email["content"]["attachments"][0][
            "fileBytes"
        ] == "original-bytes"

    def test_decision_event_api_failure(
        self, app, mocker, email
    ):
        mock_response = Mock()
        mock_response.status_code = 500

        mocker.patch.object(
            helpers,
            "query_nr_number",
            return_value=mock_response,
        )

        with app.app_context():
            result = helpers._prepare_event_json(
                "NR 1234567",
                Option.APPROVED.value,
                email,
            )

        assert result is None

    def test_decision_event_exception(
        self, app, mocker, email
    ):
        mocker.patch.object(
            helpers,
            "query_nr_number",
            side_effect=Exception("API error"),
        )

        with app.app_context():
            result = helpers._prepare_event_json(
                "NR 1234567",
                Option.APPROVED.value,
                email,
            )

        assert result is None


class TestRecordEvent:

    def test_success(self, app, mocker):
        app.config["NAMEX_SVC_URL"] = (
            "https://namex.example.com"
        )

        mocker.patch.object(
            helpers,
            "get_bearer_token",
            return_value="token",
        )

        response = Mock()
        response.raise_for_status.return_value = None

        mock_post = mocker.patch.object(
            helpers.requests,
            "post",
            return_value=response,
        )

        event_json = {"option": "RENEWAL"}

        with app.app_context():
            result = helpers._record_event(
                "NR 1234567",
                event_json,
            )

        assert result is True

        payload = mock_post.call_args.kwargs["json"]

        assert payload == {
            "action": "notification",
            "eventJson": event_json,
        }

    def test_request_exception(self, app, mocker):
        app.config["NAMEX_SVC_URL"] = (
            "https://namex.example.com"
        )

        mocker.patch.object(
            helpers,
            "get_bearer_token",
            return_value="token",
        )

        mocker.patch.object(
            helpers.requests,
            "post",
            side_effect=requests.exceptions.RequestException(
                "Connection error"
            ),
        )

        with app.app_context():
            result = helpers._record_event(
                "NR 1234567",
                {"option": "RENEWAL"},
            )

        assert result is False


class TestWriteToEvents:

    def test_event_with_header_nr_number(
        self, app, mocker, email
    ):
        event = Mock(
            data={
                "request": {
                    "header": {
                        "nrNum": "NR 1234567"
                    }
                }
            }
        )

        record = mocker.patch.object(
            helpers,
            "_record_event",
            return_value=True,
        )

        prepare = mocker.patch.object(
            helpers,
            "_prepare_event_json",
            return_value={"email": email},
        )

        with app.app_context():
            result = helpers.write_to_events(event, email)

        assert result is True

        prepare.assert_called_once_with(
            "NR 1234567",
            None,
            email,
        )

        record.assert_called_once()

    def test_event_without_header_nr_number(
        self, app, mocker, email
    ):
        event = Mock(
            data={
                "request": {
                    "nrNum": "NR 1234567",
                    "option": Option.RENEWAL.value,
                }
            }
        )

        record = mocker.patch.object(
            helpers,
            "_record_event",
            return_value=True,
        )

        mocker.patch.object(
            helpers,
            "_prepare_event_json",
            return_value={"option": Option.RENEWAL.value},
        )

        with app.app_context():
            result = helpers.write_to_events(event, email)

        assert result is True
        record.assert_called_once()

    def test_invalid_event(self, app, mocker, email):
        event = Mock(data={"request": {}})

        record = mocker.patch.object(
            helpers,
            "_record_event",
        )

        with app.app_context():
            result = helpers.write_to_events(event, email)

        assert result is None
        record.assert_not_called()
