"""
Integration tests for Name Request state transitions.
"""
import pytest
import json

from tests.python.common.test_name_request_utils import \
    assert_field_is_mapped, assert_list_contains

from .test_setup_utils.test_helpers import \
    create_test_nr, get_nr

from namex.models import State
from namex.constants import NameRequestActions

# Define our data
# Check NR number is the same because these are PATCH and call change_nr
test_input_fields = {
    'additionalInfo': '',
    'consentFlag': None,
    'consent_dt': None,
    'corpNum': '',
    'entity_type_cd': 'CR',
    'expirationDate': None,
    'furnished': 'N',
    'hasBeenReset': False,
    # 'lastUpdate': None,
    'natureBusinessInfo': 'Test',
    # 'nrNum': '',
    # 'nwpta': '',
    # 'previousNr': '',
    # 'previousRequestId': '',
    # 'previousStateCd': '',
    'priorityCd': 'N',
    # 'priorityDate': None,
    'requestTypeCd': 'CR',
    'request_action_cd': 'NEW',
    # 'source': 'NAMEREQUEST',
    # 'state': 'DRAFT',
    # 'stateCd': 'DRAFT',
    'submitCount': 1,
    # 'submittedDate': None,
    'submitter_userid': 'name_request_service_account',
    'userId': 'name_request_service_account',
    'xproJurisdiction': ''
}


def test_draft_response_actions(client, jwt, app):
    """
    Test the Name Request's data fields. Excludes associations 'names' and 'applicant' - we have other tests for those.
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = test_input_fields

    # Assign the payload to new nr var
    test_nr = create_test_nr(input_fields, State.DRAFT)
    assert test_nr is not None

    # Grab the record using the API
    get_response = get_nr(client, test_nr.get('id'))
    nr = json.loads(get_response.data)
    assert nr is not None

    print('PATCH Response: \n' + json.dumps(nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(nr.get('stateCd') == 'DRAFT')))
    assert nr.get('stateCd') == State.DRAFT

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(test_nr, nr, 'nrNum')

    # Check actions
    actions = nr.get('actions')
    assert_list_contains(actions, [
        NameRequestActions.EDIT.value,
        NameRequestActions.UPGRADE.value,
    ])


def test_approved_response_actions(client, jwt, app):
    """
    Test the Name Request's data fields. Excludes associations 'names' and 'applicant' - we have other tests for those.
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = test_input_fields

    # Assign the payload to new nr var
    test_nr = create_test_nr(input_fields, State.APPROVED)
    assert test_nr is not None

    # Grab the record using the API
    get_response = get_nr(client, test_nr.get('id'))
    nr = json.loads(get_response.data)
    assert nr is not None

    print('PATCH Response: \n' + json.dumps(nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == APPROVED: ' + str(bool(nr.get('stateCd') == 'APPROVED')))
    assert nr.get('stateCd') == State.APPROVED

    assert_field_is_mapped(test_nr, nr, 'nrNum')

    # Check actions
    actions = nr.get('actions')
    assert_list_contains(actions, [
        NameRequestActions.EDIT.value,
        NameRequestActions.UPGRADE.value,
    ])


def test_conditional_response_actions(client, jwt, app):
    """
    Test the Name Request's data fields. Excludes associations 'names' and 'applicant' - we have other tests for those.
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = test_input_fields

    # Assign the payload to new nr var
    test_nr = create_test_nr(input_fields, State.CONDITIONAL)
    assert test_nr is not None

    # Grab the record using the API
    get_response = get_nr(client, test_nr.get('id'))
    nr = json.loads(get_response.data)
    assert nr is not None

    print('PATCH Response: \n' + json.dumps(nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == CONDITIONAL: ' + str(bool(nr.get('stateCd') == 'CONDITIONAL')))
    assert nr.get('stateCd') == State.CONDITIONAL

    assert_field_is_mapped(test_nr, nr, 'nrNum')

    # Check actions
    actions = nr.get('actions')
    assert_list_contains(actions, [
        NameRequestActions.EDIT.value,
        NameRequestActions.UPGRADE.value,
    ])


def test_historical_response_actions(client, jwt, app):
    """
    Test the Name Request's data fields. Excludes associations 'names' and 'applicant' - we have other tests for those.
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = test_input_fields

    # Assign the payload to new nr var
    test_nr = create_test_nr(input_fields, State.CONDITIONAL)
    assert test_nr is not None

    # Grab the record using the API
    get_response = get_nr(client, test_nr.get('id'))
    nr = json.loads(get_response.data)
    assert nr is not None

    print('PATCH Response: \n' + json.dumps(nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == CONDITIONAL: ' + str(bool(nr.get('stateCd') == 'CONDITIONAL')))
    assert nr.get('stateCd') == State.CONDITIONAL

    assert_field_is_mapped(test_nr, nr, 'nrNum')

    # Check actions
    actions = nr.get('actions')
    assert_list_contains(actions, [
        NameRequestActions.EDIT.value,
        NameRequestActions.UPGRADE.value,
    ])


def test_consumed_nr_response_actions(client, jwt, app):
    """
    Test the Name Request's data fields. Excludes associations 'names' and 'applicant' - we have other tests for those.
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = test_input_fields

    # Assign the payload to new nr var
    test_nr = create_test_nr(input_fields, State.CONDITIONAL)
    assert test_nr is not None

    # Grab the record using the API
    get_response = get_nr(client, test_nr.get('id'))
    nr = json.loads(get_response.data)
    assert nr is not None

    print('PATCH Response: \n' + json.dumps(nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == CONDITIONAL: ' + str(bool(nr.get('stateCd') == 'CONDITIONAL')))
    assert nr.get('stateCd') == State.CONDITIONAL

    assert_field_is_mapped(test_nr, nr, 'nrNum')

    # Check actions
    actions = nr.get('actions')
    assert_list_contains(actions, [
        NameRequestActions.EDIT.value,
        NameRequestActions.UPGRADE.value,
    ])
