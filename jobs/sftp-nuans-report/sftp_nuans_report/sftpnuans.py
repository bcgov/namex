"""The Notebook Report - This module is the API for the Filings Notebook Report."""

import fnmatch
import logging
import os
import sys
import traceback
from datetime import datetime, timezone

import papermill as pm
from config import Config
from flask import Flask, current_app
from services.email import EmailService
from services.sftp import SftpService
from structured_logging import StructuredLogging

# Suppress verbose papermill logging
logging.getLogger("papermill").setLevel(logging.ERROR)

# Notebook Scheduler
# ---------------------------------------
# This script helps with the automated processing of Jupyter Notebooks via
# papermill (https://github.com/nteract/papermill/)


def create_app(config=Config):
    """Create app."""
    app = Flask(__name__)
    app.config.from_object(config)

    # Configure Structured Logging
    structured_logger = StructuredLogging()
    structured_logger.init_app(app)
    app.logger = structured_logger.get_logger()

    return app


def findfiles(directory, pattern):
    """Find files matched."""
    for filename in os.listdir(directory):
        if fnmatch.fnmatch(filename.lower(), pattern):
            yield os.path.join(directory, filename)


def processnotebooks(notebookdirectory, data_dir):
    """Process data."""
    status = False

    current_app.logger.info('Start processing directory: %s', notebookdirectory)

    try:
        pm.execute_notebook(os.path.join(notebookdirectory, 'generate_files.ipynb'),
                            data_dir + 'temp.ipynb', parameters=None)
        os.remove(data_dir+'temp.ipynb')

        SftpService.send_to_ocp_sftp_relay(data_dir)

        status = True
    except Exception as e:  # noqa: B902
        current_app.logger.error(
            "Error processing notebook %s. Traceback:\n%s",
            notebookdirectory,
            traceback.format_exc()
        )
        EmailService.send_email_to_notify_api(notebookdirectory, str(e))
    return status


if __name__ == '__main__':
    app = create_app(Config)
    app.app_context().push()
    start_time = datetime.now(timezone.utc)

    temp_dir = os.path.join(os.getcwd(), r'sftp_nuans_report/data/')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    processnotebooks('sftp_nuans_report/notebook', temp_dir)
    # shutil.rmtree(temp_dir)

    end_time = datetime.now(timezone.utc)
    current_app.logger.info('job - jupyter notebook report completed in: %s', end_time - start_time)
    sys.exit()
