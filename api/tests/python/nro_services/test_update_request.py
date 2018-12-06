import cx_Oracle
from namex import nro
from tests.python import integration_oracle_namesdb, integration_oracle_local_namesdb
from namex.services.nro.change_nr import _update_request


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
