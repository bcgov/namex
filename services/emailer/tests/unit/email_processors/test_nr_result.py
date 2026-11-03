from http import HTTPStatus
from types import SimpleNamespace

import pytest

from namex_emailer.constants.notification_options import Option
from namex_emailer.email_processors import nr_result


@pytest.fixture
def email_info():
    return SimpleNamespace(data={"request": {"nrNum": "NR 1234567"}})


@pytest.fixture
def nr_model():
    return {
        "nrNum": "NR 1234567",
        "applicants": [
            {
                "emailAddress": "applicant@example.com",
                "phoneNumber": "2501234567",
            }
        ],
        "expirationDate": "2027-01-01T12:00:00",
        "entity_type_cd": "BC",
        "request_action_cd": "NEW",
        "corpNum": "BC1234567",
        "stateCd": Option.APPROVED.value,
        "consentFlag": "N",
    }


@pytest.fixture
def setup_emailer(app, mocker):
    """Configure Flask and mock shared email dependencies."""

    config_values = [
        "NAMES_INFORMATION_URL",
        "NAME_REQUEST_URL",
        "BUSINESS_URL",
        "DECIDE_BUSINESS_URL",
        "REGISTRY_ACCOUNT_CREATE_URL",
        "COLIN_URL",
        "CORP_FORMS_URL",
        "SOCIETIES_URL",
        "STEPS_TO_RESTORE_URL",
    ]

    with app.app_context():
        for key in config_values:
            app.config[key] = f"https://example.com/{key.lower()}"

        mocker.patch(
            "namex_emailer.email_processors.nr_result.get_magic_link",
            return_value="https://example.com/magic",
        )

        yield


def mock_nr_response(mocker, nr_model, status_code=HTTPStatus.OK):
    response = mocker.Mock()
    response.status_code = status_code
    response.json.return_value = nr_model

    mocker.patch(
        "namex_emailer.email_processors.nr_result.query_nr_number",
        return_value=response,
    )

    return response


class TestEmailConsentLetter:

    def test_success_single_applicant(
        self, app, mocker, email_info, nr_model, setup_emailer
    ):
        nr_model["applicants"] = {
            "emailAddress": "applicant@example.com",
            "phoneNumber": "2501234567",
        }

        mock_nr_response(mocker, nr_model)

        mocker.patch.object(
            nr_result.ReportResource,
            "_update_entity_and_action_code",
        )
        mocker.patch.object(
            nr_result.ReportResource,
            "_get_instruction_group",
            return_value="corporation",
        )
        mocker.patch.object(
            nr_result.ReportResource,
            "_add_expiry_date",
        )
        mocker.patch.object(
            nr_result,
            "get_main_template",
            return_value="NR {{NAMEREQUEST_NUMBER}}",
        )

        with app.app_context():
            result = nr_result.email_consent_letter(email_info)

        assert result["recipients"] == "applicant@example.com"
        assert result["content"]["subject"] == (
            "NR 1234567 - Consent Received by Corporate Registry"
        )
        assert result["content"]["body"] == "NR NR 1234567"
        assert result["content"]["attachments"] == []
        assert nr_model["consentFlag"] == "R"

    def test_success_multiple_applicants(
        self, app, mocker, email_info, nr_model, setup_emailer
    ):
        nr_model["applicants"] = [
            {
                "emailAddress": "first@example.com",
                "phoneNumber": "111",
            },
            {
                "emailAddress": "second@example.com",
                "phoneNumber": "222",
            },
        ]

        mock_nr_response(mocker, nr_model)

        mocker.patch.object(
            nr_result.ReportResource,
            "_update_entity_and_action_code",
        )
        mocker.patch.object(
            nr_result.ReportResource,
            "_get_instruction_group",
            return_value=None,
        )
        mocker.patch.object(
            nr_result.ReportResource,
            "_add_expiry_date",
        )
        mocker.patch.object(
            nr_result,
            "get_main_template",
            return_value="Consent {{NAMEREQUEST_NUMBER}}",
        )

        with app.app_context():
            result = nr_result.email_consent_letter(email_info)

        assert result["recipients"] == (
            "first@example.com,second@example.com"
        )
        assert result["content"]["attachments"] == []

    def test_nr_api_failure(
        self, mocker, email_info, nr_model
    ):
        mock_nr_response(
            mocker,
            nr_model,
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )

        result = nr_result.email_consent_letter(email_info)

        assert result == {}

    def test_missing_expiration_date(
        self, app, mocker, email_info, nr_model, setup_emailer
    ):
        nr_model["expirationDate"] = None

        mock_nr_response(mocker, nr_model)

        mocker.patch.object(
            nr_result.ReportResource,
            "_update_entity_and_action_code",
        )

        add_expiry = mocker.patch.object(
            nr_result.ReportResource,
            "_add_expiry_date",
            side_effect=lambda model: model.update(
                {"expirationDate": "2027-01-01T12:00:00"}
            ),
        )

        mocker.patch.object(
            nr_result.ReportResource,
            "_get_instruction_group",
            return_value=None,
        )
        mocker.patch.object(
            nr_result,
            "get_main_template",
            return_value="Consent",
        )

        with app.app_context():
            result = nr_result.email_consent_letter(email_info)

        add_expiry.assert_called_once_with(nr_model)
        assert result["recipients"] == "applicant@example.com"

    def test_exception(self, mocker, email_info):
        mocker.patch(
            "namex_emailer.email_processors.nr_result.query_nr_number",
            side_effect=Exception("API error"),
        )

        result = nr_result.email_consent_letter(email_info)

        assert result["error"] == "Error retrieving the report."
        assert result["details"] == "API error"


