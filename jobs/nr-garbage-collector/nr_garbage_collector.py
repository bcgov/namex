"""Script used to regularly cancel test NRs."""
from flask import Flask, current_app
from namex import db
from namex.models import Request, State
from namex.resources.name_requests.resource import NameRequestResource
from namex.utils.logging import setup_logging
from sqlalchemy import text

from config import get_named_config


setup_logging()  # important to do this first


def create_app(environment='production'):
    """Create instance of service."""
    app = Flask(__name__)
    app.config.from_object(get_named_config(environment))
    db.init_app(app)
    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    return app


def run_nr_garbage_collection():
    """Search for stale test NRs and cancel them."""
    app = create_app()

    delay = current_app.config.get('STALE_THRESHOLD')
    max_rows = current_app.config.get('MAX_ROWS_LIMIT')
    cancelled_nrs = []
    try:
        reqs = db.session.query(Request). \
            filter(Request.nrNum.contains('NR L')). \
            filter(Request.stateCd.in_((State.DRAFT, State.COND_RESERVE, State.RESERVED))). \
            filter(Request.lastUpdate <= text(f"(now() at time zone 'utc') - INTERVAL '{delay} SECONDS'")). \
            order_by(Request.lastUpdate.asc()). \
            limit(max_rows). \
            with_for_update().all()

        row_count = 0
        for r in reqs:
            row_count += 1

            current_app.logger.debug(f'cancelling NR: {r.nrNum}, STATE: {r.stateCd}, LAST UPDATE: {r.lastUpdate}')

            original_state = r.stateCd
            r.stateCd = State.CANCELLED
            if r.names:
                try:
                    current_app.logger.debug(f'deleting {r.nrNum} from possible.conflicts...')
                    deletion = NameRequestResource.delete_solr_doc('possible.conflicts', r.nrNum)
                    if deletion:
                        cancelled_nrs.append(
                            {
                                'id': r.nrNum,
                                'name': r.names[0].name,
                                'source': 'NR',
                                'start_date': r.submittedDate.strftime('%Y-%m-%dT%H:%M:00Z')
                            }
                        )
                        current_app.logger.debug(f'successfully deleted {r.nrNum} from possible.conflics.')
                    else:
                        raise Exception(f'Failed to delete {r.nrNum} from solr possible.conflicts core')
                except Exception as err:
                    current_app.logger.error(err)
                    current_app.logger.debug(f'setting {r.nrNum} back to original state...')
                    r.stateCd = original_state

            db.session.add(r)

        db.session.commit()
        current_app.logger.debug(f'Successfully cancelled {row_count} NRs.')
        app.do_teardown_appcontext()

    except Exception as err:
        current_app.logger.error(err)
        current_app.logger.debug(f'adding {len(cancelled_nrs)} back into possible conflicts...')
        try:
            addition = NameRequestResource.add_solr_doc('possible.conflicts', cancelled_nrs)
            if addition:
                current_app.logger.debug(f'successfully added {len(cancelled_nrs)} back into possible.conflics.')
            else:
                raise Exception('Failed to add to solr possible.conflicts core')
        except Exception as err:
            current_app.logger.error(err)
            current_app.logger.error(f'Failed to add {len(cancelled_nrs)} nrs back into possible conflicts core.')
        current_app.logger.debug('rolling back db changes...')
        db.session.rollback()
        current_app.logger.debug('successfully rolled back db.')


if __name__ == '__main__':
    run_nr_garbage_collection()
