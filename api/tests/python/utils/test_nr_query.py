# api/tests/python/utils/test_nr_query.py
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
"""Tests for get_nr_num_from_query function."""

import pytest

from namex.utils.nr_query import get_nr_num_from_query


@pytest.mark.parametrize('query,expected', [
    ('NR 1234567', 'NR 1234567'),
    ('nr 1234567', 'NR 1234567'),
    ('Nr 1234567', 'NR 1234567'),
    ('NR 9999999', 'NR 9999999'),
])
def test_nr_with_space_exact_match(query, expected):
    """Test NR number with space as exact match."""
    result = get_nr_num_from_query(query)

    assert result == expected


@pytest.mark.parametrize('query,expected', [
    ('NR1234567', 'NR 1234567'),
    ('nr1234567', 'NR 1234567'),
    ('Nr1234567', 'NR 1234567'),
])
def test_nr_without_space_exact_match(query, expected):
    """Test NR number without space as exact match."""
    result = get_nr_num_from_query(query)

    assert result == expected


@pytest.mark.parametrize('query,expected', [
    ('NR 1234567 some company', 'NR 1234567'),
    ('NR1234567 some company', 'NR 1234567'),
    ('nr 1234567 ACME Corp', 'NR 1234567'),
])
def test_nr_at_start_of_string(query, expected):
    """Test NR number at the start of the query string."""
    result = get_nr_num_from_query(query)

    assert result == expected


@pytest.mark.parametrize('query,expected', [
    ('some company NR 1234567', 'NR 1234567'),
    ('some company NR1234567', 'NR 1234567'),
    ('ACME Corp nr 9876543', 'NR 9876543'),
])
def test_nr_at_end_of_string(query, expected):
    """Test NR number at the end of the query string."""
    result = get_nr_num_from_query(query)

    assert result == expected


@pytest.mark.parametrize('query,expected', [
    ('1234567', 'NR 1234567'),
    ('9876543', 'NR 9876543'),
    ('1234567 some text', 'NR 1234567'),
    ('some text 1234567', 'NR 1234567'),
])
def test_fallback_number_only(query, expected):
    """Test fallback regex for number-only patterns."""
    result = get_nr_num_from_query(query)

    assert result == expected


@pytest.mark.parametrize('query', [
    'some company name',
    'ACME 123 Corp',
    'NR in the middle 1234567 of text',
    '',
    'NR',
    'Company NR Inc',
])
def test_no_match_returns_none(query):
    """Test that non-matching queries return None."""
    result = get_nr_num_from_query(query)

    assert result is None


@pytest.mark.parametrize('query,expected', [
    ('NR 1', 'NR 1'),
    ('NR 12345678901234', 'NR 12345678901234'),
])
def test_edge_cases(query, expected):
    """Test edge cases for NR number extraction."""
    result = get_nr_num_from_query(query)

    assert result == expected


def test_nr_in_middle_not_matched():
    """Test that NR number in the middle of text is not matched."""
    result = get_nr_num_from_query('prefix NR 1234567 suffix')

    assert result is None


def test_multiple_nr_numbers_returns_first_valid():
    """Test behavior when multiple NR patterns exist."""
    result = get_nr_num_from_query('NR 1111111 NR 2222222')

    assert result == 'NR 1111111'
