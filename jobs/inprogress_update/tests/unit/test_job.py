from datetime import datetime
from flask import current_app
import pytest
from functools import reduce
from operator import mul

from namex.models import User, State, Request

from inprogress_update import db, job

from . import EPOCH_DATETIME, FROZEN_DATETIME


def helper_create_requests(row_data):

    user = User('automation', 'automation', 'automation', 'internal', 'localhost')
    user.save_to_db()

    for row in row_data:
        print('inserting nr:{}'.format(row['nr_num']))
        if row['nr_num']:
            nr = Request()
            nr.nrNum = row['nr_num']
            nr.stateCd = row['state']
            nr.lastUpdate = row['last_update']
            nr.userId = user.id
            nr.save_to_db()


job_test_data=[
    ('update_0_row',
     [
         {'nr_num': 'NR 0000001', # NR Number of the Request to be create, or None if no prior NR is needed for the test
          'state': State.DRAFT,  # state if the existing NR
          'last_update': EPOCH_DATETIME,
          },
     ],
     0, # expected_row_count
     ),
    ('update_1_row',
     [
         {'nr_num': 'NR 6144860', 'state': State.INPROGRESS, 'last_update': EPOCH_DATETIME},
     ],
     1,
     ),
    ('update_row_2_leave_row_1_and_3',
     [
        {'nr_num': 'NR 0000001', 'state': State.DRAFT, 'last_update': EPOCH_DATETIME},
        {'nr_num': 'NR 0000002', 'state': State.INPROGRESS, 'last_update': EPOCH_DATETIME},
        {'nr_num': 'NR 0000003', 'state': State.INPROGRESS, 'last_update': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')},
     ],
     1,
    ),
    ('update_no_rows_leave_row_1_and_2',
     [
         {'nr_num': 'NR 0000001', 'state': State.DRAFT, 'last_update': EPOCH_DATETIME},
         {'nr_num': 'NR 0000002', 'state': State.INPROGRESS, 'last_update': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')},
     ],
     0,
     ),
]


@pytest.mark.parametrize("test_name, request_data, expected_row_count", job_test_data)
def test_run_job(app, session, test_name, request_data, expected_row_count):

    # setup
    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost')
    helper_create_requests(request_data)

    # Run Test
    processed, success = job(user, max_rows=100, delay=1800)

    # check expected rows processed by job
    assert processed == expected_row_count

    # check expected state of rows
    # pending = 0
    # rows = nro_connection.cursor().execute("select * from NAMEX.NAMEX_FEEDER")
    # for row in rows:
    #     if row[2] != 'C':
    #         pending += 1
    # assert pending == 0
    #
    # check for rows skipped due to errors
    # expected_errors = reduce(mul, [x['error'] for x in feeder_data])
    # errors=0
    # rows = nro_connection.cursor().execute("select * from NAMEX.NAMEX_FEEDER")
    # for row in rows:
    #     if row[7] is not None:
    #         errors += 1
    #         print('error', row[7])
    # assert errors == expected_errors

