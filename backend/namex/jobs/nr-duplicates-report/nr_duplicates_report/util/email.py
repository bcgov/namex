import base64
import os
import requests
import traceback
from flask import current_app
from config import Config
from http import HTTPStatus
from util.token import get_bearer_token

def process_attachments(attachments: list[str]) -> list:
    processed_attachments = []
    for order, file_path in enumerate(attachments, start=1):
        try:
            with open(file_path, "rb") as f:
                file_bytes = base64.b64encode(f.read()).decode()
            processed_attachments.append({
                "fileName": os.path.basename(file_path),
                "fileBytes": file_bytes,
                "fileUrl": "",
                "attachOrder": order
            })
        except Exception:
            current_app.logger.error(
                "Failed to process attachment %s. Traceback:\n%s",
                file_path,
                traceback.format_exc()
            )
            raise
    return processed_attachments


def send_email_notification(recipients: list[str], subject: str, body: str, attachments: list[str]):
    """Sends an email notification via the Notify API with file attachments."""
    if not recipients:
        current_app.logger.error("No recipients found in the configuration.")
        raise ValueError("Email recipients are not defined. Please check the configuration.")

    processed_attachments = process_attachments(attachments)
    email_data = {
        "recipients": ",".join(recipients),
        "content": {
            "subject": subject,
            "body": body,
            "attachments": processed_attachments,
        },
    }
    current_app.logger.info(f"Send Email: {email_data}")
    resp = requests.post(
        Config.NOTIFY_API_URL,
        json=email_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_bearer_token()}",
        },
    )

    if resp.status_code == HTTPStatus.OK:
        current_app.logger.info(f"Email with subject '{subject}' sent successfully to: {recipients}")
    else:
        current_app.logger.error(
            f"Failed to send email with subject '{subject}' to {recipients}. "
            f"Response code: {resp.status_code}, Response text: {resp.text}"
        )