class TestEmailReport:

    @pytest.fixture
    def report_mocks(self, mocker, nr_model):
        mock_nr_response(mocker, nr_model)

        mocker.patch.object(
            nr_result.ReportResource,
            "_get_report",
            return_value=(b"PDF report content", HTTPStatus.OK),
        )

        mocker.patch.object(
            nr_result.ReportResource,
            "_get_instruction_group",
            return_value=None,
        )

        mocker.patch.object(
            nr_result,
            "get_contact_info",
            return_value=(["applicant@example.com"], []),
        )

        template = mocker.patch.object(
            nr_result,
            "get_main_template",
            return_value="Name Request {{NAMEREQUEST_NUMBER}}",
        )

        return template

    def test_approved_email(
        self, app, mocker, email_info, nr_model,
        setup_emailer, report_mocks
    ):
        nr_model["stateCd"] = Option.APPROVED.value
        nr_model["consentFlag"] = "N"

        with app.app_context():
            result = nr_result.email_report(email_info)

        assert result["recipients"] == "applicant@example.com"
        assert result["content"]["subject"] == (
            "NR 1234567 - Name Request Results from Corporate Registry"
        )
        assert len(result["content"]["attachments"]) == 1

        attachment = result["content"]["attachments"][0]

        assert attachment["fileName"] == (
            "NR_1234567_Name_Request_Results_from_Corporate_Registry.pdf"
        )
        assert attachment["fileBytes"] == "UERGIHJlcG9ydCBjb250ZW50"
        assert attachment["attachOrder"] == "1"

        report_mocks.assert_any_call(
            "NEW", "approved.md", "approved"
        )

    def test_conditional_email(
        self, app, mocker, email_info, nr_model,
        setup_emailer, report_mocks
    ):
        nr_model["stateCd"] = Option.CONDITIONAL.value
        nr_model["consentFlag"] = "Y"

        with app.app_context():
            result = nr_result.email_report(email_info)

        assert result["recipients"] == "applicant@example.com"

        report_mocks.assert_any_call(
            "NEW", "conditional.md", "conditional"
        )

    def test_conditional_email_consent_received(
        self, app, mocker, email_info, nr_model,
        setup_emailer, report_mocks
    ):
        nr_model["stateCd"] = Option.APPROVED.value
        nr_model["consentFlag"] = "R"

        with app.app_context():
            result = nr_result.email_report(email_info)

        assert result["content"]["attachments"][0]["fileBytes"] == (
            "UERGIHJlcG9ydCBjb250ZW50"
        )

        report_mocks.assert_any_call(
            "NEW", "conditional.md", "conditional"
        )

    def test_approved_email_with_instruction_group(
        self, app, mocker, email_info, nr_model,
        setup_emailer, report_mocks
    ):
        nr_model["stateCd"] = Option.APPROVED.value

        mocker.patch.object(
            nr_result.ReportResource,
            "_get_instruction_group",
            return_value="corporation",
        )

        with app.app_context():
            nr_result.email_report(email_info)

        report_mocks.assert_any_call(
            "NEW", "approved-corporation.md", "approved"
        )

    def test_rejected_email(
        self, app, mocker, email_info, nr_model,
        setup_emailer, report_mocks
    ):
        nr_model["stateCd"] = Option.REJECTED.value

        with app.app_context():
            nr_result.email_report(email_info)

        report_mocks.assert_any_call("NEW", "rejected.md")

    def test_nr_api_failure(self, mocker, email_info, nr_model):
        mock_nr_response(
            mocker,
            nr_model,
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )

        result = nr_result.email_report(email_info)

        assert result == {}

    def test_report_api_failure(
        self, mocker, email_info, nr_model
    ):
        mock_nr_response(mocker, nr_model)

        mocker.patch.object(
            nr_result.ReportResource,
            "_get_report",
            return_value=("Report unavailable", HTTPStatus.NOT_FOUND),
        )

        result = nr_result.email_report(email_info)

        assert result == {
            "error": "Report unavailable",
            "status_code": HTTPStatus.NOT_FOUND,
        }

    def test_exception(self, mocker, email_info):
        mocker.patch(
            "namex_emailer.email_processors.nr_result.query_nr_number",
            side_effect=Exception("API error"),
        )

        result = nr_result.email_report(email_info)

        assert result["error"] == "Error retrieving the report."
        assert result["details"] == "API error"


