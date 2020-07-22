import json

from .common import API_BASE_URI
# Import token and claims if you need it
# from ..common import token_header, claims
from ..common.http import build_test_query, build_request_uri
from ..common.logging import log_request_path

create_payment_request = {
    "payment_info": {
        "method_of_payment": "CC"
    },
    "business_info": {
        "business_identifier": "CP1234567",
        "corp_type": "CP",
        "business_name": "ABC Corp",
        "contact_info": {
            "city": "Victoria",
            "postal_code": "V8P2P2",
            "province": "BC",
            "address_line1": "100 Douglas Street",
            "country": "CA"
        }
    },
    "filing_info": {
        "filing_types": [
            {
                "filing_type_code": "OTADD",
                "filing_description": "TEST"
            },
            {
                "filing_type_code": "OTANN"
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
    request_uri = API_BASE_URI

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
