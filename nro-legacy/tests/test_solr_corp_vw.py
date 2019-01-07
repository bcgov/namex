import os
import pytest
from hamcrest import *
from .postgres import Postgres
from .seeds import *

release = 'sql/release/201901XX_solr_view/registry/namex/'
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
    assert_that(sut(), contains_string('VIEW namex.solr_dataimport_conflicts_vw'))


def test_environment_ready():
    assert_that(os.getenv('COLIN_DATABASE'), is_not(None))
    assert_that(os.getenv('COLIN_USER'), is_not(None))
    assert_that(os.getenv('COLIN_PASSWORD'), is_not(None))


@pytest.fixture(autouse=True)
def before_each_test():
    Postgres().execute(open('tests/sql/create.table.corporation.sql').read())
    Postgres().execute(open('tests/sql/create.table.corp.state.sql').read())
    Postgres().execute(open('tests/sql/create.table.corp.name.sql').read())
    Postgres().execute(open('tests/sql/create.table.corp.op.state.sql').read())
    Postgres().execute(open('tests/sql/create.table.corp.type.sql').read())


def test_view():
    seed_corp_type('A', 'XPRO')
    seed_corp_type('BC', 'BC')
    seed_corp_type('QD', 'BC')
    seed_corp_op_state()
    seed_corp('A0012419', 'A')
    seed_corp('A0012445', 'A')
    seed_corp('A0008461', 'A')
    seed_corp_name('A0012419', '19', 'CO', 'ONLINE SEALING SERVICES LTD.')
    seed_corp_name('A0012445', '20', 'CO', 'HOWIE MEEKER ENTERPRISES LIMITED')
    seed_corp_name('A0008461', '21', 'CO', 'W.H. ODELL DRUGS LTD.')
    seed_corp_state('A0012419', '7')
    seed_corp_state('A0012445', '8')
    seed_corp_state('A0008461', '9')

    seed_corp('0000160', 'BC')
    seed_corp('QD0000162', 'QD')
    seed_corp('0000558', 'BC')
    seed_corp_name('0000160','10', 'CO','BRITISH COLUMBIA GOLF CLUB, LIMITED')
    seed_corp_name('QD0000162', '11', 'CO', 'THE VERNON JOCKEY CLUB LIMITED LIABILITY')
    seed_corp_name('0000558', '12', 'CO', 'COLUMBIA ESTATE COMPANY LIMITED')
    seed_corp_state('0000160', '1')
    seed_corp_state('QD0000162', '2')
    seed_corp_state('0000558', '3')

    seed_corp('A0037274', 'A')
    seed_corp('A0038332', 'A')
    seed_corp('A0041224', 'A')
    seed_corp_name('A0037274','15','AS','ASSUMED ROBEV VENTURES LTD.')
    seed_corp_name('A0038332', '16','AS', 'ASSUMED RED-L HOSE DISTRIBUTORS LTD.')
    seed_corp_name('A0041224', '17', 'AS','ASSUMED 571266 SASKATCHEWAN INC.')
    seed_corp_state('A0037274', '4')
    seed_corp_state('A0038332','5')
    seed_corp_state('A0041224','6')

    #ensure tables are seeded
    result = Postgres().select("select * from corporation where corp_typ_cd= 'A' ")
    assert_that(len(result), equal_to(6))

    result = Postgres().select("select * from corporation where corp_typ_cd IN ('BC','QD') ")
    assert_that(len(result),equal_to(3))

    result = Postgres().select(extract_select())
    assert_that(len(result),equal_to(9))

    #seed XPROS that have an assumed name row with a CO row to duplicate production
    seed_corp_name('A0037274','18','CO','ROBEV VENTURES LTD.')
    seed_corp_name('A0038332', '19','CO', 'RED-L HOSE DISTRIBUTORS LTD.')
    seed_corp_name('A0041224', '20', 'CO','571266 SASKATCHEWAN INC.')

    #ensure these XPRO CO rows do not appear in the view
    result = Postgres().select(extract_select())
    assert_that(len(result),equal_to(9))

