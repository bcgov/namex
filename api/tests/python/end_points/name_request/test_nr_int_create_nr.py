import json

from .configuration import API_BASE_URI
# Import token and claims if you need it
# from ..common import token_header, claims
from ..common.http import build_test_query, build_request_uri
from ..common.logging import log_request_path


def test_create_draft_nr(client, jwt, app):
    """
    Test
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    request_uri = API_BASE_URI
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)
    assert payload is not None


def test_create_conditional_nr(client, jwt, app):
    """
    Test
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    request_uri = API_BASE_URI
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)
    assert payload is not None


def test_create_reserved_nr(client, jwt, app):
    """
    Test
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    request_uri = API_BASE_URI
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)
    assert payload is not None
