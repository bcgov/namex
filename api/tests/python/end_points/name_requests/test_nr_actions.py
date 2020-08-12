"""
Integration tests for Name Request state transitions.
"""
import pytest
import json

from tests.python.end_points.common.http import build_test_query, build_request_uri
from tests.python.end_points.common.logging import log_request_path

from tests.python.unit.test_setup_utils import build_nr
from tests.python.end_points.common.http import get_test_headers
# Import token and claims if you need it
# from tests.python.end_points.common.configuration import claims, token_header

from .configuration import API_BASE_URI
from tests.python.common.test_name_request_utils import \
    pick_name_from_list, assert_name_has_name, assert_name_has_id, assert_field_is_mapped, assert_field_equals_value, assert_field_is_lt_value

from namex.models import State, User
from namex.constants import NameRequestActions

"""
Add states
DRAFT - Unexamined name, submitted by a client
INPROGRESS - An examiner is working on this request
CANCELLED - The request is cancelled and cannot be changed
HOLD - A name approval was halted for some reason
APPROVED - Approved request, this is a final state
REJECTED - Rejected request, this is a final state
CONDITIONAL - Approved, but with conditions to be met. This is a final state
HISTORICAL - HISTORICAL
COMPLETED - COMPLETED - LEGACY state for completed NRs from NRO
EXPIRED	EXPIRED - LEGACY state for expired NRs from NRO
NRO_UPDATING - Internal state used when updating records from NRO
COND-RESERVE Temporary reserved state with consent required
RESERVED - Temporary reserved state between name available and paid.  Once paid it is set to APPROVED or CONDITIONAL approval.
"""

state_data = [
    # ('DRAFT', 'Unexamined name, submitted by a client'),
    # ('INPROGRESS', 'An examiner is working on this request'),
    # ('CANCELLED', 'The request is cancelled and cannot be changed'),
    # ('HOLD', 'A name approval was halted for some reason'),
    # ('APPROVED', 'Approved request, this is a final state'),
    # ('REJECTED', 'Rejected request, this is a final state'),
    # ('CONDITIONAL', 'Approved, but with conditions to be met. This is a final state'),
    # ('HISTORICAL', 'HISTORICAL'),
    # ('COMPLETED', 'COMPLETED - LEGACY state for completed NRs from NRO'),
    # ('EXPIRED', 'EXPIRED - LEGACY state for expired NRs from NRO'),
    # ('NRO_UPDATING', 'NRO_UPDATING - internal state used when updating records from NRO'),
    # TODO: These states are missing in Test DB
    ('COND-RESERVE', 'Temporary reserved state with consent required'),
    ('RESERVED', 'Temporary reserved state between name available and paid.  Once paid it is set to APPROVED or CONDITIONAL approval.')
]

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
def add_states_to_db(states):
    for code, desc in states:
        state = State(cd=code, description=desc)
        state.save_to_db()


@pytest.mark.skip
def add_test_user_to_db():
    user = User(username='name_request_service_account', firstname='Test', lastname='User', sub='idir/name_request_service_account', iss='keycloak')
    user.save_to_db()


@pytest.mark.skip
def create_draft_nr(client, nr_data=None):
    """
    Create a draft NR, using the API, to use as the initial state for each test.
    :param client:
    :param nr_data:
    :return:
    """
    try:
        # Configure auth
        # token, headers = setup_test_token(jwt, claims, token_header)
        headers = get_test_headers()

        # Set up our test data
        add_states_to_db(state_data)
        add_test_user_to_db()

        # Optionally supply the field data
        nr = build_nr(State.DRAFT, nr_data)

        nr_data = nr.json()

        nr_data['applicants'] = [{
            'addrLine1': '1796 KINGS RD',
            'addrLine2': '',
            'addrLine3': '',
            'city': 'VICTORIA',
            'clientFirstName': '',
            'clientLastName': '',
            'contact': '',
            'countryTypeCd': 'CA',
            # 'declineNotificationInd': None,
            'emailAddress': 'bob.johnson@example.com',
            'faxNumber': '',
            'firstName': 'BOB',
            'lastName': 'JOHNSON',
            'middleName': '',
            # 'partyId': None,
            'phoneNumber': '2505320083',
            'postalCd': 'V8R 2P1',
            'stateProvinceCd': 'BC'

        }]

        nr_data['names'] = [{
            'name': 'BLUE HERON TOURS LTD.',
            'choice': 1,
            'designation': 'LTD.',
            'name_type_cd': 'CO',
            'consent_words': '',
            'conflict1': 'BLUE HERON TOURS LTD.',
            'conflict1_num': '0515211'
        }]

        # Create a new DRAFT NR using the NR we just created
        request_uri = API_BASE_URI
        test_params = [{}]

        query = build_test_query(test_params)
        path = build_request_uri(request_uri, query)
        log_request_path(path)

        post_response = client.post(path, data=json.dumps(nr_data), headers=headers)

        if not post_response or post_response.status_code != 201:
            raise Exception('NR POST operation failed, cannot continue with PATCH test')

        return post_response
    except Exception as err:
        print(repr(err))


