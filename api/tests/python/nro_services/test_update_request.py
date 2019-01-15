import cx_Oracle
from namex import nro
from namex.models import User
from tests.python import integration_oracle_namesdb, integration_oracle_local_namesdb
from namex.services.nro.change_nr import \
    _update_request, \
    _get_event_id, \
    _create_nro_transaction, \
    _update_nro_request_state


@integration_oracle_namesdb
def test_nro_connection(app):

    conn = nro.connection
    assert type(conn) is cx_Oracle.Connection


class FakeRequest:
    requestId = '42'
    previousRequestId = '15'


@integration_oracle_namesdb
@integration_oracle_local_namesdb
def test_preserves_previous_request_id(app):
    con = nro.connection
    cursor = con.cursor()
    cursor.execute("""
        declare exist number;
        begin
            select count(1) into exist from user_tables where table_name='REQUEST';
            if exist = 1 then
                execute immediate 'drop table request';
            end if;
        end;        
    """)
    cursor.execute('create table request (request_id varchar(10), previous_request_id varchar(10))')
    cursor.execute("insert into request(request_id, previous_request_id) values('42', '99')")
    _update_request(cursor, FakeRequest(), None, {
        'is_changed__request': False,
        'is_changed__previous_request': True
    })

    cursor.execute("select previous_request_id from request")
    (value,) = cursor.fetchone()

    assert '99' == value


@integration_oracle_namesdb
def test_create_nro_transaction(app):
    con = nro.connection
    cursor = con.cursor()

    eid = _get_event_id(cursor)

    fake_request = FakeRequest()
    fake_request.requestId = 884047

    _create_nro_transaction(cursor, fake_request, eid)

    cursor.execute("select event_id, transaction_type_cd from transaction where request_id = {} order by event_id desc".format(fake_request.requestId))
    (value, transaction_type_cd) = cursor.fetchone()

    assert eid == value
    assert value != 0
    assert value != None
    assert transaction_type_cd == 'ADMIN'

@integration_oracle_namesdb
def test_create_nro_transaction_with_type(app):
    con = nro.connection
    cursor = con.cursor()

    eid = _get_event_id(cursor)

    fake_request = FakeRequest()
    fake_request.requestId = 884047

    _create_nro_transaction(cursor, fake_request, eid, 'CORRT')

    cursor.execute("select event_id, transaction_type_cd from transaction where request_id = {} order by event_id desc".format(fake_request.requestId))
    (value, transaction_type_cd) = cursor.fetchone()

    assert eid == value
    assert transaction_type_cd == 'CORRT'


@integration_oracle_namesdb
def test_update_nro_request_state_to_draft(app):
    con = nro.connection
    cursor = con.cursor()

    eid = _get_event_id(cursor)

    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost')

    fake_request = FakeRequest()
    fake_request.requestId = 884047
    fake_request.stateCd = 'DRAFT'
    fake_request.activeUser = user

    _update_nro_request_state(cursor, fake_request, eid, {'is_changed__request_state': True})

    cursor.execute("select state_type_cd from request_state where request_id = {} and start_event_id = {}"
                   .format(fake_request.requestId, eid))
    (state_type_cd,) = cursor.fetchone()

    assert state_type_cd == 'D'


@integration_oracle_namesdb
def test_update_nro_request_state_to_approved(app):
    """
    Code should not allow us to set state to anything except Draft
    """
    con = nro.connection
    cursor = con.cursor()

    eid = _get_event_id(cursor)

    user = User('idir/bob', 'bob', 'last', 'idir', 'localhost')

    fake_request = FakeRequest()
    fake_request.requestId = 884047
    fake_request.stateCd = 'APPROVED'
    fake_request.activeUser = user

    _update_nro_request_state(cursor, fake_request, eid, {'is_changed__request_state': True})

    cursor.execute("select state_type_cd from request_state where request_id = {} and start_event_id = {}"
                   .format(fake_request.requestId, eid))
    resultset = cursor.fetchone()

    assert resultset is None
