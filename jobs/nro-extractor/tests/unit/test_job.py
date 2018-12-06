from flask import current_app
import pytest
from functools import reduce
from operator import mul

from namex.models import User, State, Request

from extractor.app import db, update_feeder_row, job

from . import integration_oracle_namesdb


def helper_add_namex_feeder_rows(nro_connection, row_data):

    cursor = nro_connection.cursor()
    # load data
    ins_sql = """insert into NAMEX.NAMEX_FEEDER
    (ID, TRANSACTION_ID, STATUS, NR_NUM, ACTION)
    values
    ({})"""
    for data in row_data:
        cursor.execute(ins_sql.format(data['feeder']))


def helper_create_requests(row_data):

    user = User('automation', 'automation', 'automation', 'internal', 'localhost')
    user.save_to_db()

    for row in row_data:
        if row['nr_num']:
            nr = Request()
            nr.nrNum = row['nr_num']
            nr.stateCd = row['state']
            nr.userId = user.id
            nr.save_to_db()


update_feeder_row_data=[
    ([
        {'expected': True, 'nr_num': 'NR 6144860', 'feeder': "38, 38, 'P', '{nr_num}', 'C'"},
    ]),
]

@integration_oracle_namesdb
@pytest.mark.parametrize("feeder_data", update_feeder_row_data)
def test_update_feeder_row(app, nro_connection, feeder_data):

    print(feeder_data)
    helper_add_namex_feeder_rows(nro_connection, feeder_data)

    success = update_feeder_row(nro_connection
                                ,id=38
                                ,status='C'
                                ,send_count=1
                                ,error_message=None)

    assert success == feeder_data[0]['expected']


job_test_data=[
    ('success_create',
     [
         {'nr_num': None, # NR Number of the Request to be create, or None if no prior NR is needed for the test
          'state': State.DRAFT,  # state if the existing NR
          'feeder': "38, 38, 'P', 'NR 6144860', 'C'", # Feeder table data
          'error': 0}, # 0 == no error message should be logged, 1 == error messge should be logged
     ]),
    ('success_update',
     [
        {'nr_num': 'NR 6144860', 'state': State.DRAFT, 'feeder': "39, 39, 'P', 'NR 6144860', 'U'", 'error': 0},
    ]),
    ('success_create_multiple_rows',
     [
        {'nr_num': None, 'state': State.DRAFT, 'feeder': "39, 39, 'P', 'NR 5790841', 'C'", 'error': 0},
        {'nr_num': None, 'state': State.DRAFT, 'feeder': "40, 40, 'P', 'NR 6367425', 'C'", 'error': 0},
    ]),
    ('success_update_multiple_rows',
     [
         {'nr_num': 'NR 5790841', 'state': State.DRAFT, 'feeder': "39, 39, 'P', 'NR 5790841', 'U'", 'error': 0},
         {'nr_num': 'NR 6367425', 'state': State.DRAFT, 'feeder': "40, 40, 'P', 'NR 6367425', 'U'", 'error': 0},
     ]),
    ('success_cancel-draft',
     [
        {'nr_num': 'NR 9021859', 'state': State.DRAFT, 'feeder': "38, 38, 'P', 'NR 9021859', 'X'", 'error': 0},
    ]),
    ('success_cancel-inprogress',
     [
        {'nr_num': 'NR 9021859', 'state': State.INPROGRESS, 'feeder': "38, 38, 'P', 'NR 9021859', 'X'", 'error': 0},
    ]),
    ('success_cancel-hold',
     [
         {'nr_num': 'NR 9021859', 'state': State.HOLD, 'feeder': "38, 38, 'P', 'NR 9021859', 'X'", 'error': 0},
     ]),
    ('log-error_update-inprogress',
     [
         {'nr_num': 'NR 9021859', 'state': State.INPROGRESS, 'feeder': "38, 38, 'P', 'NR 9021859', 'U'", 'error': 1},
     ]),
    ('log-error_update-hold',
     [
         {'nr_num': 'NR 9021859', 'state': State.HOLD, 'feeder': "38, 38, 'P', 'NR 9021859', 'U'", 'error': 1},
     ]),
    ('log-error_update-approved',
     [
         {'nr_num': 'NR 9021859', 'state': State.APPROVED, 'feeder': "38, 38, 'P', 'NR 9021859', 'U'", 'error': 1},
     ]),
    ('log-error_update-conditional',
     [
         {'nr_num': 'NR 9021859', 'state': State.CONDITIONAL, 'feeder': "38, 38, 'P', 'NR 9021859', 'U'", 'error': 1},
     ]),
    ('log-error_update-rejected',
     [
         {'nr_num': 'NR 9021859', 'state': State.REJECTED, 'feeder': "38, 38, 'P', 'NR 9021859', 'U'", 'error': 1},
     ]),
    ('log-error_update-expired',
     [
         {'nr_num': 'NR 9021859', 'state': State.EXPIRED, 'feeder': "38, 38, 'P', 'NR 9021859', 'U'", 'error': 1},
     ]),
]


@integration_oracle_namesdb
@pytest.mark.parametrize("test_name, feeder_data", job_test_data)
def test_run_job(app, session, nro_connection, namex_feeder, test_name, feeder_data):

    # setup
    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost')
    helper_add_namex_feeder_rows(nro_connection, feeder_data)
    helper_create_requests(feeder_data)

    # Run Test
    processed = job(app, db, nro_connection, user, 100)

    # check expected rows processed by job
    assert processed == len(feeder_data)

    # check expected state of rows
    pending = 0
    rows = nro_connection.cursor().execute("select * from NAMEX.NAMEX_FEEDER")
    for row in rows:
        if row[2] != 'C':
            pending += 1
    assert pending == 0

    # check for rows skipped due to errors
    expected_errors = reduce(mul, [x['error'] for x in feeder_data])
    errors=0
    rows = nro_connection.cursor().execute("select * from NAMEX.NAMEX_FEEDER")
    for row in rows:
        if row[7] is not None:
            errors += 1
            print('error', row[7])
    assert errors == expected_errors

