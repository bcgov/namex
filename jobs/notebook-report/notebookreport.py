import os
import sys
import ast
import time
import smtplib
import email
import traceback
import argparse
import fnmatch
import logging
import papermill as pm
import shutil
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from util.logging import setup_logging
from flask import Flask, g, current_app
from config import Config

setup_logging(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logging.conf'))  # important to do this first

# Notebook Scheduler
# ---------------------------------------
# This script helps with the automated processing of Jupyter Notebooks via
# papermill (https://github.com/nteract/papermill/)

snapshotDir = 'snapshots'


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    # db.init_app(app)
    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    return app


def findfiles(directory, pattern):
    # Lists all files in the specified directory that match the specified pattern
    for filename in os.listdir(directory):
        if fnmatch.fnmatch(filename.lower(), pattern):
            yield os.path.join(directory, filename)


def send_email(subject, filename, emailtype, errormessage):
    message = MIMEMultipart()
    message["Subject"] = subject
    sender_email = os.getenv('SENDER_EMAIL', '')

    if emailtype == "ERROR":
        recipients = os.getenv('ERROR_EMAIL_RECIPIENTS', '')
        message.attach(MIMEText("ERROR!!! \n" + errormessage, "plain"))
    else:
        if subject.startswith("Daily"):
            recipients = os.getenv('DAILY_REPORT_RECIPIENTS', '')
        if subject.startswith("Weekly"):
            recipients = os.getenv('WEEKLY_REPORT_RECIPIENTS', '')    
        # Add body to email
        message.attach(MIMEText("Please see attached.", "plain"))

        # Open file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)

    server = smtplib.SMTP(os.getenv('EMAIL_SMTP', ''))
    email_list = []
    email_list = recipients.strip('][').split(', ')
    logging.info('Email recipients list is: {}'.format(email_list))
    server.sendmail(sender_email, email_list, message.as_string())
    logging.info('Email with subject \'' + subject + '\' has been sent successfully!')
    server.quit()


def processnotebooks(notebookdirectory):
    status = False    
    weekno = datetime.now().weekday()
    date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    ext = ''
    if not os.getenv('ENVIRONMENT', '') == 'prod':
        ext = ' on ' + os.getenv('ENVIRONMENT', '')

    try:
        retry_times = int(os.getenv('RETRY_TIMES', '1'))
        retry_interval = int(os.getenv('RETRY_INTERVAL', '60'))
        if notebookdirectory == 'weekly':            
            weekreportday = ast.literal_eval(os.getenv('WEEK_REPORT_DATE', ''))                    
    except Exception:
        logging.exception("Error processing notebook for {}.".format(notebookdirectory))
        # we failed all the attempts
        subject = "NameX Jupyter Notebook Error Notification for " + notebookdirectory + " on " + date + ext
        filename = ''
        send_email(subject, filename, "ERROR", traceback.format_exc())
        return status

    # For weekly tasks, we only run on the specified days
    # Only run weekly report on Monday (index is 0) for previous 7 days data
    if ( notebookdirectory == 'daily' or (notebookdirectory == 'weekly' and weekno in weekreportday)): 

        logging.info('Processing: ' + notebookdirectory)      

        # Each time a notebook is processed a snapshot is saved to a snapshot sub-directory
        # This checks the sub-directory exists and creates it if not
        snapshot_dir = os.path.join(notebookdirectory, snapshotDir)
        if not os.path.isdir(snapshot_dir):
            os.mkdir(snapshot_dir)

        for file in findfiles(notebookdirectory, '*.ipynb'):
            note_book = os.path.basename(file)
            for attempt in range(retry_times):
                try:
                    pm.execute_notebook(file, os.getenv('DATA_DIR', '')+'temp.ipynb', parameters=None)                  
            
                    nbfile = note_book.split('.ipynb')[0]

                    if nbfile == 'daily':
                        subject = "Daily NameX Stats for " + date + ext
                        filename = 'daily_totals_' + date + '.csv'
                    elif nbfile == 'weekly':
                        subject = "Weekly NameX Stats till " + date + ext
                        filename = 'weekly_totals_till_' + datetime.strftime(datetime.now()-timedelta(1), '%Y-%m-%d') +'.csv'

                    # send email to receivers and remove files/directories which we don't want to keep
                    send_email(subject, filename, "", "")
                    os.remove(os.getenv('DATA_DIR', '')+'temp.ipynb') 
                    
                    status = True
                    break
                except Exception:
                    if attempt + 1 == retry_times:
                        # If any errors occur with the notebook processing they will be logged to the log file
                        logging.exception("Error processing notebook {0} at {1}/{2} try.".format(notebookdirectory, attempt + 1, retry_times))
                        # we failed all the attempts
                        subject = "NameX Jupyter Notebook Error Notification for " + notebookdirectory + " on " + date + ext
                        filename = ''
                        send_email(subject, filename, "ERROR", traceback.format_exc())
                    else:
                        # If any errors occur with the notebook processing they will be logged to the log file
                        logging.exception("Error processing notebook {0} at {1}/{2} try. Sleeping for {3} secs before next try"
                                          .format(notebookdirectory, attempt + 1, retry_times, retry_interval))
                        time.sleep(retry_interval)
                        continue
            if not status:
                break

        shutil.rmtree(snapshot_dir, ignore_errors=True)        
        return status


if __name__ == '__main__':
    start_time = datetime.utcnow()    

    # Check if the subfolders for notebooks exist, and create them if they don't    
    for directory in ['daily', 'weekly']:  
        if not os.path.isdir(directory):
            os.mkdir(directory)
    
        processnotebooks(directory)        
    end_time = datetime.utcnow()
    logging.info("job - jupyter notebook report completed in: {}".format(end_time - start_time))
    exit(0)
