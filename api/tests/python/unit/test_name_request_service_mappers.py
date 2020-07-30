"""
Unit tests for Name Request mapping methods.
"""
import pytest

from namex.models import State
from namex.services.name_request import NameRequestService
# from namex.services.name_request.name_request_state import get_nr_state_actions
# Use the static methods in the NameRequest(s) class
from namex.resources.name_requests import NameRequest

from .test_setup_utils import build_nr

test_names_no_id = [
    {
        "name": "BLUE HERON TOURS LTD.",
        "choice": 1,
        "designation": "LTD.",
        "name_type_cd": "CO",
        "consent_words": "",
        "conflict1": "BLUE HERON TOURS LTD.",
        "conflict1_num": "0515211"
    },
    {
        "name": "BLUE HERON ADVENTURE TOURS LTD.",
        "choice": 2,
        "designation": "LTD.",
        "name_type_cd": "CO",
        "consent_words": "",
        "conflict1": "BLUE HERON TOURS LTD.",
        "conflict1_num": "0515211"
    },
    {
        "name": "BLUE HERON ISLAND TOURS LTD.",
        "choice": 3,
        "designation": "LTD.",
        "name_type_cd": "CO",
        "consent_words": "",
        "conflict1": "BLUE HERON TOURS LTD.",
        "conflict1_num": "0515211"
    }
]

test_names = [
    {
        "id": 1,
        "name": "BLUE HERON TOURS LTD.",
        "choice": 1,
        "designation": "LTD.",
        "name_type_cd": "CO",
        "consent_words": "",
        "conflict1": "BLUE HERON TOURS LTD.",
        "conflict1_num": "0515211"
    },
    {
        "id": 2,
        "name": "BLUE HERON ADVENTURE TOURS LTD.",
        "choice": 2,
        "designation": "LTD.",
        "name_type_cd": "CO",
        "consent_words": "",
        "conflict1": "BLUE HERON TOURS LTD.",
        "conflict1_num": "0515211"
    },
    {
        "id": 3,
        "name": "BLUE HERON ISLAND TOURS LTD.",
        "choice": 3,
        "designation": "LTD.",
        "name_type_cd": "CO",
        "consent_words": "",
        "conflict1": "BLUE HERON TOURS LTD.",
        "conflict1_num": "0515211"
    }
]


@pytest.mark.skip
def test_map_request_data(client, jwt, app):
    """
    Setup:
    Test:
    Validate:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    nr_svc = NameRequestService()
    # Set data to the service
    input_data = {}
    nr_svc.request_data = input_data

    # Build the NR structure
    nr_model = build_nr(State.DRAFT)
    nr_model.save_to_db()

    # Apply the state change
    updated_nr_model = nr_svc.apply_state_change(nr_model, State.DRAFT, NameRequest.handle_name_request_update)

    # Test the result
    assert updated_nr_model is not None


@pytest.mark.skip
def test_map_request_applicants(client, jwt, app):
    """
    Setup:
    Test:
    Validate:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # TODO: We need this first
    pass


def test_map_request_names(client, jwt, app):
    """
    Setup:
    Test:
    Validate:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Initialize the service
    nr_svc = NameRequestService()

    """
    Test adding two new names 
    """
    # We will need a base NR
    nr = build_nr(State.DRAFT, [test_names[0]])

    # Set data to the service, all we need to test is names so just provide what's necessary
    nr_svc.request_data = {
        'names': [
            # Same as test name 1
            test_names_no_id[1],
            test_names_no_id[2]
        ]
    }

    # Build the names
    nr = nr_svc.map_request_names(nr)

    assert nr is not None

    """
    Test updating three names 
    """
    # We will need a base NR
    nr = build_nr(State.DRAFT, [test_names[0], test_names[1], test_names[2]])

    # Set data to the service, all we need to test is names so just provide what's necessary
    nr_svc.request_data = {
        'names': [
            # Same as test name 1
            test_names[0],
            test_names[1],
            test_names[2]
        ]
    }

    # Build the names
    nr = nr_svc.map_request_names(nr)

    assert nr is not None


@pytest.mark.skip
def test_map_submitted_name(client, jwt, app):
    """
    Setup:
    Test:
    Validate:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # TODO: We need this first
    pass


@pytest.mark.skip
def test_map_submitted_name_attrs(client, jwt, app):
    """
    Setup:
    Test:
    Validate:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # TODO: We need this first
    pass


@pytest.mark.skip
def test_map_draft_attrs(client, jwt, app):
    """
    Setup:
    Test:
    Validate:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    pass


@pytest.mark.skip
def test_map_request_attrs(client, jwt, app):
    """
    Setup:
    Test:
    Validate:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    pass


@pytest.mark.skip
def test_map_request_header_attrs(client, jwt, app):
    """
    Setup:
    Test:
    Validate:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    pass


@pytest.mark.skip
def test_map_request_comments(client, jwt, app):
    """
    Setup:
    Test:
    Validate:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    pass


@pytest.mark.skip
def test_map_request_language_comments(client, jwt, app):
    """
    Setup:
    Test:
    Validate:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    pass


@pytest.mark.skip
def test_map_request_person_name_comments(client, jwt, app):
    """
    Setup:
    Test:
    Validate:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    pass


@pytest.mark.skip
def test_map_submitted_name_conflicts(client, jwt, app):
    """
    Setup:
    Test:
    Validate:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    pass


@pytest.mark.skip
def test_clear_submitted_name_conflicts(client, jwt, app):
    """
    Setup:
    Test:
    Validate:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    pass
