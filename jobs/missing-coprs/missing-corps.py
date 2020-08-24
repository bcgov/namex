import sys
from datetime import datetime

from flask import current_app

from namex.utils.logging import setup_logging

from config import Config
from corps.app import create_app, db, nro, job


setup_logging() # important to do this first


def get_ops_params():
    try:
        max_rows = int(current_app.config.get('MAX_ROW_LIMIT', 100))
    except:
        max_rows = 100

    return max_rows


if __name__ == "__main__":
    start_time = datetime.utcnow()
    print('missing corps sync: starting job: {}'.format(start_time))

    # setup Flask, push a context, initialize db & nro connections
    app = create_app(Config)

    max_rows = get_ops_params()
    processed = 0

    # run the job
    processed = job(app, db, nro.connection,max_rows)

    # clean up
    app.do_teardown_appcontext()
    end_time = datetime.utcnow()

    # report out
    if processed < 0:
        print("missing corp sync: errored out: no rows process; completed in:{}".format(end_time - start_time)
              ,file=sys.stderr)
        exit(1)

    print("missing corp sync: finished - requests processed: {0} completed in:{1}".format(processed, end_time-start_time),
          file=sys.stderr)
    exit(0)
