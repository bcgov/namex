from .common import API_BASE_URI
# Import token and claims if you need it
# from ..common import token_header, claims
from ..common.http import build_test_query, build_request_uri
from ..common.logging import log_request_path


def test_mras_get_profile(client, jwt, app):
    """
    """
    province = 'MB'  # Test jursidiction from MRAS docs
    corp_num = '4291018'  # Test corp num / profile ID from MRAS docs

    request_uri = API_BASE_URI + '{province}/{corp_num}'.format(province=province, corp_num=corp_num)
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)
    print(repr(response))
    assert response and response.status_code == 200

