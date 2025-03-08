import base64
import os
import logging
import requests
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
            logging.exception(f"Failed to process attachment {file_path}")
            raise
    return processed_attachments


def send_email_notification(recipients: list[str], subject: str, body: str, attachments: list[str]):
    """Sends an email notification via the Notify API with file attachments."""
    if not recipients:
        logging.error("No recipients found in the configuration.")
        raise ValueError("Email recipients are not defined. Please check the configuration.")

    processed_attachments = process_attachments(attachments)
    for recipient in recipients:
        email_data = {
            "recipients": recipient,
            "content": {
                "subject": subject,
                "body": body,
                "attachments": processed_attachments,
            },
        }
        logging.info(f"Send Email: {email_data}")
        resp = requests.post(
            Config.NOTIFY_API_URL,
            json=email_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {get_bearer_token()}",
            },
        )

        if resp.status_code == HTTPStatus.OK:
            logging.info(f"Email with subject '{subject}' sent successfully to: {recipient}")
        else:
            logging.error(
                f"Failed to send email with subject '{subject}' to {recipient}. "
                f"Response code: {resp.status_code}, Response text: {resp.text}"
            )
