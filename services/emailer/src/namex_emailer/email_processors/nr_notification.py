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
"""Email processing rules and actions for Name Request before expiry, expiry, renewal, upgrade."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from http import HTTPStatus
from pathlib import Path

from flask import current_app, request
from gcp_queue.logging import structured_log
from jinja2 import Template
from simple_cloudevent import SimpleCloudEvent

from namex.constants import RequestAction
from namex.resources.name_requests import ReportResource
from namex_emailer.email_processors import substitute_template_parts
from namex_emailer.services.helpers import as_legislation_timezone, format_as_report_string, get_magic_link, query_nr_number, get_instruction_group

class Option(Enum):
    """NR notification option."""

    BEFORE_EXPIRY = "before-expiry"
    EXPIRED = "expired"
    RENEWAL = "renewal"
    UPGRADE = "upgrade"
    REFUND = "refund"
    APPROVED = "APPROVED"
    CONDITIONAL = "CONDITIONAL"
    REJECTED = "REJECTED"
    CONSENT_RECEIVED = "CONSENT_RECEIVED"



def process(email_info: SimpleCloudEvent, option) -> dict:  # pylint: disable-msg=too-many-locals
    """
    Build the email for Name Request notification.

    valid values of option: Option
    """
    structured_log(request, "DEBUG", f"NR {option} notification: {email_info}")
    nr_number = email_info.data['request']['nrNum']

    nr_response = query_nr_number(nr_number)
    if nr_response.status_code != HTTPStatus.OK:
        structured_log(request, "ERROR", f"Failed to get nr info for name request: {nr_number}")
        return {}

    nr_data = nr_response.json()

    expiration_date = ""
    if nr_data["expirationDate"]:
        exp_date = datetime.fromisoformat(nr_data["expirationDate"])
        exp_date_tz = as_legislation_timezone(exp_date)
        expiration_date = format_as_report_string(exp_date_tz)

    refund_value = ""
    if option == Option.REFUND.value:
        refund_value = email_info.data.get("request", {}).get("refundValue", None)

    business_name = ""
    for n_item in nr_data["names"]:
        if n_item["state"] in ("APPROVED", "CONDITION"):
            business_name = n_item["name"]
            break

    name_request_url = current_app.config.get("NAME_REQUEST_URL")
    decide_business_url = current_app.config.get("DECIDE_BUSINESS_URL")
    corp_online_url = current_app.config.get("COLIN_URL")
    form_page_url = current_app.config.get("CORP_FORMS_URL")
    societies_url = current_app.config.get("SOCIETIES_URL")
    magic_link = get_magic_link(nr_number, nr_data["applicants"]["emailAddress"], nr_data["applicants"]["phoneNumber"])

    file_name_suffix = option.upper()
    if option == Option.BEFORE_EXPIRY.value:
        if "entity_type_cd" in nr_data:
            legal_type = nr_data["entity_type_cd"]
            request_action = nr_data["request_action_cd"]
            corpNum = nr_data["corpNum"]
            # This function will be restred after the emailer service and NameX API are sync well.
            # group = ReportResource._get_instruction_group(legal_type, request_action, corpNum)
            group = get_instruction_group(legal_type, request_action, corpNum)
            if group:
                instruction_group = "-" + group
                file_name_suffix += instruction_group.upper()

    template = Path(f'{current_app.config.get("TEMPLATE_PATH")}/NR-{file_name_suffix}.html').read_text()
    filled_template = substitute_template_parts(template)

    # render template with vars
    mail_template = Template(filled_template, autoescape=True)
    html_out = mail_template.render(
        nr_number=nr_number,
        expiration_date=expiration_date,
        legal_name=business_name,
        refund_value=refund_value,
        name_request_url=name_request_url,
        decide_business_url=decide_business_url,
        corp_online_url=corp_online_url,
        form_page_url=form_page_url,
        societies_url=societies_url,
        magic_link=magic_link
    )

    # get recipients
    recipients = nr_data["applicants"]["emailAddress"]
    if not recipients:
        return {}

    subjects = {
        Option.BEFORE_EXPIRY.value: "Expiring Soon",
        Option.EXPIRED.value: "Expired",
        Option.RENEWAL.value: "Confirmation of Renewal",
        Option.UPGRADE.value: "Confirmation of Upgrade",
        Option.REFUND.value: "Refund request confirmation",
    }

    return {
        "recipients": recipients,
        "requestBy": "BCRegistries@gov.bc.ca",
        "content": {
            "subject": f"{nr_number} - {subjects[option]}",
            "body": f"{html_out}",
            "attachments": [],
        },
    }
