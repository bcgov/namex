"""
Integration tests for Name Request reponses.
"""

import json

import pytest
import responses

from namex.models import State

from .test_setup_utils.test_helpers import create_test_nr, get_nr


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
        # 'priorityCd': 'N',
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
        'xproJurisdiction': '',
    }


@responses.activate
@pytest.mark.parametrize(
    'priorityCd, queue_time_returned, status_cd',
    [('Y', True, State.DRAFT), ('N', True, State.DRAFT), ('N', False, State.INPROGRESS)],
)
def test_draft_response(priorityCd, queue_time_returned, status_cd, client, jwt, app, mock_auth_affiliation):
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
    input_fields['priorityCd'] = priorityCd

    # Assign the payload to new nr var
    test_nr = create_test_nr(input_fields, status_cd)
    assert test_nr is not None

    # Grab the record using the API
    mock_auth_affiliation()  # Mock any NR number
    get_response = get_nr(client, test_nr.id, jwt)
    nr = json.loads(get_response.data)
    assert nr is not None

    print('Response: \n' + json.dumps(nr, sort_keys=True, indent=4, separators=(',', ': ')) + '\n')
    if queue_time_returned:
        # check that the queue time is returned for draft
        assert 'waiting_time' in nr
    else:
        assert 'waiting_time' not in nr
