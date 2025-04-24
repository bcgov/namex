from http import HTTPStatus
import pytest

from .common import API_BASE_URI

# Import token and claims if you need it
# from ..common import token_header, claims
from ..common.http import build_test_query, build_request_uri
from ..common.logging import log_request_path

from tests.python import integration_mras


@pytest.mark.parametrize(
    'test_name, province, corp_num, expected_status, expected_msg',
    [
        (
            'valid',  # test_name
            'QC',  # province
            '1172490972',  # corp_num
            HTTPStatus.OK,  # expected_status
            '',  # expected_msg
        ),
        ('invalid jurisdiction', '42', '1172490972', HTTPStatus.BAD_REQUEST, ''),
        ('invalid registration', 'QC', 'invalid', HTTPStatus.NOT_FOUND, ''),
    ],
)
@integration_mras
def test_mras_get_profile(client, jwt, app, test_name, province, corp_num, expected_status, expected_msg):
    """Assert that the test suite works as expected.

    This calls a live MRAS endpoint that has the test data available to it.
    It passes the MRAS profile through without changes if it exists.
    """
    request_uri = API_BASE_URI + '{province}/{corp_num}'.format(province=province, corp_num=corp_num)
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)
    print(repr(response))
    assert response and response.status_code == expected_status
