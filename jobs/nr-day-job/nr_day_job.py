# Copyright © 2021 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""s2i based launch script to run the service."""
import asyncio
import os

from flask import Flask, current_app
from namex.models import Request, State, db
from namex.services.queue import QueueService
from sqlalchemy import text

import config
from utils.logging import setup_logging

APP_CONFIG = config.get_named_config(os.getenv('FLASK_ENV', 'production'))


async def run():
    """Run the day job."""
    app = Flask(__name__)
    app.config.from_object(APP_CONFIG)
    db.init_app(app)

    register_shellcontext(app)

    qsm = QueueService(app=app, loop=event_loop)

    await notify_nr_before_expiry(app, qsm)
    await notify_nr_expired(app, qsm)


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {'app': app}

    app.shell_context_processor(shell_context)


async def publish_email_message(qsm: QueueService, payload: dict):  # pylint: disable=redefined-outer-name
    """Publish the email message onto the NATS emailer subject."""
    subject = APP_CONFIG.NATS_EMAILER_SUBJECT
    current_app.logger.debug('publish to queue, subject:%s, event:%s', subject, payload)
    await qsm.publish_json_to_subject(payload, subject)


async def furnish_request_message(
        qsm: QueueService,
        request: Request,
        option: str
):  # pylint: disable=redefined-outer-name
    """Send notification info to the mail queue."""
    current_app.logger.debug('Start of the furnishing of request for %s nrNumber=%s', option, request.nrNum)
    payload = {
        'email': {
            'nrNumber': request.nrNum,
            'type': 'namerequest',
            'option': option
        }
    }

    current_app.logger.debug('About to publish email for %s nrNumber=%s', option, request.nrNum)
    await publish_email_message(qsm, payload)

    if option == 'before-expiry':
        request.notifiedBeforeExpiry = True
    elif option == 'expired':
        request.notifiedExpiry = True
    request.save_to_db()


async def notify_nr_before_expiry(app: Flask, qsm: QueueService):  # pylint: disable=redefined-outer-name
    """Send nr before expiry."""
    try:
        with app.app_context():
            app.logger.debug('entering notify_nr_before_expiry')

            where_clause = text(
                "expiration_date - interval '14 day' <= CURRENT_DATE AND expiration_date > CURRENT_DATE")
            requests = db.session.query(Request).filter(
                Request.stateCd.in_((State.APPROVED, State.CONDITIONAL)),
                Request.notifiedBeforeExpiry == False,  # noqa E712; pylint: disable=singleton-comparison
                where_clause
            ).all()
            for request in requests:
                await furnish_request_message(qsm, request, 'before-expiry')
    except Exception as err:  # noqa B902; pylint: disable=W0703;
        app.logger.error(err)


async def notify_nr_expired(app: Flask, qsm: QueueService):  # pylint: disable=redefined-outer-name
    """Send nr expired."""
    try:
        with app.app_context():
            app.logger.debug('entering notify_nr_expired')

            where_clause = text('expiration_date <= CURRENT_DATE')
            requests = db.session.query(Request).filter(
                Request.stateCd.in_((State.APPROVED, State.CONDITIONAL)),
                Request.notifiedBeforeExpiry == True,  # noqa E712; pylint: disable=singleton-comparison
                Request.notifiedExpiry == False,  # noqa E712; pylint: disable=singleton-comparison
                where_clause
            ).all()
            for request in requests:
                await furnish_request_message(qsm, request, 'expired')
    except Exception as err:  # noqa B902; pylint: disable=W0703;
        app.logger.error(err)


if __name__ == '__main__':
    setup_logging(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logging.conf'))

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run())