class TestBuildEmailBody:

    def test_template_variables(
        self, app, mocker, nr_model, setup_emailer
    ):
        mocker.patch(
            "namex_emailer.email_processors.nr_result.get_magic_link",
            return_value="https://example.com/magic",
        )

        template = (
            "{{NAMEREQUEST_NUMBER}} "
            "{{NAMES_INFORMATION_URL}} "
            "{{NAME_REQUEST_URL}} "
            "{{BUSINESS_URL}} "
            "{{DECIDE_BUSINESS_URL}} "
            "{{REGISTRY_ACCOUNT_CREATE_URL}} "
            "{{CORP_ONLINE_URL}} "
            "{{CORP_FORMS_URL}} "
            "{{SOCIETIES_URL}} "
            "{{STEPS_TO_RESTORE_URL}} "
            "{{MAGIC_LINK}}"
        )

        with app.app_context():
            result = nr_result._build_email_body(template, nr_model)

        assert "{{NAMEREQUEST_NUMBER}}" not in result
        assert "{{NAMES_INFORMATION_URL}}" not in result
        assert "{{NAME_REQUEST_URL}}" not in result
        assert "{{BUSINESS_URL}}" not in result
        assert "{{DECIDE_BUSINESS_URL}}" not in result
        assert "{{REGISTRY_ACCOUNT_CREATE_URL}}" not in result
        assert "{{CORP_ONLINE_URL}}" not in result
        assert "{{CORP_FORMS_URL}}" not in result
        assert "{{SOCIETIES_URL}}" not in result
        assert "{{STEPS_TO_RESTORE_URL}}" not in result
        assert "{{MAGIC_LINK}}" not in result

    def test_no_expiration_date(
        self, app, mocker, nr_model, setup_emailer
    ):
        nr_model["expirationDate"] = None

        mocker.patch(
            "namex_emailer.email_processors.nr_result.get_magic_link",
            return_value="magic-link",
        )

        with app.app_context():
            result = nr_result._build_email_body(
                "NR {{NAMEREQUEST_NUMBER}} {{EXPIRATION_DATE}}",
                nr_model,
            )

        assert result == "NR NR 1234567 "

    def test_expiration_date(
        self, app, mocker, nr_model, setup_emailer
    ):
        mocker.patch(
            "namex_emailer.email_processors.nr_result.as_legislation_timezone",
            return_value="Pacific date",
        )

        mocker.patch(
            "namex_emailer.email_processors.nr_result.format_as_report_string",
            return_value="January 1, 2027 at 12:00 PM Pacific time",
        )

        mocker.patch(
            "namex_emailer.email_processors.nr_result.get_magic_link",
            return_value="magic-link",
        )

        with app.app_context():
            result = nr_result._build_email_body(
                "{{EXPIRATION_DATE}}",
                nr_model,
            )

        assert result == "January 1, 2027 at 12:00 PM Pacific time"

    def test_datetime_template_variable(
        self, app, mocker, nr_model, setup_emailer
    ):
        from datetime import datetime

        mocker.patch(
            "namex_emailer.email_processors.nr_result.as_legislation_timezone",
            return_value=datetime(2027, 1, 1, 12, 0),
        )

        mocker.patch(
            "namex_emailer.email_processors.nr_result.format_as_report_string",
            return_value="formatted date",
        )

        mocker.patch(
            "namex_emailer.email_processors.nr_result.get_magic_link",
            return_value="magic-link",
        )

        with app.app_context():
            result = nr_result._build_email_body(
                "{{EXPIRATION_DATE}}",
                nr_model,
            )

        assert result == "formatted date"
