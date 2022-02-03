"""Script used to regularly update INPROGRESS NRs."""
from datetime import datetime

from flask import Flask, current_app
from namex import db, nro
from namex.models import Event, Request, State, User
from namex.services import EventRecorder
from namex.utils.logging import setup_logging
from sqlalchemy import text

from config import Config


setup_logging()  # important to do this first


def create_app(config=Config):
    """Create instance of app."""
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    nro.init_app(app)
    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    return app


def get_ops_params():
    """Get params for job."""
    client_delay = int(current_app.config.get('MIN_CLIENT_DELAY_SECONDS', 900))
    examine_delay = int(current_app.config.get('MIN_EXAMINE_DELAY_SECONDS', 1800))
    max_rows = int(current_app.config.get('MAX_ROW_LIMIT', 100))

    return client_delay, examine_delay, max_rows


def inprogress_update(user: User, max_rows: int, client_delay: int, examine_delay: int) -> (int, bool):
    """Update inprogress nrs."""
    row_count = 0

    try:
        # for nrs edited by clients
        client_edit_reqs = db.session.query(Request). \
            filter(Request.stateCd == State.INPROGRESS). \
            filter(Request.lastUpdate <= text(f'(now() at time zone \'utc\') - INTERVAL \'{client_delay} SECONDS\'')). \
            filter(Request.checkedOutBy != None). \
            order_by(Request.lastUpdate.asc()). \
            limit(max_rows). \
            with_for_update().all()
        for r in client_edit_reqs:
            row_count += 1

            current_app.logger.debug(f'processing: {r.nrNum}')
            current_app.logger.debug(f'nr {r.nrNum}, state: {r.stateCd} last_update:{r.lastUpdate}')

            r.stateCd = State.DRAFT
            r.checkedOutBy = None
            db.session.add(r)
            errors = nro.checkin_checkout_nr(r, 'UNLOCK')
            if errors:
                raise RuntimeError('Failed to update nro.')
            # commit here to keep this entry in sync with NRO (in case errors happen later)
            db.session.commit()

            EventRecorder.record(user, Event.SET_TO_DRAFT, r, r.json(), save_to_session=True)

        # for nrs edited by examiners
        examine_reqs = db.session.query(Request). \
            filter(Request.stateCd == State.INPROGRESS). \
            filter(Request.lastUpdate <= text(f"(now() at time zone 'utc') - INTERVAL '{examine_delay} SECONDS'")). \
            filter(Request.checkedOutBy == None). \
            order_by(Request.lastUpdate.asc()). \
            limit(max_rows). \
            with_for_update().all()

        for r in examine_reqs:
            row_count += 1

            current_app.logger.debug(f'processing: {r.nrNum}')
            current_app.logger.debug(f'nr {r.nrNum}, state: {r.stateCd} last_update:{r.lastUpdate}')

            # if this NR was previously in DRAFT, reset it to that state
            # (ie: the user walked away from an open edit window)
            event = None
            if r.previousStateCd == State.DRAFT:
                r.stateCd = State.DRAFT
                r.previousStateCd = None
                event = Event.SET_TO_DRAFT
            # otherwise put it on hold
            else:
                r.stateCd = State.HOLD
                event = Event.MARKED_ON_HOLD

            db.session.add(r)
            EventRecorder.record(user, event, r, r.json(), save_to_session=True)

        # for NRs showing in NRO_UPDATING status need to be set to DRAFT
        nro_updating_reqs = db.session.query(Request). \
            filter(Request.stateCd == State.NRO_UPDATING). \
            order_by(Request.lastUpdate.asc()). \
            limit(max_rows). \
            with_for_update().all()

        for r in nro_updating_reqs:
            row_count += 1

            current_app.logger.debug(f'processing: {r.nrNum}')
            current_app.logger.debug(f'nr {r.nrNum}, state: {r.stateCd} last_update:{r.lastUpdate}')            
            
            r.stateCd = State.DRAFT
            event = Event.SET_TO_DRAFT
            
            db.session.add(r)
            EventRecorder.record(user, event, r, r.json(), save_to_session=True)
        db.session.commit()
        return row_count, True

    except Exception as err:
        current_app.logger.error(err)
        db.session.rollback()
        return -1, False


if __name__ == '__main__':
    # TODO: make service account for inporgress updater
    NRO_SERVICE_ACCOUNT = 'NRO_SERVICE_ACCOUNT'
    app = create_app(Config)
    client_delay, examine_delay, max_rows = get_ops_params()

    start_time = datetime.utcnow()

    user = User.find_by_username(current_app.config[NRO_SERVICE_ACCOUNT])
    if not user:
        current_app.logger.error(f'Setup error: unable to load {NRO_SERVICE_ACCOUNT}.')
        exit(1)

    row_count, success = inprogress_update(user, max_rows, client_delay, examine_delay)
    app.do_teardown_appcontext()
    end_time = datetime.utcnow()
    if success:
        current_app.logger.debug(f'Requests processed: {row_count} completed in:{end_time-start_time}')
    else:
        current_app.logger.error('Failed to move timed out INPROGRESS NRs')
        exit(1)
