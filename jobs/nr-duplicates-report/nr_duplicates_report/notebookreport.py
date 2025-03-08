"""s2i based launch script to run the notebook."""
import fnmatch
import logging
import os
import sys
import traceback
from datetime import datetime, timedelta

import papermill as pm
from flask import Flask, current_app

from config import Config
from util.logging import setup_logging
from util.email import send_email_notification

setup_logging(os.path.join(os.path.abspath(os.path.dirname(
    __file__)), 'logging.conf'))  # important to do this first

# Notebook Scheduler
# ---------------------------------------
# This script helps with the automated processing of Jupyter Notebooks via
# papermill (https://github.com/nteract/papermill/)


def create_app(config=Config):
    """create_app."""
    app = Flask(__name__)
    app.config.from_object(config)
    app.app_context().push()
    current_app.logger.debug(
        'created the Flask App and pushed the App Context')

    return app


def findfiles(directory, pattern):
    """findfiles."""
    # Lists all files in the specified directory that match the specified pattern
    for filename in os.listdir(directory):
        if fnmatch.fnmatch(filename.lower(), pattern):
            yield os.path.join(directory, filename)


def send_email(emailtype, errormessage):
    """Send email."""
    number_of_days_nr = int(os.getenv('NUMBER_OF_DAYS_NR', '1'))
    date = datetime.strftime(
        datetime.now()-timedelta(number_of_days_nr), '%Y-%m-%d')
    ext = ''
    if os.getenv('ENVIRONMENT', '') != 'prod':
        ext = ' on ' + os.getenv('ENVIRONMENT', '')

    if emailtype == 'ERROR':
        subject = 'NR Duplicates Report Error Notification on ' + date + ext
        filename = ''
        recipients = Config.ERROR_EMAIL_RECIPIENTS
        email_list = [email.strip() for email in (recipients.strip("[]").split(",") if isinstance(recipients, str) else recipients)]
        message = 'ERROR!!! \n' + errormessage
        attatchments = []
    else:
        subject = 'NR Duplicates Report ' + date + ext
        filename = 'nr_duplicates_' + date + '.csv'
        recipients = Config.REPORT_RECIPIENTS
        email_list = [email.strip() for email in (recipients.strip("[]").split(",") if isinstance(recipients, str) else recipients)]
        message = 'Please see the attachment(s).'
        attatchments = [(os.path.join(os.getcwd(), r'nr_duplicates_report/data/')+filename)]

    logging.info('Email recipients list is: %s', email_list)
    send_email_notification(email_list, subject, message, attatchments)


def processnotebooks(notebookdirectory, data_dir):
    """Process Notebook."""
    status = False
    logging.info('NR Duploicates Report start processing directory: %s',
                 notebookdirectory)
    try:
        pm.execute_notebook(os.path.join(notebookdirectory, 'nr-duplicates.ipynb'),
                            data_dir + 'temp.ipynb', parameters=None)

        # send email to receivers and remove files/directories which we don't want to keep
        send_email('', '')
        os.remove(data_dir+'temp.ipynb')
        status = True
    except Exception as e:  # noqa: B902
        logging.exception(
            'NR Duplicates Report Error processing %s.', notebookdirectory)
        send_email('ERROR', f'An error occurred: {str(e)}')
    return status


if __name__ == '__main__':
    start_time = datetime.utcnow()

    temp_dir = os.path.join(os.getcwd(), r'nr_duplicates_report/data/')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    processnotebooks('nr_duplicates_report/daily', temp_dir)
    # shutil.rmtree(temp_dir)

    end_time = datetime.utcnow()
    logging.info('job - jupyter notebook report completed in: %s',
                 end_time - start_time)
    sys.exit()
