"""s2i based launch script to run the notebook."""
import fnmatch
import logging
import os
import smtplib
import sys
import traceback
from datetime import datetime, timedelta
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import papermill as pm
from flask import Flask, current_app

from config import Config
from util.logging import setup_logging

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

    message = MIMEMultipart()
    sender_email = os.getenv('SENDER_EMAIL', '')

    if emailtype == 'ERROR':
        subject = 'NR Duplicates Report Error Notification on ' + date + ext
        filename = ''
        recipients = os.getenv('ERROR_EMAIL_RECIPIENTS', '')
        message.attach(MIMEText('ERROR!!! \n' + errormessage, 'plain'))
    else:
        subject = 'NR Duplicates Report ' + date + ext
        filename = 'nr_duplicates_' + date + '.csv'
        recipients = os.getenv('DAILY_REPORT_RECIPIENTS', '')
        # Add body to email
        message.attach(MIMEText('Please see attached.', 'plain'))

        # Open file in binary mode
        with open(os.path.join(os.getcwd(), r'data/')+filename, 'rb') as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {filename}',
        )

        # Add attachment to message and convert message to string
        message.attach(part)

    message['Subject'] = subject
    server = smtplib.SMTP(os.getenv('EMAIL_SMTP', ''))
    email_list = []
    email_list = recipients.strip('][').split(', ')
    logging.info('Email recipients list is: %s', email_list)
    server.sendmail(sender_email, email_list, message.as_string())
    logging.info(
        'Email with subject \"%s\" has been sent successfully!', subject)
    server.quit()


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
    except Exception:  # noqa: B902
        logging.exception(
            'NR Duplicates Report Error processing %s.', notebookdirectory)
        send_email('ERROR', traceback.format_exc())
    return status


if __name__ == '__main__':
    start_time = datetime.utcnow()

    temp_dir = os.path.join(os.getcwd(), r'data/')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    processnotebooks('daily', temp_dir)
    # shutil.rmtree(temp_dir)

    end_time = datetime.utcnow()
    logging.info('job - jupyter notebook report completed in: %s',
                 end_time - start_time)
    sys.exit()
