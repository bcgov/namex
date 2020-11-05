import pytest
import json

from .common import API_BASE_URI
# Import token and claims if you need it
# from ..common import token_header, claims
from ..common.http import build_test_query, build_request_uri
from ..common.logging import log_request_path

from tests.python.end_points.name_requests.test_setup_utils.test_helpers import create_draft_nr
from tests.python.end_points.common.http import get_test_headers

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
def is_int_or_float(val):
    return isinstance(val, float) or isinstance(val, int)


@pytest.mark.skip
def setup_draft_nr(client):
    # Define our data
    input_fields = draft_input_fields
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    return json.loads(post_response.data)


@pytest.mark.skip
def verify_fees_payload(payload):
    assert isinstance(payload.get('filingFees'), float) is True
    assert isinstance(payload.get('filingType'), str) is True
    assert isinstance(payload.get('filingTypeCode'), str) is True
    assert is_int_or_float(payload.get('futureEffectiveFees')) is True
    assert is_int_or_float(payload.get('priorityFees')) is True
    assert is_int_or_float(payload.get('processingFees')) is True
    assert is_int_or_float(payload.get('serviceFees')) is True
    assert is_int_or_float(payload.get('futureEffectiveFees')) is True
    assert isinstance(payload.get('tax'), dict) is True
    assert is_int_or_float(payload.get('total')) is True


@pytest.mark.skip
def verify_payment_payload(payload):
    assert isinstance(payload.get('id'), int) is True
    assert isinstance(payload.get('nrId'), int) is True
    assert isinstance(payload.get('payment'), dict) is True
    assert isinstance(payload.get('sbcPayment'), dict) is True
    assert isinstance(payload.get('statusCode'), str) is True
    assert isinstance(payload.get('completionDate'), str) is True
    assert isinstance(payload.get('token'), str) is True


@pytest.mark.skip
def execute_calculate_regular_fees(client):
    """
    1) Get the current the fees.
    :param client:
    :return:
    """
    headers = get_test_headers()

    request_uri = API_BASE_URI + 'fees'

    # Test regular submission
    path = request_uri
    body = json.dumps({
        'corp_type': 'NRO',
        'filing_type_code': 'NM620',
        'jurisdiction': 'BC',
        'date': '',
        'priority': ''
    })
    log_request_path(path)

    response = client.post(path, data=body, headers=headers)

    assert response.status_code == 200

    payload = json.loads(response.data)
    verify_fees_payload(payload)

    assert payload.get('filingTypeCode') == 'NM620'

    return payload


@pytest.mark.skip
def execute_calculate_upgrade_fees(client):
    """
    1) Get the current the fees.
    :param client:
    :return:
    """
    headers = get_test_headers()

    request_uri = API_BASE_URI + 'fees'

    # Test regular submission
    path = request_uri
    body = json.dumps({
        'corp_type': 'NRO',
        'filing_type_code': 'NM606',
        'jurisdiction': 'BC',
        'date': '',
        'priority': ''
    })
    log_request_path(path)

    response = client.post(path, data=body, headers=headers)

    assert response.status_code == 200

    payload = json.loads(response.data)
    verify_fees_payload(payload)

    assert payload.get('filingTypeCode') == 'NM606'

    return payload


@pytest.mark.skip
def execute_create_payment(client, create_payment_request):
    """
    Create a payment. Automatically creates an NR for use.
    :param client:
    :param create_payment_request:
    :return:
    """
    headers = get_test_headers()

    draft_nr = setup_draft_nr(client)

    nr_id = draft_nr.get('id')
    payment_action = 'COMPLETE'
    # POST /api/v1/payments/<int:nr_id>/<string:payment_action>
    request_uri = API_BASE_URI + str(nr_id) + '/' + payment_action

    path = request_uri
    body = json.dumps(create_payment_request)
    log_request_path(path)

    response = client.post(path, data=body, headers=headers)

    assert response.status_code == 201

    payload = json.loads(response.data)
    verify_payment_payload(payload)

    assert payload.get('statusCode') == 'CREATED'

    return payload


@pytest.mark.skip
def execute_get_payment(client, nr_id, payment_id):
    """
    Get a payment.
    :param client:
    :param nr_id
    :param payment_id
    :return:
    """
    # POST /api/v1/payments/<int:nr_id>/payment/<int:payment_id>
    request_uri = API_BASE_URI + str(nr_id) + '/payment/' + str(payment_id)
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)

    assert isinstance(payload.get('id'), int) is True
    # assert isinstance(payload.get('invoices'), list) is True

    return payload


@pytest.mark.skip
def execute_complete_payment(client, payment, action):
    """
    Complete a payment.
    :param client:
    :param payment
    :param action
    :return:
    """
    headers = get_test_headers()

    # PATCH /api/v1/payments/<int:nr_id>/payment/<int:payment_id>/<string:payment_action>
    request_uri = API_BASE_URI + str(payment.get('nrId')) + '/payment/' + str(payment.get('id')) + '/' + action
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.patch(path, data={}, headers=headers)

    assert response.status_code == 200

    payload = json.loads(response.data)

    return payload


@pytest.mark.skip
def execute_get_receipt(client, payment_id):
    """
    Get the receipt.
    :param client:
    :param payment_id:
    :return:
    """
    request_uri = API_BASE_URI + str(payment_id) + '/receipt'
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)

    assert isinstance(payload.get('filingFees'), int) is True
    assert isinstance(payload.get('filingType'), str) is True
    assert isinstance(payload.get('filingTypeCode'), str) is True
    assert isinstance(payload.get('processingFees'), int) is True
    assert isinstance(payload.get('tax'), list) is True


def test_payment_fees(client):
    regular_fees = execute_calculate_regular_fees(client)
    print('Regular fees: \n' + json.dumps(regular_fees))
    upgrade_fees = execute_calculate_upgrade_fees(client)
    print('Upgrade fees: \n' + json.dumps(upgrade_fees))


def test_create_payment(client):
    create_payment_request = {
        'paymentInfo': {
            'methodOfPayment': 'CC'
        },
        'businessInfo': {
            'corpType': 'NRO',
            'businessIdentifier': 'NR L000001',
            'businessName': 'ABC PLUMBING LTD.',
            'contactInfo': {
                'addressLine1': '1796 KINGS RD',
                'city': 'VICTORIA',
                'province': 'BC',
                'country': 'CA',
                'postalCode': 'V8R 2P1'
            }
        },
        'filingInfo': {
            'date': '2020-09-02',
            'filingTypes': [
                {
                    'filingTypeCode': 'NM620',
                    'priority': False,
                    'filingDescription': ''
                }
            ]
        }
    }

    payment = execute_create_payment(client, create_payment_request)
    return payment


def test_payment_creation(client):
    try:
        test_payment_fees(client)
        payment = test_create_payment(client)

        # TODO: There's really no way to complete this payment that I know of... without using a browser...
        completed_nr = execute_complete_payment(client, payment, 'COMPLETE')
        completed_payment = execute_get_payment(client, payment['nrId'], payment['id'])

        assert payment['id'] == completed_payment['id']
        # TODO: There's really no way to complete this payment that I know of... without using a browser...
        # assert completed_payment['statusCode'] == 'COMPLETE'
        assert completed_payment['statusCode'] == 'CREATED'
    except Exception as err:
        print(repr(err))
        raise err


@pytest.mark.skip
def test_payment_receipt(client):
    try:
        test_payment_creation(client)
        # payment_receipt = execute_get_receipt(client, payment['id'])
    except Exception as err:
        print(repr(err))
        raise err
