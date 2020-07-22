"""
Unit tests for Name Request state transitions.
"""

from namex.models import State
from namex.services.name_request import NameRequestService
# Use the static methods in the NameRequest(s) class
from namex.resources.name_requests import NameRequest

from .test_setup_utils import build_nr


def test_initial_to_draft(client, jwt, app):
    """
    Setup:
    - Initialize NameRequestService
    - Create a new Request model instance
    Test:
    - Call apply_state_change on the NameRequestService instance
    - Make sure to pass in the Request model instance to apply_state_change
    - Make sure to pass in the appropriate apply_state_change handler eg. handle_name_request_<create|update> to apply_state_change
    Validate:
    - That the state change is successful
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


def test_initial_to_conditionally_reserved(client, jwt, app):
    """
    Setup:
    - Initialize NameRequestService
    - Create a new Request model instance
    Test:
    - Call apply_state_change on the NameRequestService instance
    - Make sure to pass in the Request model instance to apply_state_change
    - Make sure to pass in the appropriate apply_state_change handler eg. handle_name_request_<create|update> to apply_state_change
    Validate:
    - That the state change is successful
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
    updated_nr_model = nr_svc.apply_state_change(nr_model, State.COND_RESERVE, NameRequest.handle_name_request_update)

    # Test the result
    assert updated_nr_model is not None


def test_initial_to_reserved(client, jwt, app):
    """
    Setup:
    - Initialize NameRequestService
    - Create a new Request model instance
    Test:
    - Call apply_state_change on the NameRequestService instance
    - Make sure to pass in the Request model instance to apply_state_change
    - Make sure to pass in the appropriate apply_state_change handler eg. handle_name_request_<create|update> to apply_state_change
    Validate:
    - That the state change is successful
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
    updated_nr_model = nr_svc.apply_state_change(nr_model, State.RESERVED, NameRequest.handle_name_request_update)

    # Test the result
    assert updated_nr_model is not None


def test_draft_to_reserved(client, jwt, app):
    """
    Setup:
    - Initialize NameRequestService
    - Create a new Request model instance
    Test:
    - Call apply_state_change on the NameRequestService instance
    - Make sure to pass in the Request model instance to apply_state_change
    - Make sure to pass in the appropriate apply_state_change handler eg. handle_name_request_<create|update> to apply_state_change
    Validate:
    - That the state change is successful
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
    updated_nr_model = nr_svc.apply_state_change(nr_model, State.RESERVED, NameRequest.handle_name_request_update)

    # Test the result
    assert updated_nr_model is not None


def test_draft_to_conditionally_reserved(client, jwt, app):
    """
    Setup:
    - Initialize NameRequestService
    - Create a new Request model instance
    Test:
    - Call apply_state_change on the NameRequestService instance
    - Make sure to pass in the Request model instance to apply_state_change
    - Make sure to pass in the appropriate apply_state_change handler eg. handle_name_request_<create|update> to apply_state_change
    Validate:
    - That the state change is successful
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
    updated_nr_model = nr_svc.apply_state_change(nr_model, State.COND_RESERVE, NameRequest.handle_name_request_update)

    # Test the result
    assert updated_nr_model is not None


def test_conditionally_reserved_to_conditional(client, jwt, app):
    """
    Setup:
    - Initialize NameRequestService
    - Create a new Request model instance
    Test:
    - Call apply_state_change on the NameRequestService instance
    - Make sure to pass in the Request model instance to apply_state_change
    - Make sure to pass in the appropriate apply_state_change handler eg. handle_name_request_<create|update> to apply_state_change
    Validate:
    - That the state change is successful
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
    nr_model = build_nr(State.COND_RESERVE)
    nr_model.save_to_db()

    # Apply the state change
    updated_nr_model = nr_svc.apply_state_change(nr_model, State.CONDITIONAL, NameRequest.handle_name_request_update)

    # Test the result
    assert updated_nr_model is not None


