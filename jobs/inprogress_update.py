from namex.utils.logging import setup_logging
setup_logging() ## important to do this first

from datetime import datetime, timedelta
import sys
from flask import Flask, g, current_app
from config import Config
from namex import db
from namex.models import Request, State
from sqlalchemy import text


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    # probably don't need this since not connecting to oracle
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
        delay = int(current_app.config.get('MIN_DELAY_SECONDS', 1800))
    except:
        delay = 1800
    try:
        max_rows = int(current_app.config.get('MAX_ROW_LIMIT', 100))
    except:
        max_rows = 100
    try:
        expires_days = int(current_app.config.get('EXPIRES_DAYS', 60))
    except:
        expires_days=60


    return delay, max_rows, expires_days


app = create_app(Config)
delay, max_rows, expires_days = get_ops_params()

start_time = datetime.utcnow()
row_count = 0

try:
    reqs = db.session.query(Request).\
                filter(Request.stateCd == State.INPROGRESS). \
                filter(Request.lastUpdate <= text('NOW() - INTERVAL \'{delay} SECONDS\''.format(delay=delay))). \
            order_by(Request.lastUpdate.asc()).\
                limit(max_rows).\
                with_for_update().all()

    for r in reqs:
        row_count += 1

        current_app.logger.debug('processing: {}'.format(r.nrNum))

        r.stateCd = State.HOLD
        db.session.add(r)

    db.session.commit()

except Exception as err:
    db.session.rollback()
    print('Failed to move timed out INPROGRESS NRs to HOLD: ', err, err.with_traceback(None), file=sys.stderr)
    exit(1)

app.do_teardown_appcontext()
end_time = datetime.utcnow()
print("job - requests processed: {0} completed in:{1}".format(row_count, end_time-start_time))
exit(0)
