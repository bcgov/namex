"""
Integration tests for Name Request state transitions.
"""
import datetime
import json

from tests.python.common.test_name_request_utils import \
    assert_field_is_mapped, assert_list_contains_exactly

from .test_setup_utils.test_helpers import \
    create_test_nr, get_nr

from namex.models import State
from namex.constants import NameRequestActions


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
    input_fields = build_test_input_fields()

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
    assert_list_contains_exactly(actions, [
        NameRequestActions.EDIT.value,
        # TODO: Upgrade only should show up if priorityCd has not already been set to 'Y'
        NameRequestActions.UPGRADE.value,
        # TODO: Spreadsheet conflicts with task
        # TODO: Show refund action ONLY if there is an existing payment!
        # NameRequestActions.REQUEST_REFUND.value,
        # TODO: Show receipt action ONLY if there is an existing payment!
        # NameRequestActions.RECEIPT.value
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
    input_fields = build_test_input_fields()

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
    assert_list_contains_exactly(actions, [
        NameRequestActions.EDIT.value,
        NameRequestActions.CANCEL.value,
        # TODO: Show receipt action ONLY if there is an existing payment!
        # NameRequestActions.RECEIPT.value,
        # TODO: Add logic to test 5 days / expiry
        # NameRequestActions.REAPPLY.value,
        NameRequestActions.RESEND.value
    ])


def test_approved_and_expired_response_actions(client, jwt, app):
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

    # Set the expirationDate to a previous day
    input_fields['expirationDate'] = datetime.date.today() - datetime.timedelta(days=2)

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
    assert_list_contains_exactly(actions, [
        NameRequestActions.EDIT.value,
        # TODO: Show receipt action ONLY if there is an existing payment!
        # NameRequestActions.RECEIPT.value,
        NameRequestActions.REAPPLY.value,
        NameRequestActions.RESEND.value
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
    input_fields = build_test_input_fields()

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
    assert_list_contains_exactly(actions, [
        NameRequestActions.EDIT.value,
        NameRequestActions.CANCEL.value,
        # TODO: Show receipt action ONLY if there is an existing payment!
        # NameRequestActions.RECEIPT.value,
        # TODO: Add logic to test 5 days / expiry
        # NameRequestActions.REAPPLY.value,
        NameRequestActions.RESEND.value
    ])


def test_conditional_and_expired_response_actions(client, jwt, app):
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

    # Set the expirationDate to a previous day, set to less than 5 so we get the REAPPLY option
    input_fields['expirationDate'] = datetime.date.today() - datetime.timedelta(days=2)

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
    assert_list_contains_exactly(actions, [
        NameRequestActions.EDIT.value,
        # TODO: Show receipt action ONLY if there is an existing payment!
        # NameRequestActions.RECEIPT.value,
        NameRequestActions.REAPPLY.value,
        NameRequestActions.RESEND.value
    ])


def test_consumed_and_conditional_response_actions(client, jwt, app):
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
    assert_list_contains_exactly(actions, [
        NameRequestActions.EDIT.value,
        # TODO: Show receipt action ONLY if there is an existing payment!
        # NameRequestActions.RECEIPT.value,
        NameRequestActions.RESEND.value
    ])


def test_consumed_and_approved_response_actions(client, jwt, app):
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
    assert_list_contains_exactly(actions, [
        NameRequestActions.EDIT.value,
        # TODO: Show receipt action ONLY if there is an existing payment!
        # NameRequestActions.RECEIPT.value,
        NameRequestActions.RESEND.value
    ])


def test_rejected_response_actions(client, jwt, app):
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

    # Assign the payload to new nr var
    test_nr = create_test_nr(input_fields, State.REJECTED)
    assert test_nr is not None

    # Grab the record using the API
    get_response = get_nr(client, test_nr.get('id'))
    nr = json.loads(get_response.data)
    assert nr is not None

    print('PATCH Response: \n' + json.dumps(nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == REJECTED: ' + str(bool(nr.get('stateCd') == 'REJECTED')))
    assert nr.get('stateCd') == State.REJECTED

    assert_field_is_mapped(test_nr, nr, 'nrNum')

    # Check actions
    actions = nr.get('actions')
    assert_list_contains_exactly(actions, [
        NameRequestActions.EDIT.value,  # TODO: Make sure we can only edit contact info somehow as part of this test
        # TODO: Show receipt action ONLY if there is an existing payment!
        # NameRequestActions.RECEIPT.value,
        NameRequestActions.RESEND.value,
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
    input_fields = build_test_input_fields()

    # Assign the payload to new nr var
    test_nr = create_test_nr(input_fields, State.HISTORICAL)
    assert test_nr is not None

    # Grab the record using the API
    get_response = get_nr(client, test_nr.get('id'))
    nr = json.loads(get_response.data)
    assert nr is not None

    print('PATCH Response: \n' + json.dumps(nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == HISTORICAL: ' + str(bool(nr.get('stateCd') == 'HISTORICAL')))
    assert nr.get('stateCd') == State.HISTORICAL

    assert_field_is_mapped(test_nr, nr, 'nrNum')

    # Check actions
    actions = nr.get('actions')
    assert_list_contains_exactly(actions, [
        # TODO: Show receipt action ONLY if there is an existing payment!
        # NameRequestActions.RECEIPT.value
    ])


def test_hold_response_actions(client, jwt, app):
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

    # Assign the payload to new nr var
    test_nr = create_test_nr(input_fields, State.HOLD)
    assert test_nr is not None

    # Grab the record using the API
    get_response = get_nr(client, test_nr.get('id'))
    nr = json.loads(get_response.data)
    assert nr is not None

    print('PATCH Response: \n' + json.dumps(nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == HOLD: ' + str(bool(nr.get('stateCd') == 'HOLD')))
    assert nr.get('stateCd') == State.HOLD

    assert_field_is_mapped(test_nr, nr, 'nrNum')

    # Check actions
    actions = nr.get('actions')
    assert len(actions) == 0


def test_inprogress_response_actions(client, jwt, app):
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

    # Assign the payload to new nr var
    test_nr = create_test_nr(input_fields, State.INPROGRESS)
    assert test_nr is not None

    # Grab the record using the API
    get_response = get_nr(client, test_nr.get('id'))
    nr = json.loads(get_response.data)
    assert nr is not None

    print('PATCH Response: \n' + json.dumps(nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == INPROGRESS: ' + str(bool(nr.get('stateCd') == 'INPROGRESS')))
    assert nr.get('stateCd') == State.INPROGRESS

    assert_field_is_mapped(test_nr, nr, 'nrNum')

    # Check actions
    actions = nr.get('actions')
    assert len(actions) == 0


def test_cancelled_response_actions(client, jwt, app):
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

    # Assign the payload to new nr var
    test_nr = create_test_nr(input_fields, State.CANCELLED)
    assert test_nr is not None

    # Grab the record using the API
    get_response = get_nr(client, test_nr.get('id'))
    nr = json.loads(get_response.data)
    assert nr is not None

    print('PATCH Response: \n' + json.dumps(nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')

    # Check state
    print('Assert that stateCd == CANCELLED: ' + str(bool(nr.get('stateCd') == 'CANCELLED')))
    assert nr.get('stateCd') == State.CANCELLED

    assert_field_is_mapped(test_nr, nr, 'nrNum')

    # Check actions
    actions = nr.get('actions')

    assert len(actions) == 0
    # TODO: Show receipt action ONLY if there is an existing payment!
    # assert_list_contains_exactly(actions, [
    #     NameRequestActions.RECEIPT.value
    # ])
