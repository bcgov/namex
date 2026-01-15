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
"""Tests for ReceiptResponse dataclass."""

import pytest

from namex.services.payment.models import PaymentInvoice, ReceiptResponse


def test_init_with_valid_fields():
    """Assert that valid fields are set correctly."""
    data = {
        'bcOnlineAccountNumber': 'BC12345',
        'filingIdentifier': 'FIL-001',
        'invoiceNumber': 'INV-100',
        'paymentMethod': 'CC',
        'receiptNumber': 'REC-999',
        'routingSlipNumber': 'RS-001'
    }
    response = ReceiptResponse.from_dict(data)

    assert response.bcOnlineAccountNumber == 'BC12345'
    assert response.filingIdentifier == 'FIL-001'
    assert response.invoiceNumber == 'INV-100'
    assert response.paymentMethod == 'CC'
    assert response.receiptNumber == 'REC-999'
    assert response.routingSlipNumber == 'RS-001'

def test_init_ignores_invalid_fields():
    """Assert that unknown fields are ignored."""
    data = {
        'receiptNumber': 'REC-123',
        'unknownField': 'should-be-ignored',
        'anotherInvalid': 12345
    }
    response = ReceiptResponse.from_dict(data)

    assert response.receiptNumber == 'REC-123'
    assert not hasattr(response, 'unknownField')
    assert not hasattr(response, 'anotherInvalid')

def test_init_with_empty_kwargs():
    """Assert that empty kwargs results in default values."""
    response = ReceiptResponse()

    assert response.bcOnlineAccountNumber is None
    assert response.filingIdentifier is None
    assert response.invoiceNumber == ''
    assert response.paymentMethod == ''
    assert response.receiptNumber == ''
    assert response.routingSlipNumber == ''

def test_init_with_partial_data():
    """Assert that partial data sets only provided fields."""
    data = {
        'receiptNumber': 'REC-PARTIAL',
        'paymentMethod': 'DIRECT_PAY'
    }
    response = ReceiptResponse.from_dict(data)

    assert response.receiptNumber == 'REC-PARTIAL'
    assert response.paymentMethod == 'DIRECT_PAY'
    assert response.bcOnlineAccountNumber is None
    assert response.invoiceNumber == ''

def test_init_with_invoice_dict():
    """Assert that invoice field accepts dict data."""
    invoice_data = {'id': 100, 'total': 30.0, 'paid': 30.0}
    data = {
        'receiptNumber': 'REC-INV',
        'invoice': invoice_data
    }
    response = ReceiptResponse.from_dict(data)

    assert response.receiptNumber == 'REC-INV'
    assert response.invoice == invoice_data

def test_init_overwrites_none_defaults():
    """Assert that None defaults can be overwritten."""
    data = {
        'bcOnlineAccountNumber': 'BCOL-NEW',
        'filingIdentifier': 'FIL-NEW'
    }
    response = ReceiptResponse.from_dict(data)

    assert response.bcOnlineAccountNumber == 'BCOL-NEW'
    assert response.filingIdentifier == 'FIL-NEW'
