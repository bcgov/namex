# Copyright © 2026 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for PaymentInvoice dataclass."""

import pytest

from namex.services.payment.models import PaymentInvoice


def test_init_with_valid_fields():
    """Assert that valid fields are set correctly."""
    data = {
        'id': 12345,
        'serviceFees': 1.50,
        'paid': 30.0,
        'refund': 0.0,
        'total': 31.50,
        'statusCode': 'COMPLETED',
        'paymentMethod': 'CC',
        'businessIdentifier': 'NR L000001'
    }
    invoice = PaymentInvoice(**data)

    assert invoice.id == data['id']
    assert invoice.serviceFees == data['serviceFees']
    assert invoice.paid == data['paid']
    assert invoice.refund == data['refund']
    assert invoice.total == data['total']
    assert invoice.statusCode == data['statusCode']
    assert invoice.paymentMethod == data['paymentMethod']
    assert invoice.businessIdentifier == data['businessIdentifier']


def test_init_ignores_invalid_fields():
    """Assert that unknown fields are ignored."""
    data = {
        'id': 100,
        'serviceFees': 1.0,
        'paid': 10.0,
        'refund': 0.0,
        'total': 11.0,
        'unknownField': 'should-be-ignored',
        'anotherInvalid': 12345
    }
    invoice = PaymentInvoice(**data)

    assert invoice.id == 100
    assert not hasattr(invoice, 'unknownField')
    assert not hasattr(invoice, 'anotherInvalid')


def test_init_with_default_list_fields():
    """Assert that list fields default to empty lists."""
    data = {
        'id': 200,
        'serviceFees': 1.0,
        'paid': 20.0,
        'refund': 0.0,
        'total': 21.0
    }
    invoice = PaymentInvoice(**data)

    assert invoice.lineItems == []
    assert invoice.receipts == []
    assert invoice.references == []
    assert invoice.details == []
    assert invoice._links == []


def test_init_with_default_dict_field():
    """Assert that paymentAccount defaults to empty dict."""
    data = {
        'id': 300,
        'serviceFees': 1.0,
        'paid': 30.0,
        'refund': 0.0,
        'total': 31.0
    }
    invoice = PaymentInvoice(**data)

    assert invoice.paymentAccount == {}


def test_init_with_payment_account_data():
    """Assert that paymentAccount field accepts dict data."""
    data = {
        'id': 400,
        'serviceFees': 1.5,
        'paid': 40.0,
        'refund': 0.0,
        'total': 41.5,
        'paymentAccount': {'accountId': '2698', 'accountName': 'online banking'}
    }
    invoice = PaymentInvoice(**data)

    assert invoice.paymentAccount == {'accountId': '2698', 'accountName': 'online banking'}


def test_init_with_partial_data():
    """Assert that partial data sets only provided fields."""
    data = {
        'id': 500,
        'serviceFees': 1.0,
        'paid': 50.0,
        'refund': 0.0,
        'total': 51.0,
        'statusCode': 'CREATED'
    }
    invoice = PaymentInvoice(**data)

    assert invoice.id == 500
    assert invoice.statusCode == 'CREATED'
    assert invoice.paymentMethod == ''
    assert invoice.businessIdentifier == ''
    assert invoice.bcolAccount is None


def test_init_with_bcol_account():
    """Assert that bcolAccount field is set correctly."""
    data = {
        'id': 600,
        'serviceFees': 1.0,
        'paid': 60.0,
        'refund': 0.0,
        'total': 61.0,
        'bcolAccount': 123456
    }
    invoice = PaymentInvoice(**data)

    assert invoice.bcolAccount == 123456


def test_init_with_is_payment_action_required():
    """Assert that isPaymentActionRequired field defaults correctly."""
    data = {
        'id': 700,
        'serviceFees': 1.0,
        'paid': 70.0,
        'refund': 0.0,
        'total': 71.0
    }
    invoice = PaymentInvoice(**data)

    assert invoice.isPaymentActionRequired is False


def test_init_with_is_payment_action_required_true():
    """Assert that isPaymentActionRequired can be set to True."""
    data = {
        'id': 800,
        'serviceFees': 1.0,
        'paid': 0.0,
        'refund': 0.0,
        'total': 81.0,
        'isPaymentActionRequired': True
    }
    invoice = PaymentInvoice(**data)

    assert invoice.isPaymentActionRequired is True


def test_init_with_line_items():
    """Assert that lineItems field accepts list data."""
    line_items = [{'description': 'Name Request', 'amount': 30.0}]
    data = {
        'id': 900,
        'serviceFees': 1.0,
        'paid': 31.0,
        'refund': 0.0,
        'total': 31.0,
        'lineItems': line_items
    }
    invoice = PaymentInvoice(**data)

    assert invoice.lineItems == line_items


def test_init_with_all_string_fields():
    """Assert that all string fields are set correctly."""
    data = {
        'id': 1000,
        'serviceFees': 1.0,
        'paid': 100.0,
        'refund': 0.0,
        'total': 101.0,
        'statusCode': 'COMPLETED',
        'createdBy': 'user1',
        'createdName': 'Test User',
        'createdOn': '2026-01-15T10:00:00',
        'updatedBy': 'user2',
        'updatedName': 'Update User',
        'updatedOn': '2026-01-15T11:00:00',
        'paymentMethod': 'ONLINE_BANKING',
        'businessIdentifier': 'NR L000002',
        'corpTypeCode': 'NRO',
        'routingSlip': 'RS-001',
        'datNumber': 'DAT-001',
        'folioNumber': 'FOL-001'
    }
    invoice = PaymentInvoice(**data)

    assert invoice.statusCode == 'COMPLETED'
    assert invoice.createdBy == 'user1'
    assert invoice.createdName == 'Test User'
    assert invoice.createdOn == '2026-01-15T10:00:00'
    assert invoice.updatedBy == 'user2'
    assert invoice.updatedName == 'Update User'
    assert invoice.updatedOn == '2026-01-15T11:00:00'
    assert invoice.paymentMethod == 'ONLINE_BANKING'
    assert invoice.businessIdentifier == 'NR L000002'
    assert invoice.corpTypeCode == 'NRO'
    assert invoice.routingSlip == 'RS-001'
    assert invoice.datNumber == 'DAT-001'
    assert invoice.folioNumber == 'FOL-001'


def test_init_missing_mandatory_fields():
    """Assert that missing mandatory fields raises validation error."""
    data = {
        'statusCode': 'COMPLETED',
        'paymentMethod': 'CC'
    }

    with pytest.raises(Exception):
        PaymentInvoice(**data)

