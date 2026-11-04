import base64
from http import HTTPStatus

from flask import json
from namex.resources.name_requests import ReportResource
from structured_logging import StructuredLogging

from namex_emailer.constants.notification_options import DECISION_OPTIONS, Option
from namex_emailer.services.helpers import (
    get_bearer_token,
    query_notification_event,
    send_email,
    update_resend_timestamp,
)

logger = StructuredLogging.get_logger()

def process_resend_email(event_id: str):
    """
    Process the resend email request.
    This function is called when a resend event is triggered.
    """
    logger.info(f"[Resend Email] Event ID: {event_id}")

    # Validate the event ID
    if not event_id:
        logger.error("Invalid event ID provided for resend operation.")
    else:
        # Call the resend_email function to handle the actual email sending
        _resend_email(event_id)
    return {}, HTTPStatus.OK


def _resend_email(event_id: str):
    # Query the event record
    response = query_notification_event(event_id)
    if not response:
        logger.error("No event found.")
        return

    event = response.json()
    event_json_str = event.get("jsonData")
    if not event_json_str:
        logger.error(f"No email content in the event: {event_id}")
        return

    # Parse the event JSON
    event_json = _parse_json(event_json_str)
    if not event_json:
        logger.error(f"Failed to parse jsonData for the event: {event_id}")
        return

    email = event_json.get("email")
    option = event_json.get("option")
    nr_model = event_json.get("nr_model")
    if not email or not option:
        logger.error(f"Invalid email content in the event: {event_id}")
        return

    # Handle decision options and generate report if needed
    if option and Option(option) in DECISION_OPTIONS and nr_model:
        if not _handle_attachments(email, nr_model):
            logger.error(f"Failed to handle attachments for the event: {event_id}")
            return

    # Send the email
    if _send_email(email):
        update_resend_timestamp(event_id)
        logger.debug(f"Successfully resent email for the event {event_id}")


def _parse_json(json_str: str):
    """Parse a JSON string and handle errors."""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse jsonData for the event: {e}")
        return None


def _handle_attachments(email: dict, nr_model: dict) -> bool:
    """Generate a report and update the email attachments."""
    report, status_code = ReportResource._get_report(nr_model)
    if status_code != HTTPStatus.OK:
        logger.error(f"Failed to generate report for the event: {report}")
        return False

    attachments = email.get("content", {}).get("attachments", [])
    encoded_report = base64.b64encode(report).decode()

    if attachments:
        # Update the first attachment's fileBytes
        attachments[0]["fileBytes"] = encoded_report
    else:
        # Create a new attachment if none exist
        report_name = email.get("content", {}).get("subject", "Report")
        attachments.append(
            {
                "fileName": report_name.replace(" - ", " ").replace(" ", "_") + ".pdf",
                "fileBytes": encoded_report,
                "fileUrl": "",
                "attachOrder": "1",
            }
        )
        email["content"]["attachments"] = attachments

    return True


def _send_email(email: dict):
    """Send the email and handle errors."""
    token = get_bearer_token()
    resp = send_email(email, token)

    if resp.status_code != HTTPStatus.OK:
        logger.error(f"Failed to resend email for the event: {resp.status_code} - {resp.text}")
        return False
    return True
