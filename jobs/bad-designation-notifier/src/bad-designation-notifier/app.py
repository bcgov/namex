from config import get_named_config
from flask import Flask, current_app
from services.database_service import get_bad_designations
from services.email_service import send_email_notification
from structured_logging import StructuredLogging

def create_app(config_name="default"):
    """Creates and configures the Flask app."""

    app = Flask(__name__) # NOSONAR
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
    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():  # Ensures Flask app context is available
        run_task()
