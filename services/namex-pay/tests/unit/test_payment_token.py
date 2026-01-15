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
"""Tests for PaymentToken dataclass."""

import pytest

from namex_pay.resources.worker import PaymentToken


def test_init_with_all_fields():
    """Assert that all valid fields are set correctly."""
    data = {
        'id': 'PAY-12345',
        'status_code': 'COMPLETED',
        'filing_identifier': 'FIL-001',
        'corp_type_code': 'BC'
    }
    token = PaymentToken(**data)

    assert token.id == 'PAY-12345'
    assert token.status_code == 'COMPLETED'
    assert token.filing_identifier == 'FIL-001'
    assert token.corp_type_code == 'BC'

def test_init_with_partial_fields():
    """Assert that partial data sets only provided fields."""
    data = {
        'id': 'PAY-999',
        'status_code': 'PENDING'
    }
    token = PaymentToken(**data)

    assert token.id == 'PAY-999'
    assert token.status_code == 'PENDING'
    assert token.filing_identifier is None
    assert token.corp_type_code is None

def test_init_ignores_invalid_fields():
    """Assert that unknown fields are ignored."""
    data = {
        'id': 'PAY-123',
        'status_code': 'COMPLETED',
        'unknown_field': 'should-be-ignored',
        'another_invalid': 12345
    }
    token = PaymentToken(**data)

    assert token.id == 'PAY-123'
    assert token.status_code == 'COMPLETED'
    assert not hasattr(token, 'unknown_field')
    assert not hasattr(token, 'another_invalid')

def test_init_with_empty_kwargs():
    """Assert that empty kwargs results in default None values."""
    token = PaymentToken()

    assert token.id is None
    assert token.status_code is None
    assert token.filing_identifier is None
    assert token.corp_type_code is None

def test_init_with_none_values():
    """Assert that explicit None values are set correctly."""
    data = {
        'id': 'PAY-001',
        'status_code': None,
        'filing_identifier': None,
        'corp_type_code': 'NRO'
    }
    token = PaymentToken(**data)

    assert token.id == 'PAY-001'
    assert token.status_code is None
    assert token.filing_identifier is None
    assert token.corp_type_code == 'NRO'

@pytest.mark.parametrize('status_code', [
    'COMPLETED',
    'APPROVED',
    'PENDING',
    'TRANSACTION_FAILED',
])
def test_init_with_various_status_codes(status_code):
    """Assert that different status codes are accepted."""
    token = PaymentToken(id='PAY-001', status_code=status_code)

    assert token.status_code == status_code

def test_init_with_integer_id():
    """Assert that integer id values are accepted."""
    data = {
        'id': 29590,
        'status_code': 'COMPLETED'
    }
    token = PaymentToken(**data)

    assert token.id == 29590
    assert token.status_code == 'COMPLETED'
