from email.mime.text import MIMEText
from flask import current_app
from .utils import get_yesterday_str
import smtplib

def load_recipients():
    """Load recipients dynamically from an environment variable."""
    recipients = current_app.config["EMAIL_RECIPIENTS"]
    return recipients if isinstance(recipients, list) else []

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

    msg = MIMEText(body)
    smtp_user = current_app.config["SMTP_USER"]
    smtp_server = current_app.config["SMTP_SERVER"]
    msg["Subject"] = "Bad characters in names"
    msg["From"] = smtp_user
    msg["To"] = ", ".join(recipients)

    # Send email
    try:
        with smtplib.SMTP(smtp_server) as server:
            server.starttls()
            server.sendmail(smtp_user, recipients, msg.as_string())
        current_app.logger.info("Email sent successfully to: %s", ", ".join(recipients))
    except Exception as e:
        current_app.logger.error("Failed to send email: %s", e)
        raise

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
