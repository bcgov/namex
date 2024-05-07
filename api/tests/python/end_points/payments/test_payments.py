import json
from unittest.mock import patch

import pytest

from namex.constants import (NameRequestPatchActions,
                             NameRequestPaymentActions, PaymentState)
from namex.models import Payment, Request, State, User
from namex.services.payment.client import SBCPaymentClient
from tests.python.end_points.common.http import get_test_headers
from tests.python.end_points.name_requests.test_setup_utils.test_helpers import \
    post_test_nr_json
from tests.python.end_points.util import create_header
from sbc_common_components.utils.enums import QueueMessageTypes

from ..common.http import build_request_uri, build_test_query
from ..common.logging import log_request_path
from .common import API_BASE_NAMEREQUEST_URI, API_BASE_URI

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

draft_nr_json = {
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
			'partyId': '',
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
	'entity_type_cd': 'CR',
	'request_action_cd': 'NEW',
	'stateCd': 'DRAFT',
	'english': True,
	'nameFlag': False,
	'submit_count': 0,
	'corpNum': '',
	'homeJurisNum': ''
}

@pytest.mark.skip
def setup_draft_nr(client):
    post_response = post_test_nr_json(client, draft_nr_json)

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
    # assert isinstance(payload.get('completionDate'), str) is True
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
def execute_payment(client, jwt, create_payment_request, payment_action):
    """
    Create a payment. Automatically creates an NR for use.
    :param client:
    :param create_payment_request:
    :return:
    """
    headers = create_header(jwt, [User.STAFF])
    headers['content-type'] = 'application/json'

    draft_nr = setup_draft_nr(client)

    nr_id = draft_nr.get('id')
    # POST /api/v1/payments/<int:nr_id>/<string:payment_action>
    request_uri = API_BASE_URI + str(nr_id) + '/' + payment_action

    path = request_uri
    create_payment_request['headers'] = headers
    body = json.dumps(create_payment_request)
    log_request_path(path)

    response = client.post(path, data=body, headers=headers)

    assert response.status_code == 201

    payload = json.loads(response.data)
    verify_payment_payload(payload)

    assert payload.get('statusCode') == 'CREATED'
    assert payload.get('action') == payment_action

    return payload


@pytest.mark.skip
def execute_get_payment(client, nr_id, payment_id):
    """
    Get a payment associated with a specific NR.
    :param client:
    :param nr_id
    :param payment_id
    :return:
    """
    # GET /api/v1/payments/<int:nr_id>/payment/<int:payment_id>
    request_uri = API_BASE_URI + str(nr_id) + '/payment/' + str(payment_id)
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)

    assert isinstance(payload[0].get('id'), int) is True
    # TODO: Check invoices / receipts...
    # assert isinstance(payload.get('invoices'), list) is True

    return payload


@pytest.mark.skip
def execute_get_payments(client, nr_id):
    """
    Get all payments associated with a specific NR.
    :param client:
    :param nr_id
    :return:
    """
    # GET /api/v1/payments/<int:nr_id>
    request_uri = API_BASE_URI + str(nr_id)
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.get(path)

    assert response.status_code == 200

    payload = json.loads(response.data)

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
def execute_refund_payment(client, payment):
    """
    Refund a payment.
    :param client:
    :param payment
    :return:
    """
    headers = get_test_headers()

    request_uri = API_BASE_URI + \
        str(payment.get('nrId')) + '/payment/' + str(payment.get('id')) + '/' + \
        NameRequestPaymentActions.REQUEST_REFUND.value
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.patch(path, data={}, headers=headers)

    assert response.status_code == 200

    payload = json.loads(response.data)

    return payload


@pytest.mark.skip
def execute_cancel_and_refund_all_payments(client, nr_id):
    """
    Cancel NR and request refund for all NR payments.
    :param client
    :param nr_id
    :return:
    """
    headers = get_test_headers()

    request_uri = API_BASE_NAMEREQUEST_URI + str(nr_id) + '/' + NameRequestPatchActions.REQUEST_REFUND.value
    test_params = [{}]

    query = build_test_query(test_params)
    path = build_request_uri(request_uri, query)
    log_request_path(path)

    response = client.patch(path, json={}, headers=headers)

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

