import pytest
import json

from .common import API_BASE_URI
# Import token and claims if you need it
# from ..common import token_header, claims
from ..common.http import build_test_query, build_request_uri
from ..common.logging import log_request_path

from tests.python.end_points.name_requests.test_setup_utils.test_helpers import create_draft_nr

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

calculate_fees_request = {
    "corp_type": "TT",
    "filing_type_code": "TT",
    "jurisdiction": "TT",
    "date": "",
    "priority": ""
}

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
def setup_draft_nr(client):
    # Define our data
    input_fields = draft_input_fields
    post_response = create_draft_nr(client, input_fields)

    # Assign the payload to new nr var
    return json.loads(post_response.data)


def test_get_payment(client, jwt, app):
    payment_id = 'abcd153'
    request_uri = API_BASE_URI + payment_id
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)
    payload = json.loads(response.data)

    assert isinstance(payload.get('id'), int) is True
    assert isinstance(payload.get('invoices'), list) is True


def test_create_payment(client, jwt, app):
    draft_nr = setup_draft_nr(client)

    nr_num = draft_nr.get('nrNum')
    request_uri = API_BASE_URI + nr_num

    path = request_uri
    body = json.dumps(create_payment_request)
    log_request_path(path)

    response = client.post(path, json=body)
    payload = json.loads(response.data)

    assert isinstance(payload.get('id'), int) is True
    assert isinstance(payload.get('invoices'), list) is True
    assert payload.get('updated_by') is None
    assert payload.get('updated_on') is None


def test_update_payment(client, jwt, app):
    draft_nr = setup_draft_nr(client)

    nr_num = draft_nr.get('nrNum')
    request_uri = API_BASE_URI + nr_num

    payment_id = 'abcd153'
    request_uri = API_BASE_URI + payment_id

    path = request_uri
    body = json.dumps(create_payment_request)
    log_request_path(path)

    response = client.put(path, json=body)
    payload = json.loads(response.data)

    assert isinstance(payload.get('id'), int) is True
    assert isinstance(payload.get('invoices'), list) is True
    # TODO: Test update fields
    # assert payload.get('updated_by') is not None
    # assert payload.get('updated_on') is not None


def test_get_invoice(client, jwt, app):
    payment_id = 'abcd153'
    invoice_id = 'test'
    request_uri = API_BASE_URI + payment_id + '/invoice'
    test_params = [{'invoice_id': invoice_id}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    # TODO: Test the payload
    payload = json.loads(response.data)
    assert payload is not None


def test_get_invoices(client, jwt, app):
    payment_id = 'abcd153'
    request_uri = API_BASE_URI + payment_id + '/invoices'
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)
    assert payload is not None


def test_get_transaction(client, jwt, app):
    payment_id = 'abcd153'
    request_uri = API_BASE_URI + payment_id + '/transaction'
    test_params = [{
        'transaction_identifier': 'test',
        'receipt_number': 'test',
    }]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200
    
    payload = json.loads(response.data)
    assert payload is not None


def test_get_transactions(client, jwt, app):
    payment_id = 'abcd153'
    request_uri = API_BASE_URI + payment_id + '/transactions'
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)

    assert isinstance(payload.get('items'), list) is True


def test_create_transaction(client, jwt, app):
    payment_id = 'abcd153'
    request_uri = API_BASE_URI + payment_id + '/transaction'

    test_params = [{
        'redirect_uri': 'http://localhost'
    }]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.post(path)
    payload = json.loads(response.data)

    assert isinstance(payload.get('items'), list) is True


def test_update_transaction(client, jwt, app):
    payment_id = 'abcd153'
    receipt_number = 'abcd'
    transaction_id = 'test'
    request_uri = API_BASE_URI + payment_id + '/transactions'

    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    body = json.dumps({
        "receipt_number": receipt_number,
        "transaction_identifier": transaction_id
    })
    log_request_path(path)

    response = client.put(path, json=body)
    payload = json.loads(response.data)

    assert isinstance(payload.get('items'), list) is True


def test_get_receipt(client, jwt, app):
    payment_id = 'abcd153'
    request_uri = API_BASE_URI + payment_id + '/receipt'
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)

    assert isinstance(payload.get('filing_fees'), int) is True
    assert isinstance(payload.get('filing_type'), str) is True
    assert isinstance(payload.get('filing_type_code'), str) is True
    assert isinstance(payload.get('processing_fees'), int) is True
    assert isinstance(payload.get('tax'), list) is True


def test_calculate_fees(client, jwt, app):
    request_uri = API_BASE_URI + 'fees'

    path = request_uri
    body = json.dumps(calculate_fees_request)
    log_request_path(path)

    response = client.post(path, json=body)
    payload = json.loads(response.data)

    assert isinstance(payload.get('filing_fees'), int) is True
    assert isinstance(payload.get('filing_type'), str) is True
    assert isinstance(payload.get('filing_type_code'), str) is True
    assert isinstance(payload.get('processing_fees'), int) is True
    assert isinstance(payload.get('tax'), list) is True
