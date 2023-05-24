""" NRO Extractor moves changes from the NamesDB to the new NameX system."""
import sys
from datetime import datetime
import os.path
from flask import current_app

from namex.utils.logging import setup_logging
from namex.models import User

from config import Config
from extractor.app import create_app, db, nro, job

setup_logging() # important to do this first


def get_ops_params():
    """Return the maximum number of rows to process in this job run."""
    try:
        max_rows = int(current_app.config.get('MAX_ROW_LIMIT', 100))  # pylint: disable=W0621
    except:  # pylint: disable=W0702
        max_rows = 100

    return max_rows


def job_runner():
    """NRO extractor job runner, checks if an instnace of the job is already running via /mutex/file"""
    start_time = datetime.utcnow()
    mutex_file = '/mutex/file'
    if not os.path.isfile(mutex_file):
        with open(mutex_file, mode='a'):
            pass
        print('nro-extractor: starting job: {}'.format(start_time))

        # setup Flask, push a context, initialize db & nro connections
        app = create_app(Config)

        # get the service account user to save Requests
        user = User.find_by_username(current_app.config['NRO_SERVICE_ACCOUNT'])
        max_rows = get_ops_params()
        processed = 0

        # run the job
        processed = job(app, db, nro.connection, user, max_rows)

        # clean up
        app.do_teardown_appcontext()
        end_time = datetime.utcnow()

        os.remove(mutex_file)

        # report out
        if processed < 0:
            print("nro-extractor: errored out: no rows process; completed in:{}".format(end_time - start_time)
                ,file=sys.stderr)
            sys.exit(1)

        print("nro-extractor: finished - requests processed: {0} completed in:{1}".format(processed, end_time-start_time),
            file=sys.stderr)
        nro.connection.close()
        sys.exit(0)
    else:
        print('previous job still running')
        sys.exit(0)


if __name__ == "__main__":
    job_runner()
