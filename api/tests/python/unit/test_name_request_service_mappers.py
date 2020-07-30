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
    # TODO: We need this first
    pass


@pytest.mark.skip
def test_map_request_names(client, jwt, app):
    # TODO: We need this first
    pass


@pytest.mark.skip
def test_map_submitted_name(client, jwt, app):
    # TODO: We need this first
    pass


@pytest.mark.skip
def test_map_submitted_name_attrs(client, jwt, app):
    # TODO: We need this first
    pass


@pytest.mark.skip
def test_map_draft_attrs(client, jwt, app):
    pass


@pytest.mark.skip
def test_map_request_attrs(client, jwt, app):
    pass


@pytest.mark.skip
def test_map_request_header_attrs(client, jwt, app):
    pass


@pytest.mark.skip
def test_map_request_comments(client, jwt, app):
    pass


@pytest.mark.skip
def test_map_request_language_comments(client, jwt, app):
    pass


@pytest.mark.skip
def test_map_request_person_name_comments(client, jwt, app):
    pass


@pytest.mark.skip
def test_map_submitted_name_conflicts(client, jwt, app):
    pass


@pytest.mark.skip
def test_clear_submitted_name_conflicts(client, jwt, app):
    pass
