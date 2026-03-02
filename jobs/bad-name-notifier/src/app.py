"""Application factory and configuration setup for the Bad Name Notifier service."""

from flask import Flask, current_app
from structured_logging import StructuredLogging

from config import get_named_config
from services.database_service import get_bad_names
from services.email_service import send_email_notification


def create_app(config_name="default"):
    """Creates and configures the Flask app."""

    flask_app = Flask(__name__)  # NOSONAR
    flask_app.config.from_object(get_named_config(config_name))

    # Configure Structured Logging
    structured_logger = StructuredLogging()
    structured_logger.init_app(flask_app)
    flask_app.logger = structured_logger.get_logger()

    return flask_app


def run_task():
    """Executes the task to query bad names and send an email."""
    try:
        # Step 1: Query data
        bad_names = get_bad_names()

        # Step 2: Send email
        send_email_notification(bad_names)
        current_app.logger.info("Notification sent successfully.")
    except Exception as e:  # pylint: disable=broad-exception-caught
        current_app.logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():  # Ensures Flask app context is available
        run_task()
