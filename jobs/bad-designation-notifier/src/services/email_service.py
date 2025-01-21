import csv
import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import current_app
from .utils import get_yesterday_str

def load_recipients():
    """Load recipients dynamically from an environment variable."""
    recipients = current_app.config["EMAIL_RECIPIENTS"]
    return recipients if isinstance(recipients, list) else []

def send_email_notification(bad_designations):
    """Sends an email notification with the bad names."""
    # Dynamically load recipients
    recipients = load_recipients()
    current_app.logger.info(f'recipients:{recipients}')

    # Check if recipients list is empty
    if not recipients:
        current_app.logger.error("No recipients found in the configuration.")
        raise ValueError("Email recipients are not defined. Please check the configuration.")

    # Define headers
    headers = [
        "NR", "Name", "Last Update", "Request Type", "Entity Type",
        "State", "Expiration Date", "Consumed Corp", "Consumed Date"
    ]

    total_count = len(bad_designations)

    # Add total count at the end
    email_body = f"""
    The attached report contains {total_count} record(s) collected on {get_yesterday_str()}.
    Please find the detailed report in the attached file.
    """ if total_count > 0 else f"""
    No bad designations were found on {get_yesterday_str()}.
    """

    smtp_user = current_app.config["SMTP_USER"]
    smtp_server = current_app.config["SMTP_SERVER"]

    # Compose the email
    msg = MIMEMultipart()
    msg.attach(MIMEText(email_body, "plain"))
    msg["Subject"] = "Bad designation in names"
    msg["From"] = smtp_user
    msg["To"] = ", ".join(recipients)

    csv_file = f"bad-designation-{get_yesterday_str()}.csv"

    # Attach the CSV file if there are records
    if total_count > 0:
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(bad_designations)

        with open(csv_file, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={csv_file}")
            msg.attach(part)

    # Send email
    try:
        with smtplib.SMTP(smtp_server) as server:
            server.starttls()
            server.send_message(msg)
        current_app.logger.info("Email sent successfully to: %s", ", ".join(recipients))
    except Exception as e:
        current_app.logger.error("Failed to send email: %s", e)
        raise
    finally:
        # Cleanup: Delete the CSV file if it exists
        if os.path.exists(csv_file):
            os.remove(csv_file)
            current_app.logger.info("Temporary CSV file deleted: %s", csv_file)