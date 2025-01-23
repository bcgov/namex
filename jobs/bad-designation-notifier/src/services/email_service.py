import base64
import csv
from http import HTTPStatus
from io import StringIO
import requests
from flask import current_app
from .utils import get_bearer_token, get_yesterday_str

def load_recipients():
    """Load recipients dynamically from an environment variable."""
    recipients = current_app.config["EMAIL_RECIPIENTS"]
    return recipients if isinstance(recipients, list) else []

def build_csv_attachment(total_count, bad_designations):
    """Builds the CSV attachment if there are bad designations."""
    if total_count > 0:
        csv_file_name = f"bad-designation-{get_yesterday_str()}.csv"
        headers = [
            "NR",
            "Name",
            "Last Update",
            "Request Type",
            "Entity Type",
            "State",
            "Expiration Date",
            "Consumed Corp",
            "Consumed Date",
        ]
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(bad_designations)
        csv_content = base64.b64encode(output.getvalue().encode()).decode()
        return [
            {
                "fileName": csv_file_name,
                "fileBytes": csv_content,
                "fileUrl": "",
                "attachOrder": "1",
            }
        ]
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


def send_email_notification(bad_designations):
    """Sends an email notification with the bad names."""
    # Dynamically load recipients
    recipients = load_recipients()
    current_app.logger.info(f"recipients:{recipients}")

    # Check if recipients list is empty
    if not recipients:
        current_app.logger.error("No recipients found in the configuration.")
        raise ValueError("Email recipients are not defined. Please check the configuration.")

    # Build the csv attatchment
    total_count = len(bad_designations)
    attachment = build_csv_attachment(total_count, bad_designations)

    # Add total count at the end
    email_body = f"""
    The attached report contains {total_count} record(s) collected on {get_yesterday_str()}.
    Please find the detailed report in the attached file.
    """ if total_count > 0 else f"""
    No bad designations were found on {get_yesterday_str()}.
    """

    # Send email via Notify API
    token = get_bearer_token()
    for recipient in recipients:
        email_data = {
            "recipients": recipient,
            "content": {
                "subject": "Bad designation in names",
                "body": email_body,
                "attachments": attachment,
            },
        }

        resp = send_email(email_data, token)
        if resp.status_code == HTTPStatus.OK:
            current_app.logger.info(f"Email sent successfully to: {recipient}")
        else:
            current_app.logger.error(
                f"Failed to send email. Status Code: {resp.status_code}, Response: {resp.text}"
            )