@pytest.mark.skip
def patch_nr(client, action, nr_num, nr_data):
    try:
        request_uri = API_BASE_URI + nr_num + '/' + action
        test_params = [{}]

        headers = get_test_headers()
        query = build_test_query(test_params)
        path = build_request_uri(request_uri, query)
        print('Patch (' + action + ') Name Request [' + nr_num + ']: \n' + json.dumps(nr_data, sort_keys=True, indent=4, separators=(',', ': ')))
        log_request_path(path)

        patch_response = client.patch(path, data=json.dumps(nr_data), headers=headers)

        if not patch_response or patch_response.status_code != 200:
            # raise Exception('NR PATCH operation failed')
            pass

        return patch_response
    except Exception as err:
        print(repr(err))
        raise


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
    input_fields = draft_input_fields
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
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

    # updated_applicant = {}

    # nr_data['applicant'] = updated_applicant

    patch_response = patch_nr(client, NameRequestActions.EDIT.value, draft_nr.get('nrNum'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == 'DRAFT'

    # Check names
    assert_names_are_mapped_correctly(nr_data.get('names'), patched_nr.get('names'))

    # Check data
    expected_field_values = {
        'additionalInfo': 'Testing additional info',
        'consentFlag': None,
        'consent_dt': None,
        'corpNum': 'TESTCORP123',
        # 'homeJurisNum': 'TESTHOME123',
        'entity_type_cd': 'FR',
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
        'requestTypeCd': 'CR',
        'request_action_cd': 'NEW',
        'source': 'NAMEREQUEST',
        'state': 'DRAFT',
        'stateCd': 'DRAFT',
        'submitCount': 1,
        # 'submittedDate': None,
        'submitter_userid': 'name_request_service_account',
        'userId': 'name_request_service_account',
        'xproJurisdiction': ''
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
    input_fields = draft_input_fields
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

    patch_response = patch_nr(client, NameRequestActions.EDIT.value, draft_nr.get('nrNum'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response #1: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == 'DRAFT'

    # TODO: Check applicant(s)

    # Check names
    assert_names_are_mapped_correctly(nr_data.get('names'), patched_nr.get('names'))

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')

    # Check actions (write a util for this)

    """
    Patch the NR again with the response to make sure everything runs as expected
    """

    patch_response = patch_nr(client, NameRequestActions.EDIT.value, patched_nr.get('nrNum'), patched_nr)
    patched_nr = json.loads(patch_response.data)

    re_patched_nr = json.loads(patch_response.data)
    assert re_patched_nr is not None

    print('PATCH Response #2: \n' + json.dumps(re_patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(re_patched_nr.get('stateCd') == 'DRAFT')))
    assert re_patched_nr.get('stateCd') == 'DRAFT'

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
    input_fields = draft_input_fields
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    nr_data = {}
    patch_response = patch_nr(client, NameRequestActions.UPGRADE.value, draft_nr.get('nrNum'), nr_data)

    assert patch_response.status_code == 200
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == State.DRAFT

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
    input_fields = draft_input_fields
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    nr_data = {}
    patch_response = patch_nr(client, NameRequestActions.CANCEL.value, draft_nr.get('nrNum'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == CANCELLED: ' + str(bool(patched_nr.get('stateCd') == 'CANCELLED')))
    assert patched_nr.get('stateCd') == State.CANCELLED

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')

    # Check actions (write a util for this)


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
    input_fields = draft_input_fields
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    nr_data = {}
    patch_response = patch_nr(client, NameRequestActions.REFUND.value, draft_nr.get('nrNum'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == State.DRAFT

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
    input_fields = draft_input_fields
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    def do_reapply():
        # Take the response and edit it
        nr_data = {}
        patch_response = patch_nr(client, NameRequestActions.REAPPLY.value, draft_nr.get('nrNum'), nr_data)

        updated_nr = None
        if patch_response.status_code == 200:
            updated_nr = json.loads(patch_response.data)
            assert updated_nr is not None

            print('PATCH Response: \n' + json.dumps(updated_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

        return updated_nr, patch_response.status_code

    # Re-apply
    patched_nr, status_code = do_reapply()

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == State.DRAFT

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
    input_fields = draft_input_fields
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    nr_data = {
        'request_action_cd': 'REH'
    }

    patch_response = patch_nr(client, NameRequestActions.REAPPLY.value, draft_nr.get('nrNum'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == State.DRAFT

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')

    assert_field_is_lt_value(patched_nr, 'submitCount', 4)
    # assert_field_equals_value(patched_nr, 'expirationDate', '')

    # Take the response and edit it
    nr_data = {
        'request_action_cd': 'REST'
    }

    patch_response = patch_nr(client, NameRequestActions.REAPPLY.value, draft_nr.get('nrNum'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == State.DRAFT

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
    input_fields = draft_input_fields
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    nr_data = {}
    patch_response = patch_nr(client, NameRequestActions.RESEND.value, draft_nr.get('nrNum'), nr_data)
    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    print('PATCH Response: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == State.DRAFT

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')
