from app.resources.corporations import Methods
import pytest
from sqlalchemy import text


@pytest.fixture(autouse=True)
def given(fake_names_db):
    background = [
        'drop schema if exists bc_registries cascade;',
        'create schema bc_registries;',
        """
        create table bc_registries.office_vw(
            delivery_addr_id    varchar(1),
            end_event_id        varchar(1),
            corp_num            varchar(10)
        );
        """
    ]
    for sql in background:
        fake_names_db.engine.execute(sql)


def insert(addr_id, end_event_id, corp_num):
    return text("insert into bc_registries.office_vw"
                "(delivery_addr_id, end_event_id, corp_num)"
                "values({}, {}, {})".format(
        addr_id if addr_id!=None else 'NULL',
        end_event_id if end_event_id!=None else 'NULL',
        corp_num
    ))

def test_ignores_past_addresses(app, fake_names_db):
    fake_names_db.engine.execute(insert(addr_id='1', end_event_id='1', corp_num='12345'))
    sql = Methods.build_addr_id_sql('\'12345\'')
    result = fake_names_db.engine.execute(sql).fetchall()

    assert [] == result

def test_return_current_addresses(app, fake_names_db):
    fake_names_db.engine.execute(insert(addr_id='1', end_event_id=None, corp_num='12345'))
    fake_names_db.engine.execute(insert('2', None, '12345'))
    sql = Methods.build_addr_id_sql('\'12345\'')
    result = fake_names_db.engine.execute(sql).fetchall()

    assert 2 == len(result)

def test_ignores_empty_address(app, fake_names_db):
    fake_names_db.engine.execute(insert(addr_id=None, end_event_id=None, corp_num='12345'))
    sql = Methods.build_addr_id_sql('\'12345\'')
    result = fake_names_db.engine.execute(sql).fetchall()

    assert [] == result