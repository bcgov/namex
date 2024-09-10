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
import os
import uuid
from datetime import datetime, timezone

from flask import Flask, current_app
from namex.models import Request, State, db, Event
from namex.services import queue, EventRecorder
from sbc_common_components.utils.enums import QueueMessageTypes
from simple_cloudevent import SimpleCloudEvent
from sqlalchemy import text

import config
from utils.logging import setup_logging

APP_CONFIG = config.get_named_config(os.getenv('FLASK_ENV', 'production'))


def create_app():
    """Return a configured Flask App using the Factory method."""
    app = Flask(__name__)
    app.config.from_object(APP_CONFIG)

    queue.init_app(app)
    db.init_app(app)

    register_shellcontext(app)

    return app


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {'app': app}

    app.shell_context_processor(shell_context)


def publish_email_message(payload: dict):
    """Publish the email message onto the pubsub emailer topic."""
    email_topic = current_app.config.get('EMAILER_TOPIC', '')
    current_app.logger.debug('publish to queue, subject:%s, event:%s', email_topic, payload)
    queue.publish(topic=email_topic, payload=payload)

def furnish_request_message(
        request: Request,
        option: str
):  # pylint: disable=redefined-outer-name
    """Send notification info to the mail queue."""
    current_app.logger.debug('Start of the furnishing of request for %s nrNum=%s', option, request.nrNum)
    ce = SimpleCloudEvent(
        id=str(uuid.uuid4()),
        source=f'/requests/{request.nrNum}',
        subject="namerequest",
        type=QueueMessageTypes.NAMES_MESSAGE_TYPE.value,
        time=datetime.now(tz=timezone.utc).isoformat(),
        data={
            'request': {
                'nrNum': request.nrNum,
                'option': option
            }
        }
    )
    payload = queue.to_queue_message(ce)
    current_app.logger.debug('About to publish email for %s nrNum=%s', option, request.nrNum)

    publish_email_message(payload)

    if option == 'before-expiry':
        request.notifiedBeforeExpiry = True
    elif option == 'expired':
        request.notifiedExpiry = True
        request.stateCd = State.EXPIRED
    request.save_to_db()


def notify_nr_before_expiry():
    """Send nr before expiry."""
    try:
        current_app.logger.debug('entering notify_nr_before_expiry')

        where_clause = text(
            "expiration_date::DATE - interval '14 day' <= CURRENT_DATE and expiration_date::DATE > CURRENT_DATE")
        requests = db.session.query(Request).filter(
            Request.stateCd.in_((State.APPROVED, State.CONDITIONAL)),
            Request.notifiedBeforeExpiry == False,  # noqa E712; pylint: disable=singleton-comparison
            where_clause
        ).all()
        for request in requests:
            furnish_request_message(request, 'before-expiry')
    except Exception as err:  # noqa B902; pylint: disable=W0703;
        current_app.logger.error(err)


def notify_nr_expired():
    """Send nr expired."""
    try:
        current_app.logger.debug('entering notify_nr_expired')

        where_clause = text('expiration_date::DATE <= CURRENT_DATE')
        requests = db.session.query(Request).filter(
            Request.stateCd.in_((State.APPROVED, State.CONDITIONAL)),
            Request.notifiedExpiry == False,  # noqa E712; pylint: disable=singleton-comparison
            where_clause
        ).all()
        for request in requests:
            furnish_request_message(request, 'expired')
            EventRecorder.record_as_system(Event.NR_DAY_JOB, request, request.json())

    except Exception as err:  # noqa B902; pylint: disable=W0703;
        current_app.logger.error(err)


if __name__ == '__main__':
    setup_logging(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logging.conf'))

    application = create_app()
    with application.app_context():
        notify_nr_expired()
        notify_nr_before_expiry()
