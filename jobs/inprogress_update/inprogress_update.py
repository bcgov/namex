import sys

from sqlalchemy import text
from datetime import datetime, timedelta

from flask import Flask, g, current_app

from namex import db
from namex.models import Request, State, User, Event
from namex.services import EventRecorder
from namex.utils.logging import setup_logging

from config import Config

setup_logging() ## important to do this first


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    return app

def get_ops_params():
    try:
        delay = int(current_app.config.get('MIN_DELAY_SECONDS', 1800))
    except:
        delay = 1800
    try:
        max_rows = int(current_app.config.get('MAX_ROW_LIMIT', 100))
    except:
        max_rows = 100

    return delay, max_rows


def job(user: User, max_rows: int, delay: int) -> (int, bool):
    row_count = 0

    try:

        reqs = db.session.query(Request). \
            filter(Request.stateCd == State.INPROGRESS). \
            filter(Request.lastUpdate <= text('(now() at time zone \'utc\') - INTERVAL \'{delay} SECONDS\''.format(delay=delay))). \
            order_by(Request.lastUpdate.asc()). \
            limit(max_rows). \
            with_for_update().all()

        for r in reqs:
            row_count += 1

            current_app.logger.debug('processing: {}'.format(r.nrNum))

            print ('nr {}, state: {} last_update:{}'.format(r.nrNum, r.stateCd, r.lastUpdate))

            # if this NR was previously in DRAFT, reset it to that state (ie: the user walked away from an open edit window)
            if r.previousStateCd == State.DRAFT:
                r.stateCd = State.DRAFT
                r.previousStateCd = None
            # otherwise put it on hold
            else:
                r.stateCd = State.HOLD

            db.session.add(r)
            EventRecorder.record(user, Event.MARKED_ON_HOLD, r, {}, save_to_session=True)

        db.session.commit()
        return row_count, True

    except Exception as err:
        current_app.logger.error(err)
        db.session.rollback()
        return -1, False


if __name__ == "__main__":
    NRO_SERVICE_ACCOUNT = 'NRO_SERVICE_ACCOUNT'
    app = create_app(Config)
    delay, max_rows = get_ops_params()

    start_time = datetime.utcnow()

    user = User.find_by_username(current_app.config[NRO_SERVICE_ACCOUNT])
    if not user:
        print("job: unable to load {0}, current config value={1}"
              .format(NRO_SERVICE_ACCOUNT, current_app.config[NRO_SERVICE_ACCOUNT]))
        exit(0)

    row_count, success = job(user, max_rows, delay)

    app.do_teardown_appcontext()
    end_time = datetime.utcnow()

    if success:
        print("job - requests processed: {0} completed in:{1}".format(row_count, end_time-start_time))
        exit(0)

    print('Failed to move timed out INPROGRESS NRs to HOLD: ', err, err.with_traceback(None), file=sys.stderr)
    exit(1)
