import cx_Oracle
from namex import nro
from tests.python import integration_oracle_namesdb, integration_oracle_local_namesdb
from namex.services.nro.change_nr import _update_request, _cancel_nro_transaction


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
