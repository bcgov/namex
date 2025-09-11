"""
Test helpers for Name Requests.
"""

import json

import pytest

from namex.models import State, User

from ....common.test_name_request_utils import (assert_applicant_has_id,
                                                assert_field_is_mapped,
                                                assert_name_has_id,
                                                assert_name_has_name,
                                                pick_name_from_list)
from ....end_points.common.http import (build_request_uri, build_test_query,
                                        get_test_headers)
from ....end_points.common.logging import log_request_path
from ....unit.test_setup_utils import build_nr
from ...common import claims, token_header
from ...common.http import setup_test_token
# Import token and claims if you need it
# from tests.python.end_points.common.configuration import claims, token_header
from ..configuration import API_BASE_URI

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
    (
        'RESERVED',
        'Temporary reserved state between name available and paid.  Once paid it is set to APPROVED or CONDITIONAL approval.',
    ),
]


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
        assert_field_is_mapped(req_name, res_name, 'designation')
        print('\n......................................\n')

    print('\n-------- Test names complete --------\n')


def assert_applicant_is_mapped_correctly(req_applicant, res_applicant):
    print('\n-------- Test applicant --------\n')
    print('\nCompare request applicant: \n' + repr(req_applicant) + '\n')
    print('With response applicant: \n' + repr(res_applicant) + '\n')

    if res_applicant and req_applicant.get('partyId', None) is None:
        # It's a new applicant make sure it has an ID set
        assert_applicant_has_id(res_applicant)
    if res_applicant and req_applicant.get('partyId', None) is not None:
        # The applicant existed, make sure the ID has not changed
        assert_field_is_mapped(req_applicant, res_applicant, 'partyId')

    print('\n-------- Test applicant complete --------\n')


def add_states_to_db(states):
    """Add states to database only if they don't already exist."""
    for code, desc in states:
        # Check if state already exists (migrations may have loaded it)
        existing_state = State.query.filter_by(cd=code).first()
        if not existing_state:
            state = State(cd=code, description=desc)
            state.save_to_db()


def add_test_user_to_db():
    """Create or get the service account user expected by the API."""
    # The API expects this specific username
    expected_username = 'name_request_service_account'

    # Check if user already exists
    existing_user = User.query.filter_by(username=expected_username).first()
    if existing_user:
        return existing_user

    # Create the expected service account user
    user = User(
        username=expected_username,
        firstname='Test',
        lastname='User',
        sub='idir/name_request_service_account',
        iss='keycloak',
        idp_userid='123',
        login_source='IDIR',
    )

    try:
        user.save_to_db()
        return user
    except Exception:
        # If there's a conflict, try to fetch the existing user again
        # This can happen in concurrent test runs
        existing_user = User.query.filter_by(username=expected_username).first()
        if existing_user:
            return existing_user
        raise


def create_approved_nr(client, nr_data=None):
    return create_test_nr(nr_data, State.APPROVED)


def create_cancelled_nr(client, nr_data=None):
    return create_test_nr(nr_data, State.CANCELLED)


def create_expired_nr(client, nr_data=None):
    return create_test_nr(nr_data, State.EXPIRED)


def create_consumed_nr(client, nr_data=None):
    return create_test_nr(nr_data, State.CONSUMED)


def create_draft_nr(client, nr_data=None, use_api=True):
    """
    You can optionally set the use_api param to False to create an NR using model persistence as opposed to the API!
    :param client:
    :param nr_data:
    :param use_api:
    :return:
    """
    if use_api:
        return post_test_nr(client, nr_data, State.DRAFT)

    return create_test_nr(nr_data, State.DRAFT)


