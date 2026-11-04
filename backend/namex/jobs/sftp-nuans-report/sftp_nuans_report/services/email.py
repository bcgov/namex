"""Email service module for sending error notifications via Notify API."""

import re
from datetime import datetime
from http import HTTPStatus

import requests
from flask import current_app

from sftp_nuans_report.config import Config
from sftp_nuans_report.util.token import get_bearer_token


class EmailService:
    """Service responsible for sending email notifications."""

    @staticmethod
    def send_email_to_notify_api(note_book: str, error_message: str) -> None:
        """Send an email notification via the Notify API.

        Builds the email payload and sends it to all configured recipients.
        """
        recipients = EmailService.load_recipients()
        token = get_bearer_token()
        current_app.logger.info('Email recipients list: %s', recipients)

        for recipient in recipients:
            email_data = EmailService.build_email_data(
                note_book,
                error_message,
                recipient,
            )

            current_app.logger.info('Sending email with data: %s', email_data)

            response = requests.post(
                Config.NOTIFY_API_URL,
                json=email_data,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}',
                },
                timeout=10,  # seconds
            )

            if response.status_code == HTTPStatus.OK:
                current_app.logger.info(
                    'Email sent successfully to: %s',
                    recipient,
                )
            else:
                current_app.logger.error(
                    'Failed to send email. Status Code: %s, Response: %s',
                    response.status_code,
                    response.text,
                )

    @staticmethod
    def load_recipients() -> list[str]:
        """Load recipients from environment configuration.

        Expects ERROR_EMAIL_RECIPIENTS to be a comma-separated string.
        Example: foo@example.com,bar@example.com
        """
        recipients_str = Config.ERROR_EMAIL_RECIPIENTS
        return [r.strip() for r in recipients_str.split(',') if r.strip()]

    @staticmethod
    def build_email_data(
        note_book: str,
        error_message: str,
        recipient: str,
    ) -> dict:
        """Build the email payload for the Notify API.

        Sanitizes the error message and formats the subject and body.
        """
        clean_error = error_message.replace("'", '').replace('"', '')
        clean_error = re.sub(r'[^a-zA-Z0-9\s\.,:-]', '', clean_error)
        clean_error = re.sub(r'\s+', ' ', clean_error).strip()

        date_str = datetime.now().strftime('%Y%m%d')

        subject = (
            f'SFTP NUANS Error Notification from LEAR '
            f'for processing {note_book} on {date_str}'
        )

        return {
            'recipients': recipient,
            'content': {
                'subject': subject,
                'body': clean_error,
                'attachments': [],
            },
        }
