import requests
import re
from datetime import datetime
from http import HTTPStatus
from flask import current_app
from config import Config
from util.token import get_bearer_token

class EmailService:
    @staticmethod
    def send_email_to_notify_api(note_book: str, error_message: str):
        """Send the email via the Notify API."""
        recipients = EmailService.load_recipients()
        token = get_bearer_token()
        current_app.logger.info("Email recipients list: %s", recipients)

        for recipient in recipients:
            email_data = EmailService.build_email_data(note_book, error_message, recipient)
            current_app.logger.info("Sending email with data: %s", email_data)
            response = requests.post(
                Config.NOTIFY_API_URL,
                json=email_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                }
            )
            if response.status_code == HTTPStatus.OK:
                current_app.logger.info("Email sent successfully to: %s", recipient)
            else:
                current_app.logger.error(
                    "Failed to send email. Status Code: %s, Response: %s",
                    response.status_code,
                    response.text
                )

    @staticmethod
    def load_recipients() -> list[str]:
        """
        Assumes ERROR_EMAIL_RECIPIENTS is defined in .env as a comma-separated list.
        E.g.: foo@example.com,@bar@example.com
        """
        recipients_str = Config.ERROR_EMAIL_RECIPIENTS
        recipients = [r.strip() for r in recipients_str.split(",") if r.strip()]
        return recipients

    @staticmethod
    def build_email_data(note_book: str, error_message: str, recipient: str) -> dict:
        # Sanitize the error for Notify API
        clean_error = error_message.replace("'", "").replace('"', "")
        clean_error = re.sub(r'[^a-zA-Z0-9\s\.,:-]', '', clean_error)
        clean_error = re.sub(r'\s+', ' ', clean_error).strip()

        date_str = datetime.now().strftime('%Y%m%d')
        subject = f"SFTP NUANS Error Notification from LEAR for processing '{note_book}' on {date_str}"

        email_data = {
            "recipients": recipient,
            "content": {
                "subject": subject,
                "body": clean_error,
                "attachments": [],
            },
        }
        return email_data
