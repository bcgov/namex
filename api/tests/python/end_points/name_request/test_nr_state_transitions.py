import json

from .configuration import API_BASE_URI
# Import token and claims if you need it
# from ..common import token_header, claims
from ..common.http import build_test_query, build_request_uri
from ..common.logging import log_request_path


def test_draft_to_reserved(client, jwt, app):
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


def test_draft_to_conditionally_reserved(client, jwt, app):
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


def test_conditionally_reserved_to_conditional(client, jwt, app):
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


def test_reserved_to_approved(client, jwt, app):
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


def test_conditional_to_hold(client, jwt, app):
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


def test_approved_to_hold(client, jwt, app):
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


def test_conditional_to_cancelled(client, jwt, app):
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


def test_approved_to_cancelled(client, jwt, app):
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


def test_conditional_to_rejected(client, jwt, app):
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


def test_approved_to_rejected(client, jwt, app):
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