def test_reserved_to_approved(client, jwt, app):
    """
    Setup:
    - Initialize NameRequestService
    - Create a new Request model instance
    Test:
    - Call apply_state_change on the NameRequestService instance
    - Make sure to pass in the Request model instance to apply_state_change
    - Make sure to pass in the appropriate apply_state_change handler eg. handle_name_request_<create|update> to apply_state_change
    Validate:
    - That the state change is successful
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
    nr_model = build_nr(State.RESERVED)
    nr_model.save_to_db()

    # Apply the state change
    updated_nr_model = nr_svc.apply_state_change(nr_model, State.APPROVED, NameRequest.handle_name_request_update)

    # Test the result
    assert updated_nr_model is not None


def test_conditional_to_hold(client, jwt, app):
    """
    Setup:
    - Initialize NameRequestService
    - Create a new Request model instance
    Test:
    - Call apply_state_change on the NameRequestService instance
    - Make sure to pass in the Request model instance to apply_state_change
    - Make sure to pass in the appropriate apply_state_change handler eg. handle_name_request_<create|update> to apply_state_change
    Validate:
    - That the state change is successful
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
    nr_model = build_nr(State.CONDITIONAL)
    nr_model.save_to_db()

    # Apply the state change
    updated_nr_model = nr_svc.apply_state_change(nr_model, State.HOLD, NameRequest.handle_name_request_update)

    # Test the result
    assert updated_nr_model is not None


def test_approved_to_hold(client, jwt, app):
    """
    Setup:
    - Initialize NameRequestService
    - Create a new Request model instance
    Test:
    - Call apply_state_change on the NameRequestService instance
    - Make sure to pass in the Request model instance to apply_state_change
    - Make sure to pass in the appropriate apply_state_change handler eg. handle_name_request_<create|update> to apply_state_change
    Validate:
    - That the state change is successful
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
    nr_model = build_nr(State.APPROVED)
    nr_model.save_to_db()

    # Apply the state change
    updated_nr_model = nr_svc.apply_state_change(nr_model, State.HOLD, NameRequest.handle_name_request_update)

    # Test the result
    assert updated_nr_model is not None


def test_conditional_to_cancelled(client, jwt, app):
    """
    Setup:
    - Initialize NameRequestService
    - Create a new Request model instance
    Test:
    - Call apply_state_change on the NameRequestService instance
    - Make sure to pass in the Request model instance to apply_state_change
    - Make sure to pass in the appropriate apply_state_change handler eg. handle_name_request_<create|update> to apply_state_change
    Validate:
    - That the state change is successful
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
    nr_model = build_nr(State.CONDITIONAL)
    nr_model.save_to_db()

    # Apply the state change
    updated_nr_model = nr_svc.apply_state_change(nr_model, State.CANCELLED, NameRequest.handle_name_request_update)

    # Test the result
    assert updated_nr_model is not None


def test_approved_to_cancelled(client, jwt, app):
    """
    Setup:
    - Initialize NameRequestService
    - Create a new Request model instance
    Test:
    - Call apply_state_change on the NameRequestService instance
    - Make sure to pass in the Request model instance to apply_state_change
    - Make sure to pass in the appropriate apply_state_change handler eg. handle_name_request_<create|update> to apply_state_change
    Validate:
    - That the state change is successful
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
    nr_model = build_nr(State.APPROVED)
    nr_model.save_to_db()

    # Apply the state change
    updated_nr_model = nr_svc.apply_state_change(nr_model, State.CANCELLED, NameRequest.handle_name_request_update)

    # Test the result
    assert updated_nr_model is not None


def test_conditional_to_rejected(client, jwt, app):
    """
    Setup:
    - Initialize NameRequestService
    - Create a new Request model instance
    Test:
    - Call apply_state_change on the NameRequestService instance
    - Make sure to pass in the Request model instance to apply_state_change
    - Make sure to pass in the appropriate apply_state_change handler eg. handle_name_request_<create|update> to apply_state_change
    Validate:
    - That the state change is successful
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
    nr_model = build_nr(State.CONDITIONAL)
    nr_model.save_to_db()

    # Apply the state change
    updated_nr_model = nr_svc.apply_state_change(nr_model, State.REJECTED, NameRequest.handle_name_request_update)

    # Test the result
    assert updated_nr_model is not None


def test_approved_to_rejected(client, jwt, app):
    """
    Setup:
    - Initialize NameRequestService
    - Create a new Request model instance
    Test:
    - Call apply_state_change on the NameRequestService instance
    - Make sure to pass in the Request model instance to apply_state_change
    - Make sure to pass in the appropriate apply_state_change handler eg. handle_name_request_<create|update> to apply_state_change
    Validate:
    - That the state change is successful
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
    nr_model = build_nr(State.APPROVED)
    nr_model.save_to_db()

    # Apply the state change
    updated_nr_model = nr_svc.apply_state_change(nr_model, State.REJECTED, NameRequest.handle_name_request_update)

    # Test the result
    assert updated_nr_model is not None
