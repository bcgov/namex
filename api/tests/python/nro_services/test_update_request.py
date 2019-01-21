import cx_Oracle
from namex import nro
from namex.models import User
from tests.python import integration_oracle_namesdb, integration_oracle_local_namesdb
from namex.services.nro.change_nr import \
    _update_request, \
    _get_event_id, \
    _create_nro_transaction, \
    _update_nro_request_state, \
    _cancel_nro_transaction


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


@integration_oracle_local_namesdb
def test_create_cancel_nro_transaction(app):
    con = nro.connection
    cursor = con.cursor()

    cursor.execute("BEGIN EXECUTE IMMEDIATE 'DROP TABLE transaction'; EXCEPTION WHEN OTHERS THEN "
                   "IF SQLCODE != -942 THEN NULL; END IF; END;")
    cursor.execute("BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE transaction_seq'; EXCEPTION WHEN OTHERS THEN "
                   "IF SQLCODE != -942 THEN NULL; END IF; END;")

    cursor.execute('create sequence transaction_seq minvalue 1 maxvalue 9999999999 increment by 1 start with 1')
    cursor.execute('create table transaction (transaction_id number(10), request_id varchar2(10), '
                   'transaction_type_cd varchar2(10), event_id number(10),staff_idir varchar2(8))')
    _cancel_nro_transaction(cursor, FakeRequest(), None)

    cursor.execute("select transaction_type_cd from transaction")
    (value,) = cursor.fetchone()

    cursor.execute("BEGIN EXECUTE IMMEDIATE 'DROP TABLE transaction'; EXCEPTION WHEN OTHERS THEN "
                   "IF SQLCODE != -942 THEN NULL; END IF; END;")
    cursor.execute("BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE transaction_seq'; EXCEPTION WHEN OTHERS THEN "
                   "IF SQLCODE != -942 THEN NULL; END IF; END;")

    assert 'CANCL' == value
