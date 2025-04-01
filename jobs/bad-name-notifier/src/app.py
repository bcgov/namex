from config import APP_CONFIG
from flask import Flask, current_app
from services.database_service import get_bad_names
from services.email_service import send_email_notification

import logging
import logging.config
import os

def create_app(config_name="default"):
    """Creates and configures the Flask app."""

    app = Flask(__name__) # NOSONAR
    app.config.from_object(APP_CONFIG[config_name])
    print(app.config)
    return app

def run_task():
    """Executes the task to query bad names and send an email."""
    try:
        # Step 1: Query data
        bad_names = get_bad_names()

        # Step 2: Send email
        send_email_notification(bad_names)
        current_app.logger.info("Notification sent successfully.")
    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")

def setup_logging():
    # Load the logging configuration
    logging.config.fileConfig(os.path.join(os.path.dirname(__file__), "logging.conf"))
    logger = logging.getLogger("api")  # Use the `api` logger
    # Example log message
    logger.info("Logging is configured and ready!")

if __name__ == "__main__":
    setup_logging()
    app = create_app()
    with app.app_context():  # Ensures Flask app context is available
        run_task()
