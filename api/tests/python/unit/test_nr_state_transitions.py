"""
Unit tests for Name Request state transitions.
"""

from namex.services.name_request import NameRequestService


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
    pass


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
    pass


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
    pass


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
    pass


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
    pass


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
    pass


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
    pass


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
    pass


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
    pass


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
    pass


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
    pass


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
    pass


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
    pass
