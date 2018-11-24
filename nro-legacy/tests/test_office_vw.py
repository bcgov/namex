import os
import pytest
from hamcrest import *
from .postgres import Postgres

release = 'sql/release/201811XX_namex/registry/namex/'
migration = 'create.sql'


def sut():
    content = open(release + migration).read()
    target = content[content.find('@') + 1:]
    return open(release + target.strip(), 'r').read()


def extract_select():
    source = sut()
    sql = source[source.find('AS') + 2:]
    return sql[:sql.find(';')]


def test_sut_can_be_reached():
    assert_that(sut(), contains_string('VIEW namex.office_vw'))


def test_environment_ready():
    assert_that(os.getenv('PGDATABASE'), is_not(None))
    assert_that(os.getenv('PGUSER'), is_not(None))
    assert_that(os.getenv('PGPASSWORD'), is_not(None))


@pytest.fixture(autouse=True)
def before_each():
    Postgres().execute(open('tests/sql/create.table.office.sql').read())


def test_select_current_addresses():
    Postgres().execute("""
        insert into office(
            corp_num, 
            office_typ_cd, 
            start_event_id, 
            end_event_id, 
            mailing_addr_id, 
            delivery_addr_id,
            dd_corp_num, 
            email_address
        )
        values ('1', '1', '1', '1', '1', '1', '1', '1')
    """)
    Postgres().execute("""
            insert into office(
                corp_num, 
                office_typ_cd, 
                start_event_id, 
                end_event_id, 
                mailing_addr_id, 
                delivery_addr_id,
                dd_corp_num, 
                email_address
            )
            values ('2', '2', '2', '2', '2', '2', '2', '2')
        """)
    result = Postgres().select(extract_select())

    assert_that(len(result), equal_to(2))

