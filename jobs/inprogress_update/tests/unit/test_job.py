"""This is test job."""
import uuid
from datetime import datetime, timezone

import pytest
from namex.models import Request, State, User

from inprogress_update import inprogress_update

from . import EPOCH_DATETIME


def helper_create_requests(row_data):
    from namex.models import Event, Request, db

    # collect NR numbers we’re about to insert
    nr_nums = [row['nr_num'] for row in row_data if row['nr_num']]

    if nr_nums:
        # find existing request IDs for these NR numbers
        req_ids = [r.id for r in db.session.query(Request.id).filter(Request.nrNum.in_(nr_nums)).all()]

        if req_ids:
            # delete dependent events first
            db.session.query(Event).filter(Event.nrId.in_(req_ids)).delete(synchronize_session=False)

        # delete requests
        db.session.query(Request).filter(Request.nrNum.in_(nr_nums)).delete(synchronize_session=False)

        db.session.commit()

    # Create a user for ownership
    unique_sub = f'idir_{uuid.uuid4()}'[:36]
    unique_idp_userid = f'idp_{uuid.uuid4()}'[:36]
    user = User(
        username='idir/bob',
        firstname='bob',
        lastname='last',
        sub=unique_sub,
        iss='localhost',
        idp_userid=unique_idp_userid,
        login_source='login_source_value'
    )
    user.save_to_db()

    # Insert fresh requests
    for row in row_data:
        if row['nr_num']:
            req = Request()
            req.nrNum = row['nr_num']
            req.stateCd = row['state']
            req.lastUpdate = row['last_update']
            req.userId = user.id
            req.save_to_db()



job_test_data = [
    (
        'update_0_row',
        [
            {
                'nr_num': 'NR 1000002',
                # NR Number of the Request to be create, or None if no prior NR is needed for the test
                'state': State.DRAFT,  # state if the existing NR
                'last_update': EPOCH_DATETIME,
            },
        ],
        0,  # expected_row_count
    ),
    (
        'update_1_row',
        [
            {'nr_num': 'NR 1000003', 'state': State.INPROGRESS, 'last_update': EPOCH_DATETIME},
        ],
        1,
    ),
    (
        'update_row_2_leave_row_1_and_3',
        [
            {'nr_num': 'NR 1000004', 'state': State.DRAFT, 'last_update': EPOCH_DATETIME},
            {'nr_num': 'NR 1000005', 'state': State.INPROGRESS, 'last_update': EPOCH_DATETIME},
            {
                'nr_num': 'NR 1000006',
                'state': State.INPROGRESS,
                'last_update': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f'),
            },
        ],
        1,
    ),
    (
        'update_no_rows_leave_row_1_and_2',
        [
            {'nr_num': 'NR 1000007', 'state': State.DRAFT, 'last_update': EPOCH_DATETIME},
            {
                'nr_num': 'NR 1000008',
                'state': State.INPROGRESS,
                'last_update': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f'),
            },
        ],
        0,
    ),
    (
        'update_2_rows',
        [
            {'nr_num': 'NR 1000009', 'state': State.INPROGRESS, 'last_update': EPOCH_DATETIME},
            {'nr_num': 'NR 1000010', 'state': State.INPROGRESS, 'last_update': EPOCH_DATETIME},
        ],
        2,
    ),
]


@pytest.mark.parametrize('test_name, request_data, expected_row_count', job_test_data)
def test_run_job(app, session, test_name, request_data, expected_row_count):
    # setup
    unique_sub = f'idir_{uuid.uuid4()}'[:36]
    unique_idp_userid = f'idp_{uuid.uuid4()}'[:36]
    user = User(
        'idir/bob',
        'bob',
        'last',
        unique_sub,
        'localhost',
        unique_idp_userid,
        'login_source_value'
    )
    helper_create_requests(request_data)

    # Run Test
    processed, success = inprogress_update(
        user,
        max_rows=100,
        client_delay=1800,
        examine_delay=1800
    )

    # check expected rows processed by job
    assert processed == expected_row_count
