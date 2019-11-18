import os
import sys
import traceback
import argparse
import fnmatch
import logging
import papermill as pm
import shutil
import time
import email, smtplib
from datetime import datetime, timedelta
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, g, current_app
from namex.utils.logging import setup_logging
from config import Config
from app import create_app, db

setup_logging() # important to do this first
app = create_app(Config)

# Notebook Scheduler
# ---------------------------------------
# This script helps with the automated processing of Jupyter Notebooks via papermill (https://github.com/nteract/papermill/)

snapshotDir = 'snapshots'

def findFiles(directory, pattern):
    # Lists all files in the specified directory that match the specified pattern
    for filename in os.listdir(directory):
        if fnmatch.fnmatch(filename.lower(), pattern):
            yield os.path.join(directory, filename)

def send_email(subject, filename, emailtype, errormessage):
    message = MIMEMultipart()
    message["Subject"] = subject
    sender_email = "steven.chen@gov.bc.ca"

    if emailtype == "ERROR":
        recipients = ['steven.chen@gov.bc.ca']
        message.attach(MIMEText("ERROR!!! \n" + errormessage, "plain"))
    else:
        recipients = ['steven.chen@gov.bc.ca']
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

    server = smtplib.SMTP("apps.smtp.gov.bc.ca")
    emaillist = [elem.strip().split(',') for elem in recipients]
    server.sendmail(sender_email, emaillist, message.as_string())
    server.quit()


def processNotebooks(notebookDirectory, days=[], months=[]):
    
    now = datetime.now()

    # For six months tasks or monthly tasks, we only run on the specified days and month
    # (or for others if no days are specified)
    if (len(months) > 0 and now.month in months and len(days) > 0 and now.day in days) \
            or (len(months) == 0 and len(days) > 0 and now.day in days) \
            or (len(months) == 0 and len(days) == 0):

        logging.info('Processing ' + notebookDirectory)
        
        # Each time a notebook is processed a snapshot is saved to a snapshot sub-directory
        # This checks the sub-directory exists and creates it if not
        if os.path.isdir(os.path.join(notebookDirectory,snapshotDir)) == False:
            os.mkdir(os.path.join(notebookDirectory,snapshotDir))
        
        for file in findFiles(notebookDirectory, '*.ipynb'):
            date = datetime.strftime(datetime.now(), '%Y-%m-%d')
            try:
                nb = os.path.basename(file)
                
                # Within the snapshot directory, each notebook output is stored in its own sub-directory
                notebookSnapshot = os.path.join(notebookDirectory, snapshotDir, nb.split('.ipynb')[0])
                
                if os.path.isdir(notebookSnapshot) == False:
                    os.mkdir(notebookSnapshot)

                # The output will be saved in a timestamp directory (snapshots/notebook/timestamp) 
                runDir = os.path.join(notebookSnapshot, now.strftime("%Y-%m-%d %H.%M.%S.%f"))
                if os.path.isdir(runDir) == False:
                    os.mkdir(runDir)

                # The snapshot file includes a timestamp
                output_file = os.path.join(runDir, nb)
                
                # Execute the notebook and save the snapshot
                pm.execute_notebook(
                    file,
                    output_file,
                    parameters=dict(snapshotDir = runDir + os.sep)
                )

                if notebookDirectory == 'daily':
                    subject = "NameX Daily Stats for " + date
                    filename = 'daily_totals_' + date + '.csv'
                    dest = './daily/'
                    # send email to receivers
                    send_email(subject, filename, "", "")
                    # move csv file to sub directory
                    if os.path.exists(dest + filename):
                        os.remove(dest + filename)
                    shutil.move(filename, dest)
                elif notebookDirectory == 'sixMonth':
                    subject = "NameX Six Months Stats Before " + date
                    filename = 'six_month_totals_before_' + date+'.csv'
                    dest = './sixMonth/'
                    # send email to receivers
                    send_email(subject, filename, "", "")
                    # move csv file to sub directory
                    if os.path.exists(dest + filename):
                        os.remove(dest + filename)
                    shutil.move(filename, dest)
            except Exception:
                # If any errors occur with the notebook processing they will be logged to the log file
                logging.exception("Error processing notebook")
                subject = "NameX Jupyter Notebook Error Notification on " + date
                filename = ''
                send_email(subject, filename, "ERROR", traceback.format_exc())



if __name__ == '__main__':

    # Ensure we're running in the same directory as the script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Set up logger to display to screen and file
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='notebooks.log')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)

    # Check if the subfolders for notebooks exist, and create them if they don't
    # for directory in ['daily', 'sixMonth']:
    for directory in ['daily', 'sixMonth']:
        if os.path.isdir(directory) == False:
            os.mkdir(directory)

    processNotebooks("daily")
    processNotebooks("sixMonth", days=[1, 15], months=[1, 7, 11])