"""
Integration tests for Name Request state transitions.
"""

import json
import pytest

from .configuration import API_BASE_URI
# Import token and claims if you need it
# from ..common import token_header, claims
from ..common.http import build_test_query, build_request_uri
from ..common.logging import log_request_path

from .test_setup_utils import create_nr, get_nr_request_uri

from namex.models import State


@pytest.mark.skip
def test_initial_to_reserved(client, jwt, app):
    """
    Setup:
    - Create a basic INITIAL NR
    Test:
    - Update the record (PUT) to the RESERVED STATE
    - Save the record
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Set up our test data
    nr = create_nr(State.DRAFT)

    request_uri = API_BASE_URI + nr.nrNum
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)
    assert payload is not None


@pytest.mark.skip
def test_initial_to_conditionally_reserved(client, jwt, app):
    """
    Setup:
    - Create a basic INITIAL NR
    Test:
    - Update the record (PUT) to the COND-RESERVE state
    - Save the record
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Set up our test data
    nr = create_nr(State.DRAFT)

    request_uri = API_BASE_URI + nr.nrNum
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)
    assert payload is not None


@pytest.mark.skip
def test_initial_to_draft(client, jwt, app):
    """
    Setup:
    - Create a basic INITIAL NR
    Test:
    - Update the record (PUT) to the DRAFT state
    - Save the record
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Set up our test data
    nr = create_nr(State.DRAFT)

    request_uri = API_BASE_URI + nr.nrNum
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)
    assert payload is not None


@pytest.mark.skip
def test_conditionally_reserved_to_conditional(client, jwt, app):
    """
    Setup:
    - Create a basic INITIAL NR
    Test:
    - Update the record (PUT) to the COND-RESERVE state
    - Save the record
    - Create a payment (see Payments)
    - Update the record (PUT) to the CONDITIONAL state
    Validate:
    - Assert that all is as expected
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Set up our test data
    nr = create_nr(State.COND_RESERVE)

    request_uri = API_BASE_URI + nr.nrNum
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)
    assert payload is not None


@pytest.mark.skip
def test_reserved_to_approved(client, jwt, app):
    """
    Setup:
    - Create a basic INITIAL NR
    Test:
    - Update the record (PUT) to the RESERVED state
    - Save the record
    - Create a payment (see Payments)
    - Update the record (PUT) to the APPROVED state
    Validate:
    - Assert that all is as expected
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Set up our test data
    nr = create_nr(State.RESERVED)

    request_uri = API_BASE_URI + nr.nrNum
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)
    assert payload is not None


@pytest.mark.skip
def test_conditional_to_hold(client, jwt, app):
    """
    Setup:
    - Create a basic INITIAL NR
    Test:
    - Update the record (PUT) to the COND-RESERVE state
    - Save the record
    - Create a payment (see Payments)
    - Update the record (PUT) to the CONDITIONAL state
    - Save the record
    - Update the record (PATCH) to the HOLD state
    - Save the record
    Validate:
    - Assert that all is as expected
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Set up our test data
    nr = create_nr(State.CONDITIONAL)

    request_uri = API_BASE_URI + nr.nrNum
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)
    assert payload is not None


@pytest.mark.skip
def test_approved_to_hold(client, jwt, app):
    """
    Setup:
    - Create a basic INITIAL NR
    Test:
    - Update the record (PUT) to the RESERVED state
    - Save the record
    - Create a payment (see Payments)
    - Update the record (PUT) to the APPROVED state
    - Save the record
    - Update the record (PATCH) to the HOLD state
    - Save the record
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Set up our test data
    nr = create_nr(State.APPROVED)

    request_uri = API_BASE_URI + nr.nrNum
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)
    assert payload is not None


@pytest.mark.skip
def test_conditional_to_cancelled(client, jwt, app):
    """
    Setup:
    - Create a basic INITIAL NR
    Test:
    - Update the record (PUT) to the COND-RESERVE state
    - Save the record
    - Create a payment (see Payments)
    - Update the record (PUT) to the CONDITIONAL state
    - Save the record
    - Update the record (PATCH) to the CANCELLED state
    - Save the record
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Set up our test data
    nr = create_nr(State.CONDITIONAL)

    request_uri = API_BASE_URI + nr.nrNum
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)
    assert payload is not None


@pytest.mark.skip
def test_approved_to_cancelled(client, jwt, app):
    """
    Setup:
    - Create a basic INITIAL NR
    Test:
    - Update the record (PUT) to the RESERVED state
    - Save the record
    - Create a payment (see Payments)
    - Update the record (PUT) to the APPROVED state
    - Save the record
    - Update the record (PATCH) to the CANCELLED state
    - Save the record
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Set up our test data
    nr = create_nr(State.APPROVED)

    request_uri = API_BASE_URI + nr.nrNum
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)
    assert payload is not None


@pytest.mark.skip
def test_conditional_to_rejected(client, jwt, app):
    """
    Setup:
    - Create a basic INITIAL NR
    Test:
    - Update the record (PUT) to the COND-RESERVE state
    - Save the record
    - Create a payment (see Payments)
    - Update the record (PUT) to the CONDITIONAL state
    - Save the record
    - Update the record (PATCH) to the REJECTED state
    - Save the record
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Set up our test data
    nr = create_nr(State.CONDITIONAL)

    request_uri = API_BASE_URI + nr.nrNum
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)
    assert payload is not None


@pytest.mark.skip
def test_approved_to_rejected(client, jwt, app):
    """
    Setup:
    - Create a basic INITIAL NR
    Test:
    - Update the record (PUT) to the RESERVED state
    - Save the record
    - Create a payment (see Payments)
    - Update the record (PUT) to the APPROVED state
    - Save the record
    - Update the record (PATCH) to the REJECTED state
    - Save the record
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Set up our test data
    nr = create_nr(State.APPROVED)

    request_uri = API_BASE_URI + nr.nrNum
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)
    assert payload is not None
