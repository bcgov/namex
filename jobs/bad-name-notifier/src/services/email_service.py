import requests
from http import HTTPStatus
from flask import current_app
from .utils import get_yesterday_str, get_bearer_token

def load_recipients():
    """Load recipients dynamically from an environment variable."""
    recipients = current_app.config["EMAIL_RECIPIENTS"]
    if isinstance(recipients, list):
        return [r.strip('[]') for r in recipients]
    return []

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
    )

def send_email_notification(bad_names):
    """Sends an email notification with the bad names."""
    # Dynamically load recipients
    recipients = load_recipients()
    current_app.logger.info(f'recipients:{recipients}')

    # Check if recipients list is empty
    if not recipients:
        current_app.logger.error("No recipients found in the configuration.")
        raise ValueError("Email recipients are not defined. Please check the configuration.")

    # Create email content
    body = generate_report_title() + "\n\n" + generate_report_body(bad_names)

    # Send email via Notify API
    token = get_bearer_token()
    for recipient in recipients:
        email_data = {
            "recipients": recipient,
            "content": {
                "subject": "Bad characters in names",
                "body": body,
                "attachments": [],
            },
        }

        resp = send_email(email_data, token)
        if resp.status_code == HTTPStatus.OK:
            current_app.logger.info(f"Email sent successfully to: {recipient}")
        else:
            current_app.logger.error(
                f"Failed to send email. Status Code: {resp.status_code}, Response: {resp.text}"
            )

def generate_report_title():
    """Generates an email title with yesterday's date."""
    # Format the date as yyyy-mm-dd
    yesterday = get_yesterday_str()

    # Construct the email title
    email_title = f"BAD CHARACTERS FOR {yesterday}"

    return email_title

def generate_report_body(bad_names):
    """Formats the result into a table with headers and adds a total count at the end."""
    # Table headers
    title = f"{'NR Number':<15}{'Choice':<10}Name"
    separator = "-" * len(title)

    # Format each row
    lines = [
        f"{row['nr_num']:<15}{row['choice']:<10}{row['name']}"
        for row in bad_names
    ]

    # Add total count at the end
    total_count = len(bad_names)
    footer_separator = "-" * len(title)  # Line of dashes before the total
    footer = f"\n{footer_separator}\nTotal bad names: {total_count}"

    # Combine title, separator, rows, and footer into a single formatted string
    return "\n".join([title, separator] + lines) + footer
