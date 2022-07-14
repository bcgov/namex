import sys
from datetime import datetime, timedelta

import cx_Oracle
from sqlalchemy.dialects import postgresql
from sqlalchemy import text
from flask import Flask, g, current_app

from namex.utils.logging import setup_logging
from namex.models import Request, State, User, Event
from namex.services import EventRecorder
from namex.services.name_request import NameRequestService

from config import Config
from nro.nro_datapump import nro_data_pump_update
from nro.app import create_app, db
from util.job_tracker import JobTracker

setup_logging() # important to do this first

def get_ops_params():
    try:
        delay = int(current_app.config.get('MIN_DELAY_SECONDS', 600))
    except:
        delay = 600
    try:
        max_rows = int(current_app.config.get('MAX_ROW_LIMIT', 1000))
    except:
        max_rows = 1000
    try:
        expires_days = int(current_app.config.get('EXPIRES_DAYS', 60))
    except:
        expires_days=60


    return delay, max_rows, expires_days


# #### Send the NameX Request info to NRO
# #########################################

# this allows me to use the NameX ORM Model, and use the db scoped session attached to the models.
app = create_app(Config)
delay, max_rows, expires_days = get_ops_params()

start_time = datetime.utcnow()
row_count = 0

try:
    job_id = JobTracker.start_job(db, start_time)

    # get the service account user to save BRO Requests
    user = User.find_by_username(current_app.config['NRO_SERVICE_ACCOUNT'])

    ora_con = cx_Oracle.connect(Config.ORA_USER,
                                Config.ORA_PASSWORD,
                                "{0}:{1}/{2}".format(Config.ORA_HOST, Config.ORA_PORT, Config.ORA_NAME))
    ora_con.begin()
    ora_cursor = ora_con.cursor()

    # A more generic way of setting time
    # but it doens't print / log well from the Postgres Dialect
    # so just leaving it here for future reference
    # q = q.filter(Request.lastUpdate < datetime.utcnow()-timedelta(seconds=delay)). \
    #

    q = db.session.query(Request).\
                filter(Request.stateCd.in_([State.APPROVED, State.REJECTED, State.CONDITIONAL])).\
                filter(Request.furnished != 'Y').\
                filter(Request.lastUpdate <= text('(now() at time zone \'utc\') - INTERVAL \'{delay} SECONDS\''.format(delay=delay))).\
                order_by(Request.lastUpdate.asc()). \
                limit(max_rows). \
                with_for_update()

    # leaving this debug statement here as there were some translation and image caching issues
    # that are easier to see from the raw SQL in the log
    #
    current_app.logger.debug(str(q.statement.compile(
        dialect=postgresql.dialect(),
        compile_kwargs={"literal_binds": True}))
    )

    for r in q.all():
        row_count += 1

        current_app.logger.debug('processing: {}'.format(r.nrNum))

        try:
            nr_service = NameRequestService()
            expiry_days = int(nr_service.get_expiry_days(r))

            current_app.logger.debug('r.requestTypeCd = ' + r.requestTypeCd)
            current_app.logger.debug(f'expiry days: { expires_days }')

            nro_data_pump_update(r, ora_cursor, expiry_days)
            db.session.add(r)
            EventRecorder.record(user, Event.NRO_UPDATE, r, r.json(), save_to_session=True)

            ora_con.commit()
            db.session.commit()
            JobTracker.job_detail(db, job_id, r.nrNum)

        except Exception as err:
            current_app.logger.error(err)
            current_app.logger.error('ERROR: {}'.format(r.nrNum))
            db.session.rollback()
            ora_con.rollback()
            JobTracker.job_detail_error(db, job_id, r.nrNum, str(err))

    JobTracker.end_job(db, job_id, datetime.utcnow(), 'success')

except Exception as err:
    db.session.rollback()
    if 'ora_con' in locals() and ora_con:
        ora_con.rollback()
    print('NRO Update Failed:', err, err.with_traceback(None), file=sys.stderr)
    JobTracker.end_job(db, job_id, datetime.utcnow(), 'fail')
    exit(1)

finally:
    if 'ora_con' in locals() and ora_con:
        ora_con.close()

app.do_teardown_appcontext()
end_time = datetime.utcnow()
print("job - requests processed: {0} completed in:{1}".format(row_count, end_time-start_time))
exit(0)
