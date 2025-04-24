"""
Unit tests for Name Request mapping methods.
"""

import pytest

from namex.models import db, State, Request, Name
from namex.services.name_request import NameRequestService

# from namex.services.name_request.name_request_state import get_nr_state_actions
# Use the static methods in the NameRequest(s) class
from namex.resources.name_requests import NameRequestResource

from .test_setup_utils import build_nr
from tests.python.common.test_name_request_utils import (
    pick_name_from_list,
    assert_name_has_name,
    assert_name_has_id,
    assert_field_is_mapped,
)

test_names_no_id = [
    {
        'name': 'BLUE HERON TOURS LTD.',
        'choice': 1,
        'designation': 'LTD.',
        'name_type_cd': 'CO',
        'consent_words': '',
        'conflict1': 'BLUE HERON TOURS LTD.',
        'conflict1_num': '0515211',
    },
    {
        'name': 'BLUE HERON ADVENTURE TOURS LTD.',
        'choice': 2,
        'designation': 'LTD.',
        'name_type_cd': 'CO',
        'consent_words': '',
        'conflict1': 'BLUE HERON TOURS LTD.',
        'conflict1_num': '0515211',
    },
    {
        'name': 'BLUE HERON ISLAND TOURS LTD.',
        'choice': 3,
        'designation': 'LTD.',
        'name_type_cd': 'CO',
        'consent_words': '',
        'conflict1': 'BLUE HERON TOURS LTD.',
        'conflict1_num': '0515211',
    },
]


@pytest.mark.skip
def assert_names_are_mapped_correctly(req_names, res_names):
    print('\n-------- Test names --------\n')
    for req_name in req_names:
        res_name = pick_name_from_list(res_names, req_name.get('name'))

        print('\nCompare request name: \n' + repr(req_name) + '\n')
        print('With response name: \n' + repr(res_name) + '\n')

        assert_name_has_name(res_name)

        if res_name and req_name.get('id', None) is None:
            # It's a new name make sure it has an ID set
            assert_name_has_id(res_name)
        if res_name and req_name.get('id', None) is not None:
            # The name existed, make sure the ID has not changed
            assert_field_is_mapped(req_name, res_name, 'id')

        # Make sure the choice is mapped correctly
        assert_field_is_mapped(req_name, res_name, 'choice')
        print('\n......................................\n')

    print('\n-------- Test names complete --------\n')


@pytest.mark.skip
def do_test_cleanup():
    # Clean up
    # Delete all Names
    db.session.query(Name).delete()
    # Delete all NameRequests
    db.session.query(Request).delete()
    db.session.commit()


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
    # updated_nr_model = nr_svc.apply_state_change(nr_model, State.DRAFT, NameRequest.handle_name_request_update)

    # Test the result
    # assert updated_nr_model is not None


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


def test_add_request_names(client, jwt, app):
    """
    Setup:
    Test:
    Validate:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    do_test_cleanup()

    # Initialize the service
    nr_svc = NameRequestService()

    """
    Test adding two new names 
    """
    # We will need a base NR
    nr = build_nr(State.DRAFT, {}, [test_names_no_id[0]])
    # We can't save the NR without an NR Num
    nr.nrNum = 'NR L000001'
    # Save to DB so PK sequences are updated
    nr.save_to_db()
    db.session.flush()

    nr = Request.find_by_nr(nr.nrNum)

    # Set data to the service, all we need to test is names so just provide what's necessary
    nr_svc.request_data = {
        'names': [
            # Same as test name 1
            test_names_no_id[1],
            test_names_no_id[2],
        ]
    }

    # Build the names
    nr = nr_svc.map_request_names(nr)

    nr.save_to_db()

    nr = Request.find_by_nr(nr.nrNum)

    # Convert to dict
    nr = nr.json()

    assert nr is not None
    # Test the names
    assert_names_are_mapped_correctly(nr_svc.request_data.get('names'), nr.get('names'))

    # Clean up
    do_test_cleanup()


def test_update_request_names(client, jwt, app):
    """
    Setup:
    Test:
    Validate:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    do_test_cleanup()

    # Initialize the service
    nr_svc = NameRequestService()

    """
    Test updating three names 
    """
    # We will need a base NR
    nr = build_nr(State.DRAFT, {}, [test_names_no_id[0], test_names_no_id[1]])
    # We can't save the NR without an NR Num
    nr.nrNum = 'NR L000001'
    # Save to DB so PK sequences are updated
    nr.save_to_db()
    db.session.flush()

    # NR
    added_names = list(map(lambda n: n.as_dict(), nr.names))
    added_name_0 = pick_name_from_list(added_names, test_names_no_id[0].get('name'))
    added_name_1 = pick_name_from_list(added_names, test_names_no_id[1].get('name'))

    # Set data to the service, all we need to test is names so just provide what's necessary
    nr_svc.request_data = {
        'names': [
            # Same as test name 1
            added_name_0,  # Map this over
            added_name_1,  # Map this over
            test_names_no_id[2],
        ]
    }

    # Build the names
    nr = nr_svc.map_request_names(nr)

    nr.save_to_db()

    nr = Request.find_by_nr(nr.nrNum)

    # Convert to dict
    nr = nr.json()

    assert nr is not None
    # Test the names
    assert_names_are_mapped_correctly(nr_svc.request_data.get('names'), nr.get('names'))

    # Clean up
    do_test_cleanup()


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
