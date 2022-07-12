from app.resources.corporations import Methods
from unittest import mock
import sys

xpro_corp_nums = ['A0003650']
bc_corp_nums = ['0022258']

def test_readyz(client):
    url = 'api/v1/ops/readyz'
    response = client.get(url)
    assert response.status_code == 200

def test_healthz(client):
    url = 'api/v1/ops/healthz'
    response = client.get(url)
    assert response.status_code == 200
    assert response.json['message'] == 'api is healthy'

def test_not_authenticated(client):
    url = 'api/v1/corporations/A0003650'

    response = client.get(url)

    assert response.status_code == 401


def test_xpro_init_info(client):

    for corp_num in xpro_corp_nums:

        corp_num_sql = '\'' + corp_num + '\''

        info_sql = Methods.build_info_sql(corp_num_sql)
        directors_sql = Methods.build_directors_sql(corp_num_sql)

        assert info_sql is not None
        assert directors_sql is not None

        info_dict, directors_obj = Methods.init_info(info_sql, directors_sql)

        assert info_dict is not None
        assert info_dict['corp_class'] == 'XPRO'
        assert info_dict['corp_num'] == corp_num
        assert info_dict['recognition_dts'] is not None
        assert directors_obj is not None


def test_bc_init_info(client):

    for corp_num in bc_corp_nums:
        corp_num_sql = '\'' + corp_num + '\''

        info_sql = Methods.build_info_sql(corp_num_sql)
        directors_sql = Methods.build_directors_sql(corp_num_sql)

        assert info_sql is not None
        assert directors_sql is not None

        info_dict, directors_obj = Methods.init_info(info_sql, directors_sql)

        assert info_dict is not None
        assert info_dict['corp_class'] == 'BC'
        assert info_dict['corp_num'] == corp_num
        assert info_dict['recognition_dts'] is not None
        assert directors_obj is not None


def test_xpro_corp(client):

    for corp_num in xpro_corp_nums:
        corp_num_sql = '\'' + corp_num + '\''

        addr_id_sql = Methods.build_addr_id_sql(corp_num_sql)
        attorneys_sql = Methods.build_attorneys_sql(corp_num_sql)
        jurisdiction_sql = Methods.build_jurisdiction_sql(corp_num_sql)

        assert addr_id_sql is not None
        assert attorneys_sql is not None
        assert jurisdiction_sql is not None

        head_office_obj, attorneys_obj, jurisdiction_obj = Methods.xpro_get_objs(addr_id_sql, attorneys_sql, jurisdiction_sql)

        assert head_office_obj is not None
        assert attorneys_obj is not None
        assert jurisdiction_obj is not None

        ho_addr_list, attorneys_list, jurisdiction = \
            Methods.xpro_get_vals(head_office_obj, attorneys_obj, jurisdiction_obj)

        assert ho_addr_list is not None
        assert attorneys_list is not None
        assert jurisdiction != 'BC' and jurisdiction is not None


def test_bc_corp(client):

    for corp_num in bc_corp_nums:
        corp_num_sql = '\'' + corp_num + '\''

        addr_id_sql = Methods.build_addr_id_sql(corp_num_sql)

        assert addr_id_sql is not None

        registered_addr_obj, records_addr_obj = Methods.bc_get_objs(addr_id_sql)

        assert registered_addr_obj is not None
        assert records_addr_obj is not None

        registered_addr_list, records_addr_list = \
            Methods.bc_get_vals(registered_addr_obj, records_addr_obj)

        assert registered_addr_list is not None
        assert records_addr_list is not None


def test_get_nob(client):

    for corp_num in bc_corp_nums + xpro_corp_nums:

        corp_num_sql = '\'' + corp_num + '\''

        nr_sql = Methods.build_nr_sql(corp_num_sql)

        assert nr_sql is not None

        nob = Methods.find_nob(nr_sql)

        assert nob is not None
