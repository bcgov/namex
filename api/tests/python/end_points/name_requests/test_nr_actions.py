"""
Test HTTP endpoints for Name Requests.
"""
import datetime
import json

import pytest

from namex.constants import EntityTypes, NameRequestActions
from namex.models import State
from tests.python.common.test_name_request_utils import (
    assert_field_equals_value,
    assert_field_is_lt_value,
    assert_field_is_mapped,
)
from tests.python.end_points.common.http import get_test_headers
from tests.python.end_points.name_requests.test_setup_utils.test_helpers import add_states_to_db, add_test_user_to_db
from tests.python.end_points.util import create_header
from tests.python.unit.test_setup_utils import build_nr

# Import token and claims if you need it
# from ..common import token_header, claims
from ..common.http import build_request_uri, build_test_query
from ..common.logging import log_request_path
from .configuration import API_BASE_URI
from .test_setup_utils.test_helpers import (
    assert_applicant_is_mapped_correctly,
    assert_names_are_mapped_correctly,
    create_approved_nr,
    create_cancelled_nr,
    create_draft_nr,
    patch_nr,
)


# Define our data
# Check NR number is the same because these are PATCH and call change_nr
def build_test_input_fields():
    return {
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


@pytest.mark.skip
def test_create_draft_nr(client, jwt, app):
    """
    TODO: Just a test stub that was moved from another file that was removed.
    This needs to be completed at some point.
    Create a basic draft NR.
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


@pytest.mark.skip
def test_create_conditional_nr(client, jwt, app):
    """
    TODO: Just a test stub that was moved from another file that was removed.
    This needs to be completed at some point.
    Create a basic conditional NR.
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


@pytest.mark.skip
def test_create_reserved_nr(client, jwt, app):
    """
    TODO: Just a test stub that was moved from another file that was removed.
    This needs to be completed at some point.
    Create a basic reserved NR
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


def test_draft_patch_edit_data(client, jwt, app):
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
    input_fields = build_test_input_fields()
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr.get('stateCd') == 'PENDING_PAYMENT'
    assert draft_nr is not None

    # Take the response and edit it
    # Add another name to the mix
    nr_data = {
        'names': draft_nr.get('names'),
        'applicants': draft_nr.get('applicants'),
        'entity_type_cd': 'FR',
        'corpNum': 'TESTCORP123',
        # 'homeJurisNum': 'TESTHOME123',
        'additionalInfo': 'Testing additional info',
        'natureBusinessInfo': 'Testing nature of business info',
        'priorityCd': 'Y',
        'requestTypeCd': 'CR'
    }

    added_names = [
        {
            'name': 'BLUE HERON ADVENTURE TOURS LTD.',
            'choice': 2,
            'designation': 'LTD.',
            'name_type_cd': 'CO',
            'consent_words': '',
            'conflict1': 'BLUE HERON TOURS LTD.',
            'conflict1_num': '0515211'
        },
        {
            'name': 'BLUE HERON ISLAND TOURS LTD.',
            'choice': 3,
            'designation': 'LTD.',
            'name_type_cd': 'CO',
            'consent_words': '',
            'conflict1': 'BLUE HERON TOURS LTD.',
            'conflict1_num': '0515211'
        }
    ]

    nr_data['names'].extend(added_names)

    # Change the designation, we'll check to make sure it's mapped in the response
    nr_data['names'][0]['designation'] = 'INC.'

    # TODO: More applicant testing
    # updated_applicant = {}
    # nr_data['applicant'] = updated_applicant

    patch_response = patch_nr(client, NameRequestActions.EDIT.value, draft_nr.get('id'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None
    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == 'PENDING_PAYMENT'

    # Check names
    assert_names_are_mapped_correctly(nr_data.get('names'), patched_nr.get('names'))

    # Check applicant
    assert_applicant_is_mapped_correctly(nr_data.get('applicants'), patched_nr.get('applicants'))

    # Check data
    expected_field_values = {
        'additionalInfo': 'Testing additional info',
        'consentFlag': None,
        'consent_dt': None,
        'corpNum': 'TESTCORP123',
        # 'homeJurisNum': 'TESTHOME123',
        'entity_type_cd': 'FR',
        'requestTypeCd': 'CR',
        'request_action_cd': 'NEW',
        'expirationDate': None,
        'furnished': 'N',
        'hasBeenReset': False,
        # 'lastUpdate': None,
        'natureBusinessInfo': 'Testing nature of business info',
        # 'nrNum': '',
        # 'nwpta': '',
        # 'previousNr': '',
        # 'previousRequestId': '',
        # 'previousStateCd': '',
        'priorityCd': 'Y',
        # 'priorityDate': None,
        'source': 'NAMEREQUEST',
        'state': 'PENDING_PAYMENT',
        'stateCd': 'PENDING_PAYMENT',
        'submitCount': 1,
        # 'submittedDate': None,
        'submitter_userid': 'name_request_service_account',
        'userId': 'name_request_service_account',
        'xproJurisdiction': ''
    }

    for key, value in expected_field_values.items():
        assert_field_equals_value(patched_nr, key, value)


def test_draft_patch_edit_request_action_and_entity_type(client, jwt, app):
    """
    This is not designed to test all combinations, for those tests see test_nr_request_combos.
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data, which is initially set to:
    # test_input_fields = {
    #     'request_action_cd': 'NEW'
    #     'entity_type_cd': 'CR'
    #     'requestTypeCd': 'CR'
    #     ...
    # }
    input_fields = build_test_input_fields()
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    # Change the request action
    nr_data = {
        'request_action_cd': 'CHG',
        'entity_type_cd': 'RLC',  # Limited Liability Co.
        'requestTypeCd': 'CLC'  # From request_type_mapping in namex.constants
    }

    patch_response = patch_nr(client, NameRequestActions.EDIT.value, draft_nr.get('id'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    assert patched_nr.get('stateCd') == 'PENDING_PAYMENT'

    # Check data
    expected_field_values = {
        'request_action_cd': 'CHG',
        'entity_type_cd': 'RLC',
        'requestTypeCd': 'CLC'
    }

    for key, value in expected_field_values.items():
        assert_field_equals_value(patched_nr, key, value)


def test_draft_patch_edit_and_repatch(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = build_test_input_fields()
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    # Add another name to the mix
    nr_data = {
        'names': draft_nr.get('names'),
        'applicants': draft_nr.get('applicants')
    }

    added_names = [
        {
            'name': 'BLUE HERON ADVENTURE TOURS LTD.',
            'choice': 2,
            'designation': 'LTD.',
            'name_type_cd': 'CO',
            'consent_words': '',
            'conflict1': 'BLUE HERON TOURS LTD.',
            'conflict1_num': '0515211'
        },
        {
            'name': 'BLUE HERON ISLAND TOURS LTD.',
            'choice': 3,
            'designation': 'LTD.',
            'name_type_cd': 'CO',
            'consent_words': '',
            'conflict1': 'BLUE HERON TOURS LTD.',
            'conflict1_num': '0515211'
        }
    ]

    nr_data['names'].extend(added_names)

    # updated_applicant = {}

    # nr_data['applicant'] = updated_applicant

    patch_response = patch_nr(client, NameRequestActions.EDIT.value, draft_nr.get('id'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response #1: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    assert patched_nr.get('stateCd') == 'PENDING_PAYMENT'

    # TODO: Check applicant(s)

    # Check names
    assert_names_are_mapped_correctly(nr_data.get('names'), patched_nr.get('names'))

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')

    # Check actions (write a util for this)

    """
    Patch the NR again with the response to make sure everything runs as expected
    """

    patch_response = patch_nr(client, NameRequestActions.EDIT.value, patched_nr.get('id'), patched_nr)
    patched_nr = json.loads(patch_response.data)

    re_patched_nr = json.loads(patch_response.data)
    assert re_patched_nr is not None

    print('PATCH Response #2: \n' + json.dumps(re_patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    assert re_patched_nr.get('stateCd') == 'PENDING_PAYMENT'

    # TODO: Check applicant(s)

    # Check names
    assert_names_are_mapped_correctly(patched_nr.get('names'), re_patched_nr.get('names'))

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')


def test_draft_patch_upgrade(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = build_test_input_fields()
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None
    assert_field_equals_value(draft_nr, 'priorityCd', 'N')

    # Take the response and edit it
    nr_data = {}
    patch_response = patch_nr(client, NameRequestActions.UPGRADE.value, draft_nr.get('id'), nr_data)

    assert patch_response.status_code == 200
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    assert patched_nr.get('stateCd') == State.PENDING_PAYMENT

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')

    # Check actions (write a util for this)

    # assert_field_equals_value(patched_nr, 'payment_token', '')
    assert_field_equals_value(patched_nr, 'priorityCd', 'Y')
    # assert_field_equals_value(patched_nr, 'priorityDate', '')


def test_draft_patch_cancel(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = build_test_input_fields()

    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    nr_data = {}
    patch_response = patch_nr(client, NameRequestActions.CANCEL.value, draft_nr.get('id'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == CANCELLED: ' + str(bool(patched_nr.get('stateCd') == 'CANCELLED')))
    assert patched_nr.get('stateCd') == State.CANCELLED

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')

    # Check actions (write a util for this)


@pytest.mark.skip
def test_draft_patch_cancel_with_invalid_states(client, jwt, app):
    """
    TODO: This isn't working finish it!
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = build_test_input_fields()
    custom_names = [{
        'name': 'BLUE HERON TOURS LTD.',
        'choice': 1,
        'designation': 'LTD.',
        'name_type_cd': 'CO',
        'consent_words': '',
        'conflict1': 'BLUE HERON TOURS LTD.',
        'conflict1_num': '0515211',
        # Custom name has a corp num to make it 'consumed'
        'corpNum': '12345'
    }]

    input_fields['names'] = custom_names

    test_nr = create_approved_nr(client, input_fields)
    assert test_nr is not None

    # Take the response and edit it
    # Expect this to fail as we
    nr_data = {}
    patch_response = patch_nr(client, NameRequestActions.CANCEL.value, test_nr.get('id'), nr_data)

    # Ensure the request failed
    print('Assert that the request failed: ' + str(bool(patch_response.status_code == 500)))

    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    # There should be an error message in the response
    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')
    assert isinstance(patched_nr.get('message'), str)


def test_draft_patch_cancel_with_consumed_name(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = build_test_input_fields()
    custom_names = [{
        'name': 'BLUE HERON TOURS LTD.',
        'choice': 1,
        'designation': 'LTD.',
        'name_type_cd': 'CO',
        'consent_words': '',
        'conflict1': 'BLUE HERON TOURS LTD.',
        'conflict1_num': '0515211',
        # Custom name has a corp num to make it 'consumed'
        'corpNum': '12345'
    }]

    input_fields['names'] = custom_names

    test_nr = create_approved_nr(client, input_fields)
    assert test_nr is not None

    # Take the response and edit it
    # Expect this to fail as we
    nr_data = {}
    patch_response = patch_nr(client, NameRequestActions.CANCEL.value, test_nr.get('id'), nr_data)

    # Ensure the request failed
    print('Assert that the request failed: ' + str(bool(patch_response.status_code == 500)))

    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    # There should be an error message in the response
    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')
    assert isinstance(patched_nr.get('message'), str)


def test_draft_patch_cancel_with_expired_nr(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = build_test_input_fields()

    # Set the expirationDate to a previous day
    input_fields['expirationDate'] = datetime.date.today() - datetime.timedelta(days=2)

    custom_names = [{
        'name': 'BLUE HERON TOURS LTD.',
        'choice': 1,
        'designation': 'LTD.',
        'name_type_cd': 'CO',
        'consent_words': '',
        'conflict1': 'BLUE HERON TOURS LTD.',
        'conflict1_num': '0515211',
    }]

    input_fields['names'] = custom_names

    test_nr = create_approved_nr(client, input_fields)
    assert test_nr is not None

    # Take the response and edit it
    # Expect this to fail as we
    nr_data = {}
    patch_response = patch_nr(client, NameRequestActions.CANCEL.value, test_nr.get('id'), nr_data)

    # Ensure the request failed
    print('Assert that the request failed: ' + str(bool(patch_response.status_code == 500)))

    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    # There should be an error message in the response
    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')
    assert isinstance(patched_nr.get('message'), str)


def test_draft_patch_refund(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = build_test_input_fields()
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    nr_data = {}
    patch_response = patch_nr(client, NameRequestActions.REQUEST_REFUND.value, draft_nr.get('id'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    assert patched_nr.get('stateCd') == State.REFUND_REQUESTED

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')


def test_draft_patch_reapply(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = build_test_input_fields()
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    def do_reapply():
        # Take the response and edit it
        nr_data = {}
        patch_response = patch_nr(client, NameRequestActions.REAPPLY.value, draft_nr.get('id'), nr_data)

        updated_nr = None
        if patch_response.status_code == 200:
            updated_nr = json.loads(patch_response.data)
            assert updated_nr is not None

            print('PATCH Response: \n' + json.dumps(updated_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

        return updated_nr, patch_response.status_code

    # Re-apply
    patched_nr, status_code = do_reapply()

    # Check state
    assert patched_nr.get('stateCd') == draft_nr.get('stateCd')

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')

    assert_field_equals_value(patched_nr, 'submitCount', 2)
    # assert_field_equals_value(patched_nr, 'expirationDate', '')

    # Re-apply
    patched_nr, status_code = do_reapply()

    assert_field_equals_value(patched_nr, 'submitCount', 3)

    # Re-apply
    patched_nr, status_code = do_reapply()
    # The submitCount should never be greater than 3, this should now fail with a 500
    assert status_code == 500


def test_draft_patch_reapply_historical(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = build_test_input_fields()
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    nr_data = {
        'request_action_cd': 'REH'
    }

    patch_response = patch_nr(client, NameRequestActions.REAPPLY.value, draft_nr.get('id'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    assert patched_nr.get('stateCd') == draft_nr.get('stateCd')

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')

    assert_field_is_lt_value(patched_nr, 'submitCount', 4)
    # assert_field_equals_value(patched_nr, 'expirationDate', '')

    # Take the response and edit it
    nr_data = {
        'request_action_cd': 'REST'
    }

    patch_response = patch_nr(client, NameRequestActions.REAPPLY.value, draft_nr.get('id'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    assert patched_nr.get('stateCd') == draft_nr.get('stateCd')

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')

    assert_field_is_lt_value(patched_nr, 'submitCount', 4)
    # assert_field_equals_value(patched_nr, 'expirationDate', '')


def test_draft_patch_resend(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    # Define our data
    input_fields = build_test_input_fields()
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    nr_data = {}
    patch_response = patch_nr(client, NameRequestActions.RESEND.value, draft_nr.get('id'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == draft_nr.get('stateCd')

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')


draft_input_fields = {
	'applicants': [
		{
			'addrLine1': '123-1640 Electra Blvd',
			'addrLine2': None,
			'addrLine3': None,
			'city': 'North Saanich',
			'clientFirstName': None,
			'clientLastName': None,
			'contact': '',
			'countryTypeCd': 'CA',
			'declineNotificationInd': None,
			'emailAddress': 'a@a.com',
			'faxNumber': None,
			'firstName': 'John',
			'lastName': 'Doe',
			'middleName': None,
			'partyId': '', # must be empty
			'phoneNumber': '1234567',
			'postalCd': 'V8L 5V4',
			'stateProvinceCd': 'BC'
		}
	],
	'names': [
		{
			'choice': 1,
			'consent_words': '',
			'conflict1': '',
			'conflict1_num': '',
			'designation': 'CORP.',
			'name': 'TESTING CORP.',
			'name_type_cd': 'CO'
		}
	],
	'additionalInfo': '*** Additional Info here ***',
	'natureBusinessInfo': 'Tests',
	'priorityCd': 'N',
	'entity_type_cd': '',
	'request_action_cd': '',
	'stateCd': 'DRAFT',
	'english': True,
	'nameFlag': False,
	'submit_count': 0,
	'corpNum': '',
	'homeJurisNum': ''
}


@pytest.mark.parametrize('test_name, request_action_cd, entity_type_cd', [
    ('New CR', 'NEW', EntityTypes.CORPORATION.value),
    ('New BC', 'NEW', EntityTypes.BENEFIT_COMPANY.value),
    ('Resubmit CR', 'RESUBMIT', EntityTypes.CORPORATION.value),
    ('Resubmit BC', 'RESUBMIT', EntityTypes.BENEFIT_COMPANY.value),
])
def test_temp_nr(client, test_name, request_action_cd, entity_type_cd):
    """
    Test temp NRs
    """
    draft_input_fields['request_action_cd'] = request_action_cd
    draft_input_fields['entity_type_cd'] = entity_type_cd

    add_test_user_to_db()

    path = build_request_uri(API_BASE_URI, '')
    headers = get_test_headers()
    post_response = client.post(path, data=json.dumps(draft_input_fields), headers=headers)
    draft_nr = json.loads(post_response.data)

    assert draft_nr['id'] > 0
    assert draft_nr['nrNum'].startswith('NR L')
    assert draft_nr['request_action_cd'] == request_action_cd
    assert draft_nr['entity_type_cd'] == entity_type_cd
    assert draft_nr['applicants']['firstName'] == 'John'