def create_test_nr(nr_data=None, nr_state=State.DRAFT):
    """
    Create a draft NR and persist (NOT using the API) to use as the initial state for each test.
    :param nr_data:
    :param nr_state:
    :return:
    """
    try:
        # Set up our test data
        add_states_to_db(state_data)
        user = add_test_user_to_db()

        # Optionally supply the field data
        custom_names = nr_data.get('names', None)
        if not custom_names:
            custom_names = [
                {
                    'name': 'BLUE HERON TOURS LTD.',
                    'choice': 1,
                    'designation': 'LTD.',
                    'name_type_cd': 'CO',
                    'consent_words': '',
                    'conflict1': 'BLUE HERON TOURS LTD.',
                    'conflict1_num': '0515211',
                }
            ]

        nr = build_nr(nr_state, nr_data, custom_names, False)

        # Set any missing fields
        # TODO: We may want to add this stuff to build_nr
        nr.userId = user.id
        nr.activeUser = user
        nr.submitter = user
        nr.submitter_userid = user.id
        # Generate unique NR number using timestamp to prevent conflicts (max 10 chars)
        import time
        unique_suffix = str(int(time.time()))[-6:]  # Last 6 digits of timestamp
        nr.nrNum = f'NR {unique_suffix}'

        nr.save_to_db()

        return nr
    except Exception as err:
        print(repr(err))


def post_test_nr(client, nr_data=None, nr_state=State.DRAFT):
    """
    Create a draft NR, using the API, to use as the initial state for each test.
    :param client:
    :param nr_data:
    :param nr_state:
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
        custom_names = nr_data.get('names', None)
        if not custom_names:
            custom_names = [
                {
                    'name': 'BLUE HERON TOURS LTD.',
                    'choice': 1,
                    'designation': 'LTD.',
                    'name_type_cd': 'CO',
                    'consent_words': '',
                    'conflict1': 'BLUE HERON TOURS LTD.',
                    'conflict1_num': '0515211',
                }
            ]

        nr = build_nr(nr_state, nr_data, custom_names, False)

        nr_data = nr.json()

        nr_data['applicants'] = [
            {
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
                'stateProvinceCd': 'BC',
            }
        ]

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
def post_test_nr_json(client, nr_data=None):
    """
    Create a temp NR with nr data passed.
    """
    try:
        add_states_to_db(state_data)
        add_test_user_to_db()
        request_uri = API_BASE_URI
        path = build_request_uri(request_uri, '')
        headers = get_test_headers()
        post_response = client.post(path, data=json.dumps(nr_data), headers=headers)

        if not post_response or post_response.status_code != 201:
            raise Exception('Temp NR POST operation failed, cannot continue with test')

        return post_response
    except Exception as err:
        print(repr(err))


@pytest.mark.skip
def patch_nr(client, action, nr_id, nr_data, mocker):
    try:
        access_mock = mocker.patch('namex.resources.name_requests.name_request.full_access_to_name_request')
        access_mock.return_value = True
        refundable_mock = mocker.patch('namex.resources.name_requests.name_request.is_name_request_refundable')
        refundable_mock.return_value = True

        request_uri = API_BASE_URI + str(nr_id) + '/' + action
        test_params = [{}]

        headers = get_test_headers()
        query = build_test_query(test_params)
        path = build_request_uri(request_uri, query)
        print(
            'Patch ('
            + action
            + ') Name Request ['
            + str(nr_id)
            + ']: \n'
            + json.dumps(nr_data, sort_keys=True, indent=4, separators=(',', ': '))
        )
        log_request_path(path)

        patch_response = client.patch(path, data=json.dumps(nr_data), headers=headers)

        if not patch_response or patch_response.status_code != 200:
            # raise Exception('NR PATCH operation failed')
            pass

        return patch_response
    except Exception as err:
        print(repr(err))
        raise


@pytest.mark.skip
def get_nr(client, nr_id, jwt):
    try:
        request_uri = API_BASE_URI + str(nr_id)
        test_params = [{'org_id': '1234'}]

        _, headers = setup_test_token(jwt, claims, token_header)
        query = build_test_query(test_params)
        path = build_request_uri(request_uri, query)
        print('Get Name Request [' + str(nr_id) + ']')
        log_request_path(path)

        get_response = client.get(path, headers=headers)

        if not get_response or get_response.status_code != 200:
            # raise Exception('NR PATCH operation failed')
            pass

        return get_response
    except Exception as err:
        print(repr(err))
        raise
