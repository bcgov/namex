import csv
import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from flask import current_app
from .utils import get_yesterday_str, column_keys, column_headers

def load_recipients():
    """Load recipients dynamically from an environment variable."""
    recipients = current_app.config["EMAIL_RECIPIENTS"]
    return recipients if isinstance(recipients, list) else []

def send_email_notification(formatted_result):
    """Sends an email notification with the bad names."""
    # Dynamically load recipients
    recipients = load_recipients()
    current_app.logger.info(f'recipients:{recipients}')

    # Check if recipients list is empty
    if not recipients:
        current_app.logger.error("No recipients found in the configuration.")
        raise ValueError("Email recipients are not defined. Please check the configuration.")

    # Final email body
    email_body = format_email_body (formatted_result)

    smtp_user = current_app.config["SMTP_USER"]
    smtp_server = current_app.config["SMTP_SERVER"]

    # Compose the email
    msg = MIMEMultipart()
    msg.attach(MIMEText(email_body, "html"))
    msg["Subject"] = "Bad designation in names"
    msg["From"] = smtp_user
    msg["To"] = ", ".join(recipients)

    # Send email
    try:
        with smtplib.SMTP(smtp_server) as server:
            server.starttls()
            server.send_message(msg)
        current_app.logger.info("Email sent successfully to: %s", ", ".join(recipients))
    except Exception as e:
        current_app.logger.error("Failed to send email: %s", e)
        raise

def format_email_body(formatted_result):
    """Formats the email body as an HTML table."""
    if not formatted_result:
        return f"<p>No bad designations were found on {get_yesterday_str()}.</p>"

    # Generate table header
    table_header = "".join(f"<th>{header}</th>" for header in column_headers)

    # Generate table rows
    table_rows = "".join(
        f"<tr>{''.join(f'<td>{row[key]}</td>' for key in column_keys)}</tr>"
        for row in formatted_result
    )

    # Construct the final HTML email body
    email_body = f"""
    <html>
        <body>
            <p><b>FIRMS WITH A CORPORATE DESIGNATION {get_yesterday_str()}</b></p>
            <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; font-family: 'Arial', sans-serif; font-size: 14px; width: 100%;">
                <thead>
                    <tr style="background-color: #f2f2f2;">{table_header}</tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </body>
        <p>Total {len(formatted_result)} record(s)</p>
    </html>
    """ if len(formatted_result) > 0 else f"""
    No bad designations were found on {get_yesterday_str()}.
    """
    
    return email_body