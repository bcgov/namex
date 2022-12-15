from datetime import datetime
import os
import logging

import cx_Oracle
import pytest

from namex import nro
from namex.models import User, Request, State

from tests.python import integration_oracle_namesdb, EPOCH_DATETIME


@integration_oracle_namesdb
def test_nro_connection_type(app):

    conn = nro.connection
    assert type(conn) is cx_Oracle.Connection


@integration_oracle_namesdb
def test_get_last_modified_timestamp(app):

    ts = nro.get_last_update_timestamp(1205761)
    assert type(ts) is datetime


@integration_oracle_namesdb
def test_set_status_2_h(app):
    nro.set_request_status_to_h('NR 5970035', 'anyname')


nro_request_fetch_test_data = [
    (
        'NR 5970035', 'NR 5970035'
    ),
    (
        'NR 0000000', 'NR 0000000'
    ),
    (
        'NR 0000039', 'NR 0000039'
    ),
    (
        'NR 9999999', None
    ),
]

@integration_oracle_namesdb
@pytest.mark.parametrize("nr_num, expected_nr_num", nro_request_fetch_test_data)
def test_fetch_nro_request_and_copy_to_namex_request(app, session, nr_num, expected_nr_num):

    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost', '123', 'IDIR')
    nr = nro.fetch_nro_request_and_copy_to_namex_request(user, nr_number=nr_num)

    assert expected_nr_num == None if (expected_nr_num is None) else nr.nrNum


@integration_oracle_namesdb
@pytest.mark.parametrize("nr_num, expected_nr_num", nro_request_fetch_test_data)
def test_fetch_nro_request_and_copy_to_namex_request_with_nr(app, session, nr_num, expected_nr_num):

    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost', '123', 'IDIR')
    user.save_to_db()
    nr = Request()
    nr.nrNum = nr_num
    nr.userId = user.id
    nr.save_to_db()

    nr = nro.fetch_nro_request_and_copy_to_namex_request(user, nr_number=12, name_request=nr)

    assert expected_nr_num == None if (expected_nr_num is None) else nr.nrNum


nro_request_move_nr_test_data = [
    (
        'NR 5970035', 'NR 5970035'
    ),
    (
        'NR 0000000', 'NR 0000000'
    ),
]


@integration_oracle_namesdb
@pytest.mark.parametrize("nr_num, expected_nr_num", nro_request_move_nr_test_data)
def test_move_control_of_request_from_nro(app, session, nr_num, expected_nr_num):

    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost', '123', 'IDIR')
    user.save_to_db()
    nr = Request()
    nr.nrNum = nr_num
    nr.stateCd = State.INPROGRESS
    nr.nroLastUpdate = EPOCH_DATETIME
    nr.userId = user.id
    nr.save_to_db()

    warnings = nro.move_control_of_request_from_nro(nr, user)

    assert expected_nr_num == None if (expected_nr_num is None) else nr.nrNum
    assert warnings is None


def test_move_control_of_request_from_nro_missing_nr(app, session):

    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost', '123', 'IDIR')
    nr = None

    warnings = nro.move_control_of_request_from_nro(nr, user)

    assert warnings is not None

def test_move_control_of_existing_request_from_nro_missing_nr(app, session):

    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost', '123', 'IDIR')
    user.save_to_db()
    nr = Request()
    nr.nrNum = 'NR 9999999'
    nr.stateCd = State.INPROGRESS
    nr.nroLastUpdate = EPOCH_DATETIME
    nr.userId = user.id
    nr.save_to_db()

    warnings = nro.move_control_of_request_from_nro(nr, user)

    assert warnings is not None


@integration_oracle_namesdb
def test_get_nr_header(app):
    from namex.services.nro.request_utils import get_nr_header

    conn = nro.connection.cursor()
    nr_header = get_nr_header(conn, 'NR 5970035')

    assert 'NR 5970035' == nr_header['nr_num']


@integration_oracle_namesdb
def test_get_nr_submitter(app):
    from namex.services.nro.request_utils import get_nr_submitter

    conn = nro.connection.cursor()
    nr_submitter = get_nr_submitter(conn, 1456179)

    assert nr_submitter['submitted_date'] is not None


@integration_oracle_namesdb
def test_get_nr_requester(app):
    from namex.services.nro.request_utils import get_nr_requester

    conn = nro.connection.cursor()
    nr_requester = get_nr_requester(conn, 1456179)

    assert 1456179 == nr_requester['request_id']


@integration_oracle_namesdb
def test_get_exam_comments(app):
    from namex.services.nro.request_utils import get_exam_comments

    conn = nro.connection.cursor()
    exam_comments = get_exam_comments(conn, 54453)

    assert 2 == len(exam_comments)


@integration_oracle_namesdb
def test_get_nwpta(app):
    from namex.services.nro.request_utils import get_nwpta

    conn = nro.connection.cursor()
    nwpta = get_nwpta(conn, 884047)

    assert 1 == len(nwpta)
    assert 'AB' == nwpta[0]['partner_jurisdiction_type_cd']


nro_names_test_data = [
    (
        884047, 1, ['KHAY E & I SERVICES INC.']
    ),
    (
        0, 0, []
    ),
]


@integration_oracle_namesdb
@pytest.mark.parametrize("request_id, expected_length, expected_names", nro_names_test_data)
def test_get_names(app, request_id, expected_length, expected_names):
    from namex.services.nro.request_utils import get_names

    conn = nro.connection.cursor()
    names = get_names(conn, request_id)

    assert expected_length == 0 if (names is None) else len(names)

    if expected_length is not 0:
        name_found = False
        for name in names:
            for n in expected_names:
                if n == name['name']:
                    name_found = True
            assert name_found
