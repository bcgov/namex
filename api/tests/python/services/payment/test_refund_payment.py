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
"""Tests for PaymentRefundInvoice dataclass."""

from decimal import Decimal
from unittest.mock import patch, MagicMock

import pytest
from namex.services.payment.exceptions import SBCPaymentException
from namex.services.payment.models import PaymentRefundInvoice
from namex.services.payment.payments import refund_payment


@pytest.fixture
def mock_client():
    with patch('namex.services.payment.payments.SBCPaymentClient') as mock_client:
        yield mock_client


@pytest.fixture
def valid_response_data():
    return {
        "refundId": 1234,
        "refundAmount": Decimal("100.00"),
        "message": "Refund processed successfully.",
        "isPartialRefund": False
    }


def test_refund_payment_success(mock_client, valid_response_data):
    mock_instance = MagicMock()
    mock_client.return_value = mock_instance
    mock_instance.refund_payment.return_value = valid_response_data

    payment_identifier = "valid-payment-id"
    model = {"reason": "Customer request"}

    response = refund_payment(payment_identifier, model)

    expected_response = PaymentRefundInvoice(**valid_response_data)
    assert response == expected_response
    mock_instance.refund_payment.assert_called_once_with(payment_identifier, model)


def test_refund_payment_no_response(mock_client):
    mock_instance = MagicMock()
    mock_client.return_value = mock_instance
    mock_instance.refund_payment.return_value = None

    payment_identifier = "valid-payment-id"
    model = {"reason": "Customer request"}

    response = refund_payment(payment_identifier, model)

    assert response is None
    mock_instance.refund_payment.assert_called_once_with(payment_identifier, model)


def test_refund_payment_raises_exception(mock_client):
    mock_instance = MagicMock()
    mock_client.return_value = mock_instance
    mock_instance.refund_payment.side_effect = Exception("SBC Pay API exception.")

    payment_identifier = "invalid-payment-id"
    model = {"reason": "Invalid request"}

    with pytest.raises(SBCPaymentException, match="SBC Pay API exception."):
        refund_payment(payment_identifier, model)
    mock_instance.refund_payment.assert_called_once_with(payment_identifier, model)


def test_refund_payment_with_extra_response_data(mock_client, valid_response_data):
    mock_instance = MagicMock()
    mock_client.return_value = mock_instance

    response_with_extra_fields = {
        **valid_response_data,
        "extraField": "should-be-ignored",
        "anotherUnknownField": 9999,
        "nestedExtra": {"key": "value"}
    }
    mock_instance.refund_payment.return_value = response_with_extra_fields

    payment_identifier = "valid-payment-id"
    model = {"reason": "Customer request"}

    response = refund_payment(payment_identifier, model)

    expected_response = PaymentRefundInvoice(**valid_response_data)
    assert response == expected_response
    assert not hasattr(response, 'extraField')
    assert not hasattr(response, 'anotherUnknownField')
    assert not hasattr(response, 'nestedExtra')
    mock_instance.refund_payment.assert_called_once_with(payment_identifier, model)
