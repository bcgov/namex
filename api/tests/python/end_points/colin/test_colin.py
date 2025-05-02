import pytest

# Import token and claims if you need it
# from ..common import token_header, claims
from ..common.http import build_request_uri, build_test_query
from ..common.logging import log_request_path
from .common import API_BASE_URI


@pytest.mark.skip
def test_colin_request(client, jwt, app):
    """ """
    corp_num = '0644263'  # Test corp num / profile ID from MRAS docs

    request_uri = API_BASE_URI + '{corp_num}'.format(corp_num=corp_num)
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.post(path)
    print(repr(response))
    assert response and response.status_code == 200
