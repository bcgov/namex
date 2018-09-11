from namex.utils.logging import setup_logging
setup_logging() ## important to do this first

from sqlalchemy.dialects import postgresql
from nro.nro_datapump import nro_data_pump_update
from datetime import datetime, timedelta
import cx_Oracle
import sys
from flask import Flask, g, current_app
from config import Config
from namex import db
from namex.models import Request, State
from util.job_tracker import JobTracker


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        ''' Enable Flask to automatically remove database sessions at the
         end of the request or when the application shuts down.
         Ref: http://flask.pocoo.org/docs/patterns/sqlalchemy/
        '''
        current_app.logger.debug('Tearing down the Flask App and the App Context')
        if hasattr(g, 'ora_conn'):
            g.ora_conn.close()

    return app


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

    ora_con = cx_Oracle.connect(Config.ORA_USER,
                                Config.ORA_PASSWORD,
                                "{0}:{1}/{2}".format(Config.ORA_HOST, Config.ORA_PORT, Config.ORA_NAME))
    ora_con.begin()
    ora_cursor = ora_con.cursor()

    q = db.session.query(Request).\
                filter(Request.stateCd.in_([State.APPROVED, State.REJECTED, State.CONDITIONAL])).\
                filter(Request.furnished != 'Y')

    current_app.logger.debug(str(q.statement.compile(
                              dialect=postgresql.dialect(),
                              compile_kwargs={"literal_binds": True}))
                            )

    q = q.filter(Request.lastUpdate < datetime.utcnow()-timedelta(seconds=delay)). \
        order_by(Request.lastUpdate.asc()). \
        limit(max_rows). \
        with_for_update()\

    current_app.logger.debug(str(q.statement.compile(
        dialect=postgresql.dialect(),
        compile_kwargs={"literal_binds": True}))
    )

    reqs = q.all()

    for r in reqs:
        row_count += 1
        JobTracker.job_detail(db, job_id, r.nrNum)

        current_app.logger.debug('processing: {}'.format(r.nrNum))

        nro_data_pump_update(r, ora_cursor, expires_days)
        db.session.add(r)

    db.session.commit()
    ora_con.commit()

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
