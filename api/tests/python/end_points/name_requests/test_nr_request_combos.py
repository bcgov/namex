import pytest
import json

from tests.python.common.test_name_request_utils import \
    assert_field_is_mapped, assert_field_equals_value, assert_field_is_lt_value

from .test_setup_utils.test_helpers import \
    create_draft_nr, patch_nr

from namex.constants import NameRequestActions

# Define our data
# Check NR number is the same because these are PATCH and call change_nr
draft_input_fields = {
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
    'state': 'DRAFT',
    'stateCd': 'DRAFT',
    'submitCount': 1,
    # 'submittedDate': None,
    'submitter_userid': 'name_request_service_account',
    'userId': 'name_request_service_account',
    'xproJurisdiction': ''
}


@pytest.mark.skip
def test_fields_were_updated(client, initial_data, update_data, expected_result, mocker):
    """
    Note that this does not test associations!
    Setup:
    Test:
    :param client:
    :param initial_data: Dict
    :param update_data: Dict
    :param expected_result: Dict
    :return:
    """
    # Define our data
    input_fields = initial_data
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    patch_response = patch_nr(client, NameRequestActions.EDIT.value, draft_nr.get('id'), update_data, mocker)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check data
    for key, value in expected_result.items():
        assert_field_equals_value(patched_nr, key, value)


@pytest.mark.skip
def test_change_request_action_entity_reqtype(client, test_map, mocker):
    """
    Setup:
    Test:
    :param client:
    :param test_map:

    """
    for test_case in test_map:
        initial_data = {
            'request_action_cd': test_case.get('combo')[0],
            'entity_type_cd': test_case.get('combo')[1],
            'requestTypeCd': test_case.get('combo')[2]
        }

        update_data = {
            'request_action_cd': test_case.get('combo')[0],
            'entity_type_cd': test_case.get('combo')[1],
            'requestTypeCd': test_case.get('combo')[2]
        }

        expected_result = {
            'request_action_cd': test_case.get('result')[0],
            'entity_type_cd': test_case.get('result')[1],
            'requestTypeCd': test_case.get('result')[2]
        }

        test_fields_were_updated(client, initial_data, update_data, expected_result, mocker)


@pytest.mark.skip
def test_change_request_actions(client, mocker):
    """
    Setup:
    Test:
    :param client:
    """
    test_cases = [
        # Test actions
        {
            # request_action_cd, entity_type_cd, requestTypeCd
            'combo': ('NEW', 'CR', 'CR'),
            'result': ('NEW', 'CR', 'CR')
        },
        {
            # request_action_cd, entity_type_cd, requestTypeCd
            'combo': ('MVE', 'CR', 'CR'),
            'result': ('MVE', 'CR', 'CR')
        },
        {
            # request_action_cd, entity_type_cd, requestTypeCd
            'combo': ('CHG', 'CR', 'CR'),
            'result': ('CHG', 'CR', 'CR')
        },
        {
            # request_action_cd, entity_type_cd, requestTypeCd
            'combo': ('DBA', 'CR', 'CR'),
            'result': ('DBA', 'CR', 'CR')
        },
        {
            # request_action_cd, entity_type_cd, requestTypeCd
            'combo': ('AML', 'CR', 'CR'),
            'result': ('AML', 'CR', 'CR')
        },
        {
            # request_action_cd, entity_type_cd, requestTypeCd
            'combo': ('CNV', 'CR', 'CR'),
            'result': ('CNV', 'CR', 'CR')
        },
        {
            # request_action_cd, entity_type_cd, requestTypeCd
            'combo': ('REH', 'CR', 'CR'),
            'result': ('REH', 'CR', 'CR')
        },
        {
            # request_action_cd, entity_type_cd, requestTypeCd
            'combo': ('REN', 'CR', 'CR'),
            'result': ('REN', 'CR', 'CR')
        },
        {
            # request_action_cd, entity_type_cd, requestTypeCd
            'combo': ('ASSUMED', 'CR', 'CR'),
            'result': ('ASSUMED', 'CR', 'CR')
        },
        {
            # request_action_cd, entity_type_cd, requestTypeCd
            'combo': ('CHG-ASSUM', 'CR', 'CR'),
            'result': ('CHG-ASSUM', 'CR', 'CR')
        },
        {
            # request_action_cd, entity_type_cd, requestTypeCd
            'combo': ('NRO-NEWAML', 'CR', 'CR'),
            'result': ('NRO-NEWAML', 'CR', 'CR')
        },
        {
            # request_action_cd, entity_type_cd, requestTypeCd
            'combo': ('NRO-REST', 'CR', 'CR'),
            'result': ('NRO-REST', 'CR', 'CR')
        }
    ]

    test_change_request_action_entity_reqtype(client, test_cases, mocker)


def test_change_request_entity(client, mocker):
    """
    Setup:
    Test:
    :param client:
    """
    test_cases = [
        # Test actions
        {
            # request_action_cd, entity_type_cd, requestTypeCd
            'combo': ('NEW', 'CR', 'CR'),
            'result': ('NEW', 'CR', 'CR')
        }
    ]

    test_change_request_action_entity_reqtype(client, test_cases, mocker)


def test_change_request_type(client, mocker):
    """
    Setup:
    Test:
    :param client:
    """
    test_cases = [
        # Test actions
        {
            # request_action_cd, entity_type_cd, requestTypeCd
            'combo': ('NEW', 'CR', 'CR'),
            'result': ('NEW', 'CR', 'CR')
        }
    ]

    test_change_request_action_entity_reqtype(client, test_cases, mocker)


