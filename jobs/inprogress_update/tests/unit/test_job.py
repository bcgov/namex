"""This is test job."""
import pytest
import inprogress_update

from . import EPOCH_DATETIME
from datetime import datetime
from namex.models import Request, State, User


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


job_test_data = [
    ('update_0_row',
     [
         {'nr_num': 'NR 1000002',
          # NR Number of the Request to be create, or None if no prior NR is needed for the test
          'state': State.DRAFT,  # state if the existing NR
          'last_update': EPOCH_DATETIME,
          },
     ],
     0,  # expected_row_count
     ),
    ('update_1_row',
     [
         {'nr_num': 'NR 1000003', 'state': State.INPROGRESS, 'last_update': EPOCH_DATETIME},
     ],
     1,
     ),
    ('update_row_2_leave_row_1_and_3',
     [
        {'nr_num': 'NR 1000004', 'state': State.DRAFT, 'last_update': EPOCH_DATETIME},
        {'nr_num': 'NR 1000005', 'state': State.INPROGRESS, 'last_update': EPOCH_DATETIME},
        {'nr_num': 'NR 1000006', 'state': State.INPROGRESS, 'last_update': \
            datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')},
     ],
     1,
     ),
    ('update_no_rows_leave_row_1_and_2',
     [
         {'nr_num': 'NR 1000007', 'state': State.DRAFT, 'last_update': EPOCH_DATETIME},
         {'nr_num': 'NR 1000008', 'state': State.INPROGRESS, \
             'last_update': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')},
     ],
     0,
     ),
    ('update_2_rows',
     [
         {'nr_num': 'NR 1000009', 'state': State.NRO_UPDATING, 'last_update': EPOCH_DATETIME},
         {'nr_num': 'NR 1000010', 'state': State.NRO_UPDATING, \
             'last_update': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')},
     ],
     2,
     ),
]


@pytest.mark.parametrize("test_name, request_data, expected_row_count", job_test_data)
def test_run_job(app, session, test_name, request_data, expected_row_count):

    # setup
    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost')
    helper_create_requests(request_data)

    # Run Test
    processed, success = inprogress_update.inprogress_update(user, max_rows=100, client_delay=1800, examine_delay=1800)

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