"""Email service module for sending bad designation notifications."""

from http import HTTPStatus

import requests
from flask import current_app

from .utils import column_headers, column_keys, get_bearer_token, get_yesterday_str


def load_recipients():
    """Load recipients dynamically from an environment variable."""
    recipients = current_app.config["EMAIL_RECIPIENTS"]
    return [r.strip("[]") for r in recipients] if isinstance(recipients, list) else []


def send_email(email: dict, token: str):
    """Send the email"""
    current_app.logger.info(f"Send Email: {email}")
    return requests.post(
        f'{current_app.config.get("NOTIFY_API_URL", "")}',
        json=email,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        timeout=30,  # seconds
    )


def send_email_notification(formatted_result):
    """Sends an email notification with the bad names."""
    # Dynamically load recipients
    recipients = load_recipients()
    current_app.logger.info(f"recipients:{recipients}")

    # Check if recipients list is empty
    if not recipients:
        current_app.logger.error("No recipients found in the configuration.")
        raise ValueError(
            "Email recipients are not defined. Please check the configuration."
        )

    # Final email body
    email_body = format_email_body(formatted_result)

    # Send email via Notify API
    token = get_bearer_token()
    email_data = {
        "recipients": ",".join(recipients),
        "content": {
            "subject": "Bad designation in names",
            "body": email_body,
            "attachments": [],
        },
    }
    resp = send_email(email_data, token)
    if resp.status_code == HTTPStatus.OK:
        current_app.logger.info(f"Email sent successfully to: {recipients}")
    else:
        current_app.logger.error(
            f"Failed to send email. Status Code: {resp.status_code}, Response: {resp.text}"
        )


def format_email_body(formatted_result):
    """Formats the email body as a list of key-value lists."""
    if not formatted_result:
        return f"No bad designations were found on {get_yesterday_str()}."

    title = f"FIRMS WITH A CORPORATE DESIGNATION {get_yesterday_str()}"
    records = []
    for record in formatted_result:
        lines = [
            f"**{header}:** {record.get(key, '')}"
            for header, key in zip(column_headers, column_keys)
        ]
        records.append("\n".join(lines))
    footer = f"Total {len(formatted_result)} record(s)"

    return "\n\n".join([title, "\n\n".join(records), footer])
