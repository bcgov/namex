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
from tests.python.end_points.common.configuration import claims, token_header

from .configuration import API_BASE_URI

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


def pick_name_from_list(names, name):
    matches = [n for n in names if n.get('name') == name]
    if len(matches) == 0:
        return None
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise Exception('More than one match for a name!')


@pytest.mark.skip
def assert_name_has_name(name):
    """
    Just a util
    :param name:
    :return:
    """
    assert name is not None
    assert name.get('name') is not None


@pytest.mark.skip
def assert_name_has_id(name):
    """
    Just a util
    :param name:
    :return:
    """
    assert name.get('id') is not None


@pytest.mark.skip
def assert_field_is_mapped(req_obj, res_obj, prop_name):
    """
    Just a util
    :param req_obj:
    :param res_obj:
    :param prop_name:
    :return:
    """
    req_obj_val = req_obj.get(prop_name)
    res_obj_val = res_obj.get(prop_name)
    print('Request Field [' + prop_name + ': ' + str(req_obj_val) + '] equals Response Field [' + prop_name + ': ' + str(res_obj_val) + ']')
    assert req_obj_val == res_obj_val
    print('OK')


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
def create_draft_nr(client, jwt, app):
    """
    Create a draft NR, using the API, to use as the initial state for each test.
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    try:
        # Configure auth
        # token, headers = setup_test_token(jwt, claims, token_header)
        headers = get_test_headers()

        # Set up our test data
        add_states_to_db(state_data)
        add_test_user_to_db()

        nr = build_nr(State.DRAFT)
        # nr.requestTypeCd = 'CR'

        nr_data = nr.json()

        nr_data['names'] = [{
            "name": "BLUE HERON TOURS LTD.",
            "choice": 1,
            "designation": "LTD.",
            "name_type_cd": "CO",
            "consent_words": "",
            "conflict1": "BLUE HERON TOURS LTD.",
            "conflict1_num": "0515211"
        }]

        # New requests need to have these set
        nr_data['additionalInfo'] = ''
        nr_data['corpNum'] = ''
        nr_data['homeJurisNum'] = ''
        nr_data['natureBusinessInfo'] = 'Test'
        nr_data['previousRequestId'] = ''
        nr_data['tradeMark'] = ''
        nr_data['xproJurisdiction'] = ''
        nr_data['priorityCd'] = 'N'
        nr_data['entity_type'] = 'CR'
        nr_data['request_action'] = 'NEW'
        nr_data['stateCd'] = 'DRAFT'
        nr_data['english'] = True
        nr_data['nameFlag'] = False
        nr_data['submit_count'] = 0

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


def test_draft_patch_edit(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    post_response = create_draft_nr(client, jwt, app)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    print('Patching DRAFT: \n' + json.dumps(draft_nr, sort_keys=True, indent=4, separators=(',', ': ')))

    # Take the response and edit it
    request_uri = API_BASE_URI + draft_nr.get('nrNum') + '/' + NameRequestActions.EDIT.value
    test_params = [{}]

    headers = get_test_headers()
    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    # Add another name to the mix
    nr_data = {
        'names': draft_nr.get('names')
    }

    added_names = [
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

    nr_data['names'].extend(added_names)

    print('PATCH Request #1: \n' + json.dumps(nr_data, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')
    patch_response = client.patch(path, data=json.dumps(nr_data), headers=headers)

    if not patch_response or patch_response.status_code != 200:
        raise Exception('NR PATCH operation failed')

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

    print('PATCH Request #2: \n' + json.dumps(patched_nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')
    patch_response = client.patch(path, data=json.dumps(patched_nr), headers=headers)

    if not patch_response or patch_response.status_code != 200:
        raise Exception('NR PATCH operation failed')

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
    post_response = create_draft_nr(client, jwt, app)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    request_uri = API_BASE_URI + draft_nr.get('nrNum') + '/' + NameRequestActions.UPGRADE.value
    test_params = [{}]

    headers = get_test_headers()
    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    patch_response = client.patch(path, data=json.dumps({}), headers=headers)

    if not patch_response or patch_response.status_code != 200:
        raise Exception('NR PATCH operation failed')

    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == State.DRAFT

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')

    # Check actions (write a util for this)

    # TODO: Priority CD changes here! (Will be set to Y)
    # TODO: Setting priority date, (today's date in UTC)
    # Note: This is not designed to test for payment


def test_draft_patch_cancel(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    post_response = create_draft_nr(client, jwt, app)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    request_uri = API_BASE_URI + draft_nr.get('nrNum') + '/' + NameRequestActions.CANCEL.value
    test_params = [{}]

    headers = get_test_headers()
    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    patch_response = client.patch(path, data=json.dumps({}), headers=headers)

    if not patch_response or patch_response.status_code != 200:
        raise Exception('NR PATCH operation failed')

    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

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
    post_response = create_draft_nr(client, jwt, app)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    request_uri = API_BASE_URI + draft_nr.get('nrNum') + '/' + NameRequestActions.REFUND.value
    test_params = [{}]

    headers = get_test_headers()
    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    patch_response = client.patch(path, data=json.dumps({}), headers=headers)

    if not patch_response or patch_response.status_code != 200:
        raise Exception('NR PATCH operation failed')

    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

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
    post_response = create_draft_nr(client, jwt, app)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    request_uri = API_BASE_URI + draft_nr.get('nrNum') + '/' + NameRequestActions.REAPPLY.value
    test_params = [{}]

    headers = get_test_headers()
    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    patch_response = client.patch(path, data=json.dumps({}), headers=headers)

    # TODO: Assert that this fails! We should NOT be able to run this from a DRAFT
    if not patch_response or patch_response.status_code != 200:
        raise Exception('NR PATCH operation failed')

    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == State.DRAFT

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')

    # TODO:
    # TODO: Check submit count < 4
    # TODO: Expiry date extended by 1 yr + 56 or 56 days
    # TODO: Make sure not state change and also make sure nrNum is the same


def test_draft_patch_resend(client, jwt, app):
    """
    Setup:
    Test:
    :param client:
    :param jwt:
    :param app:
    :return:
    """
    post_response = create_draft_nr(client, jwt, app)

    # Assign the payload to new nr var
    draft_nr = json.loads(post_response.data)
    assert draft_nr is not None

    # Take the response and edit it
    request_uri = API_BASE_URI + draft_nr.get('nrNum') + '/' + NameRequestActions.RESEND.value
    test_params = [{}]

    headers = get_test_headers()
    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    patch_response = client.patch(path, data=json.dumps({}), headers=headers)

    # TODO: Ensure this notification is resent
    if not patch_response or patch_response.status_code != 200:
        raise Exception('NR PATCH operation failed')

    patched_nr = json.loads(patch_response.data)
    assert patched_nr is not None

    # Check state
    print('Assert that stateCd == DRAFT: ' + str(bool(patched_nr.get('stateCd') == 'DRAFT')))
    assert patched_nr.get('stateCd') == State.DRAFT

    # Check NR number is the same because these are PATCH and call change_nr
    assert_field_is_mapped(draft_nr, patched_nr, 'nrNum')
