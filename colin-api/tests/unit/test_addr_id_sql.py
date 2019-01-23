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
        create table bc_registries.address_vw(
            addr_id varchar(1),
            addr_line_1 varchar(20),
            addr_line_2 varchar(20),
            addr_line_3 varchar(20),
            city varchar(20),
            province varchar(3),
            country_typ_cd varchar(3) NULL,
            postal_cd varchar(7)
        );
        create table bc_registries.corp_jurs_vw(
            home_jurisdiction varchar(10),
            corp_num varchar(10)
        );
        create table bc_registries.corp_party_vw(
            first_nme varchar(10),
            middle_nme varchar(10),
            last_nme varchar(20),
            party_typ_cd varchar(3),
            end_event_id varchar(1),
            corp_num varchar(10)
        );
        """
    ]
    for sql in background:
        fake_names_db.engine.execute(sql)

def insert_office(delivery_addr_id, end_event_id, corp_num):
    return text("insert into bc_registries.office_vw"
                "(delivery_addr_id, end_event_id, corp_num)"
                "values({}, {}, {})".format(
        delivery_addr_id if delivery_addr_id!=None else 'NULL',
        end_event_id if end_event_id!=None else 'NULL',
        corp_num
    ))

def insert_address(addr_id, addr_line_1, addr_line_2, addr_line_3, city, province, country_typ_cd, postal_cd):
    return text("insert into bc_registries.address_vw"
                "(addr_id, addr_line_1, addr_line_2, addr_line_3, city, province, country_typ_cd, postal_cd)"
                "values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(addr_id, addr_line_1, addr_line_2, addr_line_3, city, province, country_typ_cd, postal_cd)
                )



def insert_person(first_nme, last_nme, party_typ_cd, corp_num):
    return text("insert into bc_registries.corp_party_vw"
                "(first_nme, last_nme, party_typ_cd, corp_num)"
                 "values ('{}','{}', '{}', '{}')".format(first_nme, last_nme, party_typ_cd, corp_num)
                )


def insert_jurisdiction(home_jurisdiction, corp_num):
    return text("insert into bc_registries.corp_jurs_vw"
                "(home_jurisdiction, corp_num)"
                "values('{}','{}')".format(home_jurisdiction, corp_num))


def test_ignores_past_addresses(app, fake_names_db):
    fake_names_db.engine.execute(insert_office(delivery_addr_id='1', end_event_id='1', corp_num='12345'))
    sql = Methods.build_addr_id_sql('\'12345\'')
    result = fake_names_db.engine.execute(sql).fetchall()
    assert [] == result

def test_return_current_addresses(app, fake_names_db):
    fake_names_db.engine.execute(insert_office(delivery_addr_id='1', end_event_id=None, corp_num='12345'))
    fake_names_db.engine.execute(insert_office('2', None, '12345'))
    sql = Methods.build_addr_id_sql('\'12345\'')
    result = fake_names_db.engine.execute(sql).fetchall()
    assert 2 == len(result)

def test_ignores_empty_address(app, fake_names_db):
    fake_names_db.engine.execute(insert_office(delivery_addr_id=None, end_event_id=None, corp_num='12345'))
    sql = Methods.build_addr_id_sql('\'12345\'')
    result = fake_names_db.engine.execute(sql).fetchall()
    assert [] == result


def test_xpro_current_addresses(app, fake_names_db):
    fake_names_db.engine.execute(insert_office('3', None, '12346'))
    fake_names_db.engine.execute(insert_office('4','5','12346' ))
    fake_names_db.engine.execute(insert_address(addr_id='3', addr_line_1='539 Oak Street', addr_line_2='Suite 19',
                                               addr_line_3='RR 2', city='Victoria', province='BC', country_typ_cd='CA',
                                               postal_cd='V9E 2A1'))
    fake_names_db.engine.execute(insert_address(addr_id='4', addr_line_1='555 Fisher Street', addr_line_2='Suite 19',
                                                addr_line_3='RR 2', city='Victoria', province='BC', country_typ_cd='CA',
                                                postal_cd='V9E 2A1'))
    fake_names_db.engine.execute(insert_person(first_nme='Joe', last_nme='Smith', party_typ_cd='ATT', corp_num='12346'))
    fake_names_db.engine.execute(insert_jurisdiction(home_jurisdiction='ON', corp_num='12346'))

    office_sql = Methods.build_addr_id_sql('\'12346\'')
    jurisdiction_sql = Methods.build_jurisdiction_sql('\'12346\'')
    attorney_sql = Methods.build_attorneys_sql('\'12346\'')

    assert office_sql is not None
    assert jurisdiction_sql is not None
    attorney_sql is not None

    office_result = fake_names_db.engine.execute(office_sql).fetchall()
    assert 1 == len(office_result)

    head_office_obj, attorneys_obj, jurisdiction_obj = Methods.xpro_get_objs(office_sql, attorney_sql, jurisdiction_sql)

    assert head_office_obj is not None
    assert attorneys_obj is not None
    assert jurisdiction_obj is not None

    head_office_results = head_office_obj.fetchall()
    attorney_results = attorneys_obj.fetchall()

    assert 1 == len(head_office_results)
    assert 1 == len(attorney_results)

def test_bc_corp_current_addresses(app, fake_names_db):
    fake_names_db.engine.execute(insert_office('6', None, '121212'))
    fake_names_db.engine.execute(insert_office('7',None,'121212' ))
    fake_names_db.engine.execute(insert_office('8','9','121212' ))
    fake_names_db.engine.execute(insert_address(addr_id='6', addr_line_1='6767 Reg Drive', addr_line_2='Suite 19',
                                                addr_line_3='RR 2', city='Victoria', province='BC', country_typ_cd='CA',
                                                postal_cd='V9E 2A1'))
    fake_names_db.engine.execute(insert_address(addr_id='7', addr_line_1='12 Rec Drive', addr_line_2='Suite 19',
                                            addr_line_3='RR 2', city='Victoria', province='BC', country_typ_cd='CA',
                                            postal_cd='V9E 2A1'))


    office_sql = Methods.build_addr_id_sql('\'121212\'')
    office_result = fake_names_db.engine.execute(office_sql).fetchall()
    assert 2 == len(office_result)

    registered_addr_obj, records_addr_obj = Methods.bc_get_objs(office_sql)
    registered_address_results = registered_addr_obj.fetchall()
    records_address_results =  records_addr_obj.fetchall()

    assert 1 == len(registered_address_results)
    assert 1 == len(records_address_results)



