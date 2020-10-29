"""Script used to regularly cancel test NRs."""
from flask import Flask, current_app
from namex import db
from namex.models import Request, State
from namex.utils.logging import setup_logging
from sqlalchemy import text
import pysolr
from config import get_named_config, Config
from namex import nro
import cx_Oracle


setup_logging()  # important to do this first


def create_app(environment='production'):
    """Create instance of service."""
    app = Flask(__name__)
    app.config.from_object(get_named_config(environment))
    db.init_app(app)
    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    return app

def delete_solr_doc(solr_base_url,solr_core, doc_id):
    solr = pysolr.Solr(solr_base_url + solr_core + '/', timeout=10)
    result = solr.delete(id=doc_id, commit=True)

    return result

def add_solr_doc(solr_base_url, solr_core, solr_docs):
    solr = pysolr.Solr(solr_base_url + solr_core + '/', timeout=10)
    result = solr.add(solr_docs, commit=True)

    return result


def process_SOLR_POSTGRES(r, cancelled_nrs, SOLR_URL):  
    original_state = r.stateCd
    r.stateCd = State.CANCELLED
    if r.names.all():
        try:            
            deletion = delete_solr_doc(SOLR_URL,'possible.conflicts', r.nrNum)
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



def process_POSTGRES_ORACLE(r, cancelled_nrs):  
    original_state = r.stateCd
    r.stateCd = State.CANCELLED
    if r.names.all():
        try:             
            nro.cancel_nr(r, 'nr_garbage_collector') 

            # save record
            r.save_to_db()            

        except Exception as err:
            current_app.logger.debug(err.with_traceback(None))

    db.session.add(r)


def run_nr_garbage_collection():
    """Search for stale test NRs and cancel them."""
    app = create_app()

    delay = current_app.config.get('STALE_THRESHOLD')
    max_rows = current_app.config.get('MAX_ROWS_LIMIT')
    solr_base_url = current_app.config.get('SOLR_BASE_URL', None)
    SOLR_URL = solr_base_url  + '/solr/'
    cancelled_nrs = []

    try:
        row_count = 0

        reqs = db.session.query(Request). \
            filter(Request.stateCd.in_((State.DRAFT, State.COND_RESERVE, State.RESERVED))). \
            filter(Request.lastUpdate <= text(f"(now() at time zone 'utc') - INTERVAL '{delay} SECONDS'")). \
            order_by(Request.lastUpdate.asc()). \
            limit(max_rows). \
            with_for_update().all()       
        

        for r in reqs:     
            if r.stateCd==State.DRAFT and not r.payments.all() and r._source=='NAMEREQUEST':
                # Must be cancelled in postgres, and cancelled in oracle                
                process_POSTGRES_ORACLE(r, cancelled_nrs) 
                row_count += 1
            elif r.stateCd in [State.DRAFT, State.RESERVED , State.COND_RESERVE]:            
                if r.nrNum.startswith('NR L'):
                    # Must be deleted in solr, cancelled in postgres                    
                    process_SOLR_POSTGRES(r, cancelled_nrs, SOLR_URL)       
                    row_count += 1             
                elif r.stateCd in [State.RESERVED , State.COND_RESERVE]:
                    # Must be deleted in solr, cancelled in postgres, added and cancelled in oracle                    
                    process_SOLR_POSTGRES(r, cancelled_nrs, SOLR_URL) 
                    process_POSTGRES_ORACLE(r, cancelled_nrs) 
                    row_count += 1

        # db.session.commit()
        current_app.logger.debug(f'Successfully cancelled {row_count} NRs.')
        app.do_teardown_appcontext()

    except Exception as err:
        current_app.logger.error(err)
        current_app.logger.debug(f'adding {len(cancelled_nrs)} back into possible conflicts...')
        try:
            addition = add_solr_doc(SOLR_URL,'possible.conflicts', cancelled_nrs)
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
