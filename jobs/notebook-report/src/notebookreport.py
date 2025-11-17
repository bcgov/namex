"""s2i based launch script to run the notebook."""
import ast
import base64
import fnmatch
import logging
import os
import sys
import traceback
from datetime import datetime, timedelta
from pathlib import Path

import papermill as pm
import requests
from flask import Flask, current_app
from structured_logging import StructuredLogging

from config import Config

# Suppress verbose papermill logging
logging.getLogger("papermill").setLevel(logging.ERROR)

# Notebook Scheduler
# ---------------------------------------
# This script helps with the automated processing of Jupyter Notebooks via
# papermill (https://github.com/nteract/papermill/)


def create_app(config=Config):
    """create_app."""
    app = Flask(__name__)
    app.config.from_object(config)

    # Configure Structured Logging
    structured_logger = StructuredLogging()
    structured_logger.init_app(app)
    app.logger = structured_logger.get_logger()

    return app


def findfiles(directory, pattern):
    """findfiles."""
    # Lists all files in the specified directory that match the specified pattern
    for filename in os.listdir(directory):
        if fnmatch.fnmatch(filename.lower(), pattern):
            yield os.path.join(directory, filename)


def send_email(email: dict, token):
    """Send the email."""
    current_app.logger.info('email is: %s', str(email))
    
    response = requests.request("POST",
        Config.NOTIFY_API_URL,
        json=email,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    if response.status_code != 200:
        current_app.logger.info(f'response:{response}')
        # print(response)
        # current_app.logger.info(f'response:{response}')
        raise Exception('Unsuccessful response when sending email.')

def processnotebooks(notebookdirectory, token):
    """Process Notebook."""
    date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    weekreportday = ast.literal_eval(Config.WEEK_REPORT_DATE)
    ext = ''
    if Config.ENVIRONMENT != 'prod':
        ext = ' on ' + Config.ENVIRONMENT

    # For weekly tasks, we only run on the specified days
    # Only run weekly report on Monday (index is 0) for previous 7 days data
    if (notebookdirectory == 'daily' or (notebookdirectory == 'weekly' and datetime.now().weekday() in weekreportday)):
        current_app.logger.info('Processing: %s', notebookdirectory)
        for file in findfiles(notebookdirectory, '*.ipynb'):
            nbfile = os.path.basename(file).split('.ipynb')[0]

            if nbfile == 'daily':
                subject = 'Daily NameX Stats for ' + date + ext
                # filename = 'daily_totals_' + date + '.csv'
                filename = os.path.join(notebookdirectory, f'daily_totals_{date}.csv')
                recipients = Config.DAILY_REPORT_RECIPIENTS   
            elif nbfile == 'weeklynamex':
                subject = 'Weekly NameX Stats till ' + date + ext
                # filename = 'weekly_totals_till_' + datetime.strftime(datetime.now()-timedelta(1), '%Y-%m-%d') + '.csv'
                filename = os.path.join(notebookdirectory, f'weekly_totals_till_{date}.csv')
                recipients = Config.WEEKLY_REPORT_NAMEX_RECIPIENTS   

            email = {
                'recipients': recipients,
                'content': {
                    'subject': subject,
                    'body': 'Please see the attachment(s).',
                    'attachments': []
                }
            }                        
            
            try:
                temp_file = 'temp.ipynb'
                # pm.execute_notebook(file, temp_file, parameters=None)
                pm.execute_notebook(
                    input_path=file,
                    output_path=temp_file,
                    parameters=None,
                    cwd=os.path.dirname(file),   # crucial!
                )

                with open(filename, "rb") as f:
                    attachments = []
                    file_encoded = base64.b64encode(f.read())
                    attachments.append(
                        {
                            'fileName': filename,
                            'fileBytes': file_encoded.decode(),
                            'fileUrl': '',
                            'attachOrder': 1
                        }
                    )
                email['content']['attachments'] = attachments
            except Exception:  # noqa: B902
                email = {
                    'recipients': Config.ERROR_EMAIL_RECIPIENTS,
                    'content': {
                        'subject': 'Error Notification ' + subject,
                        'body': 'Failed to generate report: ' + traceback.format_exc(),
                        'attachments': []
                    }
                }
            finally:
                if Path(temp_file).exists():
                    os.remove('temp.ipynb')
                if Path(filename).exists():    
                    os.remove(filename)
                send_email(email, token)


if __name__ == '__main__':
    app = create_app(Config)
    app.app_context().push()
    START_TIME = datetime.now()
    
    client = Config.NOTIFY_CLIENT_ID
    secret = Config.NOTIFY_CLIENT_SECRET
    kc_url = Config.KEYCLOAK_AUTH_TOKEN_URL 
    response = requests.post(url=kc_url,
        data='grant_type=client_credentials',
        headers={'content-type': 'application/x-www-form-urlencoded'},
        auth=(client, secret))
    token = response.json()['access_token']
    
    # Check if the subfolders for notebooks exist, and create them if they don't
    for _directory in ['daily', 'weekly']:
        if not os.path.isdir(_directory):
            os.mkdir(_directory)

        processnotebooks(_directory, token)
    END_TIME = datetime.now()
    current_app.logger.info('job - jupyter notebook report completed in: %s', (END_TIME - START_TIME))
    sys.exit()
