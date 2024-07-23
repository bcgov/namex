"""Script used to regularly cancel test NRs."""
from flask import Flask, current_app
from namex import db
from namex.models import Request, State
from namex.resources.name_requests.abstract_solr_resource import AbstractSolrResource
from namex.utils.logging import setup_logging
from sqlalchemy import and_, or_, text

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


def delete_from_solr(request, original_state: str, cancelled_nrs: list) -> list:
    """Delete doc from solr core."""
    if request.names.all():
        try:
            current_app.logger.debug('          -- deleted from solr')
            deletion = AbstractSolrResource.delete_solr_doc('possible.conflicts', request.nrNum)
            if deletion:
                cancelled_nrs.append(
                    {
                        'id': request.nrNum,
                        'name': request.names[0].name,
                        'source': 'NR',
                        'start_date': request.submittedDate.strftime('%Y-%m-%dT%H:%M:00Z')
                    }
                )
                current_app.logger.debug(' -- deleted from solr')
            else:
                raise Exception(f'Failed to delete {request.nrNum} from solr possible.conflicts core')
        except Exception as err:
            current_app.logger.error(err)
            current_app.logger.debug(f'setting {request.nrNum} back to original state...')
            request.stateCd = original_state

    return cancelled_nrs


def run_nr_garbage_collection():
    """Search for stale test NRs and cancel them."""
    app = create_app()

    delay = current_app.config.get('STALE_THRESHOLD')
    max_rows = current_app.config.get('MAX_ROWS_LIMIT')
    cancelled_nrs = []

    try:
        reqs = db.session.query(Request). \
            filter(or_(Request.stateCd.in_((State.COND_RESERVE, State.RESERVED)),
                       and_(Request.stateCd == State.DRAFT, or_(Request._source == 'NAMEREQUEST',
                            Request.nrNum.contains('NR L'))))). \
            filter(Request.lastUpdate <= text(f"(now() at time zone 'utc') - INTERVAL '{delay} SECONDS'")). \
            order_by(Request.lastUpdate.asc()). \
            limit(max_rows). \
            with_for_update().all()

        row_count = 0
        for r in reqs:
            ignore_nr = False
            if r.payments:
                # only cancel this NR if there is a payment_status_code=CREATED and payment_completion_date
                for payment in r.payments:
                    if payment.payment_status_code != 'CREATED' or not payment.payment_completion_date:
                        # skip this NR
                        ignore_nr = True
                    else:
                        # if there are any payments that fit this criteria, cancel it
                        ignore_nr = False
                        break
            if not ignore_nr:
                current_app.logger.debug(f'Cancelling {r.nrNum}...')
                original_state = r.stateCd
                r.stateCd = State.CANCELLED
                current_app.logger.debug(' -- cancelled in postgres')

                # all cases are deleted from solr and cancelled in postgres
                cancelled_nrs = delete_from_solr(r, original_state, cancelled_nrs)
                db.session.add(r)
                row_count += 1

        db.session.commit()
        current_app.logger.debug(f'Successfully cancelled {row_count} NRs.')
        app.do_teardown_appcontext()

    except Exception as err:
        current_app.logger.error(err)
        current_app.logger.debug(f'adding {len(cancelled_nrs)} back into possible conflicts...')
        try:
            addition = AbstractSolrResource.add_solr_doc('possible.conflicts', cancelled_nrs)
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
