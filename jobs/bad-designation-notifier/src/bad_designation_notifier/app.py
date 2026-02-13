"""Module for creating and configuring the Flask application."""

from flask import Flask, current_app
from structured_logging import StructuredLogging

from bad_designation_notifier.config import get_named_config
from bad_designation_notifier.services.database_service import \
    get_bad_designations
from bad_designation_notifier.services.email_service import \
    send_email_notification


def create_app(config_name="default"):
    """Creates and configures the Flask app."""

    app = Flask(__name__)  # NOSONAR
    app.config.from_object(get_named_config(config_name))

    # Configure Structured Logging
    structured_logger = StructuredLogging()
    structured_logger.init_app(app)
    app.logger = structured_logger.get_logger()

    return app


def run_task():
    """Executes the task to query bad names and send an email."""
    try:
        # Step 1: Query data
        bad_designations = get_bad_designations()

        # Step 2: Send email
        send_email_notification(bad_designations)
        current_app.logger.info("Notification sent successfully.")
    except Exception:  # pylint: disable=broad-exception-caught
        current_app.logger.exception(
            "An unexpected error occurred while running the task"
        )


if __name__ == "__main__":
    flask_app = create_app()
    with flask_app.app_context():  # Ensures Flask app context is available
        run_task()
