"""s2i based launch script to run the notebook."""
import ast
import fnmatch
import logging
import os
import smtplib
import sys
import time
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


setup_logging(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logging.conf'))  # important to do this first

# Notebook Scheduler
# ---------------------------------------
# This script helps with the automated processing of Jupyter Notebooks via
# papermill (https://github.com/nteract/papermill/)


def create_app(config=Config):
    """create_app."""
    app = Flask(__name__)
    app.config.from_object(config)
    # db.init_app(app)
    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    return app


def findfiles(directory, pattern):
    """findfiles."""
    # Lists all files in the specified directory that match the specified pattern
    for filename in os.listdir(directory):
        if fnmatch.fnmatch(filename.lower(), pattern):
            yield os.path.join(directory, filename)


def send_email(subject, filename, emailtype, errormessage):
    """Send email."""
    message = MIMEMultipart()
    message['Subject'] = subject
    sender_email = os.getenv('SENDER_EMAIL', '')

    if emailtype == 'ERROR':
        recipients = os.getenv('ERROR_EMAIL_RECIPIENTS', '')
        message.attach(MIMEText('ERROR!!! \n' + errormessage, 'plain'))
    else:
        if subject.startswith('Daily'):
            recipients = os.getenv('DAILY_REPORT_RECIPIENTS', '')
        if subject.startswith('Weekly NameX'):
            recipients = os.getenv('WEEKLY_REPORT_NAMEX_RECIPIENTS', '')
        # Add body to email
        message.attach(MIMEText('Please see attached.', 'plain'))

        # Open file in binary mode
        with open(os.getenv('DATA_DIR', '')+filename, 'rb') as attachment:
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

    server = smtplib.SMTP(os.getenv('EMAIL_SMTP', ''))
    email_list = []
    email_list = recipients.strip('][').split(', ')
    logging.info('Email recipients list is: %s', email_list)
    server.sendmail(sender_email, email_list, message.as_string())
    logging.info('Email with subject %s has been sent successfully!', email_list)
    server.quit()
    os.remove(os.getenv('DATA_DIR', '')+filename)


def processnotebooks(notebookdirectory):
    """Process Notebook."""
    status = False
    date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    ext = ''
    if os.getenv('ENVIRONMENT', '') != 'prod':
        ext = ' on ' + os.getenv('ENVIRONMENT', '')

    try:
        retry_times = int(os.getenv('RETRY_TIMES', '1'))
        retry_interval = int(os.getenv('RETRY_INTERVAL', '60'))
        if notebookdirectory == 'weekly':
            weekreportday = ast.literal_eval(os.getenv('WEEK_REPORT_DATE', '[0,1,2,3,4,5]'))
    except Exception:  # noqa: B902
        logging.exception('Error processing notebook for %s.', notebookdirectory)
        # we failed all the attempts
        subject = 'NameX Jupyter Notebook Error Notification for ' + notebookdirectory + ' on ' + date + ext
        filename = ''
        send_email(subject, filename, 'ERROR', traceback.format_exc())
        return status

    # For weekly tasks, we only run on the specified days
    # Only run weekly report on Monday (index is 0) for previous 7 days data
    if (notebookdirectory == 'daily' or (notebookdirectory == 'weekly' and datetime.now().weekday() in weekreportday)):
        logging.info('Processing: %s', notebookdirectory)

        num_files = len(os.listdir(notebookdirectory))
        file_processed = 0

        for file in findfiles(notebookdirectory, '*.ipynb'):
            file_processed += 1
            note_book = os.path.basename(file)
            for attempt in range(retry_times):
                try:
                    pm.execute_notebook(file, os.getenv('DATA_DIR', '')+'temp.ipynb', parameters=None)
                    nbfile = note_book.split('.ipynb')[0]

                    if nbfile == 'daily':
                        subject = 'Daily NameX Stats for ' + date + ext
                        filename = 'daily_totals_' + date + '.csv'
                    elif nbfile == 'weeklynamex':
                        subject = 'Weekly NameX Stats till ' + date + ext
                        filename = 'weekly_totals_till_' + datetime.strftime(datetime.now()-timedelta(1),
                                                                             '%Y-%m-%d') + '.csv'

                    # send email to receivers and remove files/directories which we don't want to keep
                    send_email(subject, filename, '', '')
                    os.remove(os.getenv('DATA_DIR', '')+'temp.ipynb')
                    status = True
                    break
                except Exception:  # noqa: B902
                    if attempt + 1 == retry_times:
                        # If any errors occur with the notebook processing they will be logged to the log file
                        logging.exception('Error processing notebook %s at %s/%s try.',
                                          notebookdirectory, attempt + 1, retry_times)
                        # we failed all the attempts
                        subject = 'NameX Jupyter Notebook Error Notification for ' + notebookdirectory + \
                                  ' on ' + date + ext
                        filename = ''
                        send_email(subject, filename, 'ERROR', traceback.format_exc())
                    else:
                        # If any errors occur with the notebook processing they will be logged to the log file
                        logging.exception('Error processing notebook %s at %s/%s try. Sleeping for %s secs before \
                                          next try', notebookdirectory, attempt + 1, retry_times, retry_interval)
                        time.sleep(retry_interval)
                        continue
            if not status and num_files == file_processed:
                break
    return status


if __name__ == '__main__':
    START_TIME = datetime.utcnow()

    # Check if the subfolders for notebooks exist, and create them if they don't
    for _directory in ['daily', 'weekly']:
        if not os.path.isdir(_directory):
            os.mkdir(_directory)

        processnotebooks(_directory)
    END_TIME = datetime.utcnow()
    logging.info('job - jupyter notebook report completed in: %s', (END_TIME - START_TIME))
    sys.exit()