mock_receipt_response = {
    "bcOnlineAccountNumber": "None",
    "filingIdentifier": "None",
    "invoice": {
        "_links": {
            "collection": "/api/v1/payment-requests/6627",
            "self": "/api/v1/payment-requests?invoice_id=6627"
        },
        "businessIdentifier": "NR 3768105",
        "corpTypeCode": "NRO",
        "createdBy": "SERVICE-ACCOUNT-NAME-REQUEST-SERVICE-ACCOUNT",
        "createdName": "None None",
        "createdOn": "2021-01-14T23:52:05.531317+00:00",
        "id": 6627,
        "lineItems":[
            {
            "description": "Name Request fee",
            "filingFees": 30.0,
            "futureEffectiveFees": 0.0,
            "gst": 0.0,
            "id": 8249,
            "priorityFees": 0.0,
            "pst": 0.0,
            "quantity": 1,
            "serviceFees": 1.5,
            "statusCode": "ACTIVE",
            "total": 30.0,
            "waivedBy": "None",
            "waivedFees": 0.0
            }
        ],
        "paid": 31.5,
        "paymentMethod": "DIRECT_PAY",
        "receipts": [
            {
            "id": 3360,
            "receiptAmount": 31.5,
            "receiptDate": "2021-01-14T00:00:00+00:00",
            "receiptNumber": "1234"
            }
        ],
        "references": [
            {
            "id": 6578,
            "invoiceNumber": "1123",
            "statusCode": "COMPLETED"
            }
        ],
        "refund": 0.0,
        "serviceFees": 1.5,
        "statusCode": "COMPLETED",
        "total": 31.5,
        "updatedName": "None None",
        "updatedOn": "2021-01-14T23:52:56.810045+00:00"
    },
    "invoiceNumber": "1234",
    "paymentMethod": "Credit Card",
    "receiptNumber": "123"
}


@pytest.mark.parametrize('test_name, action, complete_payment, do_refund, cancel_payment, request_receipt', [
    ('New NR payment', 'CREATE', False, False, False, False),
    ('Resubmit NR payment', 'RESUBMIT', False, False, False, False),
    ('Complete payment', 'CREATE', True, False, False, False),
    ('Refund payment', 'CREATE', True, True, False, False),
    ('Cancel Payment', 'CREATE', False, False, True, False),
    ('Request receipt', 'CREATE', False, False, False, True)
])
def test_create_payment(client, jwt, test_name, action, complete_payment, do_refund, cancel_payment, request_receipt, mocker):
    from namex.services import queue
    topics = []
    msg=None

    def mock_publish(topic: str, payload: bytes):
        nonlocal topics
        nonlocal msg
        topics.append(topic)
        msg = payload
        return {}

    mocker.patch.object(queue, "publish", mock_publish)

    payment = execute_payment(client, jwt, create_payment_request, action)
    assert payment['action'] == action
    if complete_payment:
        test_payment_fees(client)
        payment_id = payment['id']
        nr_id = payment['nrId']

        # Fire off the request to complete the payment, just to test that the endpoint is there and runs,
        # we will not actually be able to complete the payment without a browser (at this time anyway)
        execute_complete_payment(client, payment, NameRequestPaymentActions.COMPLETE.value)
        # Manually update the Payment, setting the stateCd to COMPLETE
        payment_model = Payment.query.get(payment_id)
        payment_model.payment_status_code = PaymentState.COMPLETED.value
        payment_model.save_to_db()
        # Get the 'completed' payment
        completed_payment = execute_get_payment(client, nr_id, payment_id)

        assert payment_id == completed_payment[0]['id']
        assert completed_payment[0]['statusCode'] == PaymentState.COMPLETED.value

    if complete_payment:
        assert len(topics) == 1

        email_pub = json.loads(msg.decode("utf-8").replace("'",'"'))

        # Verify message that would be sent to the emailer pubsub
        assert email_pub['type'] == QueueMessageTypes.NAMES_EVENT.value
        assert email_pub['source'] == '/requests/NR L000001'
        assert email_pub['subject'] == 'namerequest'
        assert email_pub['data']['request']['nrNum'] == 'NR L000001'
        assert email_pub['data']['request']['newState'] == 'DRAFT'
        assert email_pub['data']['request']['previousState'] == 'PENDING_PAYMENT'


    if do_refund:
        with patch.object(SBCPaymentClient, 'refund_payment', return_value={}):
            execute_refund_payment(client, payment)
            # Get any payments and make sure they
            payments = execute_get_payments(client, completed_payment[0]['nrId'])
            assert payments and isinstance(payments, list) and len(payments) == 1
            assert payments[0]['statusCode'] == State.REFUND_REQUESTED

    if cancel_payment:
        with patch.object(SBCPaymentClient, 'cancel_payment', return_value={}):
            headers = get_test_headers()
            request_uri = API_BASE_URI + str(payment.get('nrId')) + '/payment/' + str(payment.get('id')) + '/' + \
                          NameRequestPaymentActions.CANCEL.value
            test_params = [{}]
            query = build_test_query(test_params)
            path = build_request_uri(request_uri, query)
            log_request_path(path)

            response = client.patch(path, data={}, headers=headers)
            assert response.status_code == 200

            # Get namex payment and ensure that it is in a cancelled state
            payments = execute_get_payments(client, payment['nrId'])
            assert payments and isinstance(payments, list) and len(payments) == 1
            assert payments[0]['statusCode'] == State.CANCELLED

    if request_receipt:
        with patch.object(SBCPaymentClient, 'get_receipt', return_value=mock_receipt_response):
            request_uri = API_BASE_URI + str(payment.get('id')) + '/receipt'
            query = build_test_query([{}])
            path = build_request_uri(request_uri, query)
            log_request_path(path)
            response = client.get(path)
            assert response.status_code == 200

