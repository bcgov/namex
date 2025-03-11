"""The Notebook Report - This module is the API for the Filings Notebook Report."""

import fnmatch
import logging
import os
import sys
from datetime import datetime

import papermill as pm
from flask import Flask, current_app

from config import Config
from util.logging import setup_logging
from services.sftp import SftpService
from services.email import EmailService

setup_logging(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logging.conf'))  # important to do this first

# Notebook Scheduler
# ---------------------------------------
# This script helps with the automated processing of Jupyter Notebooks via
# papermill (https://github.com/nteract/papermill/)


def create_app(config=Config):
    """Create app."""
    app = Flask(__name__)
    app.config.from_object(config)
    # db.init_app(app)
    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    return app


def findfiles(directory, pattern):
    """Find files matched."""
    for filename in os.listdir(directory):
        if fnmatch.fnmatch(filename.lower(), pattern):
            yield os.path.join(directory, filename)


def processnotebooks(notebookdirectory, data_dir):
    """Process data."""
    status = False

    logging.info('Start processing directory: %s', notebookdirectory)

    try:
        pm.execute_notebook(os.path.join(notebookdirectory, 'generate_files.ipynb'),
                            data_dir + 'temp.ipynb', parameters=None)
        os.remove(data_dir+'temp.ipynb')

        SftpService.send_to_ocp_sftp_relay(data_dir)

        status = True
    except Exception as e:  # noqa: B902
        logging.exception('Error processing notebook %s.', notebookdirectory)
        EmailService.send_email_to_notify_api(notebookdirectory, str(e))
    return status


if __name__ == '__main__':
    start_time = datetime.utcnow()

    temp_dir = os.path.join(os.getcwd(), r'sftp_nuans_report/data/')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    processnotebooks('sftp_nuans_report/notebook', temp_dir)
    # shutil.rmtree(temp_dir)

    end_time = datetime.utcnow()
    logging.info('job - jupyter notebook report completed in: %s', end_time - start_time)
    sys.exit()
