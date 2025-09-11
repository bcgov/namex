"""
Centralized test utilities to prevent database conflicts and ensure test isolation.

This module provides utilities that tests can use to generate unique data,
preventing the database constraint violations and test isolation issues we've been seeing.
"""

import uuid
from typing import Any, Dict, Optional


def make_unique_name(base_name: str = 'TEST COMPANY') -> str:
    """Generate a unique company name to avoid database conflicts."""
    unique_id = str(uuid.uuid4())[:8].upper()
    return f'{base_name} {unique_id}'

def make_unique_nr_number() -> str:
    """Generate a unique NR number for tests."""
    unique_id = str(uuid.uuid4())[:6].upper()
    return f'NR L{unique_id}'

def make_unique_email() -> str:
    """Generate a unique email for tests."""
    unique_id = str(uuid.uuid4())[:8].lower()
    return f'test-{unique_id}@example.com'

def make_unique_user_data() -> Dict[str, Any]:
    """Generate unique user data to avoid conflicts."""
    unique_id = str(uuid.uuid4())[:8]
    return {
        'username': f'test_user_{unique_id.lower()}',
        'firstname': 'Test',
        'lastname': f'User{unique_id.upper()}',
        'sub': f'idir/test_user_{unique_id.lower()}',
        'iss': 'keycloak',
        'idp_userid': f'test_{unique_id}',
        'login_source': 'IDIR',
    }

def make_unique_applicant_data() -> Dict[str, Any]:
    """Generate unique applicant data for name requests."""
    unique_id = str(uuid.uuid4())[:8]
    return {
        'firstName': 'John',
        'lastName': f'Doe{unique_id.upper()}',
        'emailAddress': make_unique_email(),
        'phoneNumber': f'250532{unique_id[:4]}',
        'addrLine1': f'{unique_id[:4]} Test Street',
        'city': 'Victoria',
        'stateProvinceCd': 'BC',
        'postalCd': 'V8R 2P1',
        'countryTypeCd': 'CA',
    }

def make_unique_names_list(count: int = 1, base_name: str = 'TEST COMPANY') -> list:
    """Generate a list of unique names for name requests."""
    names = []
    for i in range(count):
        unique_name = make_unique_name(f'{base_name} {i+1}')
        names.append({
            'choice': i + 1,
            'consent_words': '',
            'conflict1': '',
            'conflict1_num': '',
            'designation': 'LTD.',
            'name': unique_name,
            'name_type_cd': 'CO',
        })
    return names

def make_unique_draft_nr_data() -> Dict[str, Any]:
    """
    Generate a complete set of unique data for creating a draft name request.
    This is the most commonly needed function - use this to replace hardcoded test data.
    """
    return {
        'additionalInfo': 'Test additional info',
        'consentFlag': None,
        'consent_dt': None,
        'corpNum': '',
        'entity_type_cd': 'CR',
        'expirationDate': None,
        'furnished': 'N',
        'hasBeenReset': False,
        'natureBusinessInfo': 'Test business nature',
        'priorityCd': 'N',
        'requestTypeCd': 'CR',
        'request_action_cd': 'NEW',
        'submitCount': 1,
        'submitter_userid': 'name_request_service_account',
        'userId': 'name_request_service_account',
        'xproJurisdiction': '',
        'names': make_unique_names_list(1),
        'applicants': [make_unique_applicant_data()],
    }

def ensure_test_user_exists():
    """Ensure the test user exists in the database, creating it if necessary."""
    from namex.models import User

    # Check if user already exists to avoid duplicate key errors
    existing_user = User.query.filter_by(sub='idir/name_request_service_account').first()
    if existing_user:
        return existing_user

    user = User(
        username='name_request_service_account',
        firstname='Test',
        lastname='User',
        sub='idir/name_request_service_account',
        iss='keycloak',
        idp_userid='123',
        login_source='IDIR',
    )
    user.save_to_db()
    return user

def create_draft_nr(client, input_fields):
    """Create a draft name request using the API."""
    import json

    from tests.python.end_points.common.http import build_request_uri, get_test_headers

    ensure_test_user_exists()

    path = build_request_uri('/api/v1/namerequests/', '')
    headers = get_test_headers()

    if not isinstance(input_fields, str):
        input_fields = json.dumps(input_fields)

    response = client.post(path, data=input_fields, headers=headers)
    return response

# Convenience function for the most common case
def unique_nr_data():
    """Shorthand for make_unique_draft_nr_data()"""
    return make_unique_draft_nr_data()

import uuid
from typing import Any, Dict, Optional


def make_unique_name(base_name: str = 'TEST COMPANY') -> str:
    """Generate a unique company name to avoid database conflicts."""
    unique_id = str(uuid.uuid4())[:8].upper()
    return f'{base_name} {unique_id}'

def make_unique_nr_number() -> str:
    """Generate a unique NR number for tests."""
    unique_id = str(uuid.uuid4())[:6].upper()
    return f'NR L{unique_id}'

def make_unique_email() -> str:
    """Generate a unique email for tests."""
    unique_id = str(uuid.uuid4())[:8].lower()
    return f'test-{unique_id}@example.com'

def make_unique_user_data() -> Dict[str, Any]:
    """Generate unique user data to avoid conflicts."""
    unique_id = str(uuid.uuid4())[:8]
    return {
        'username': f'test_user_{unique_id.lower()}',
        'firstname': 'Test',
        'lastname': f'User{unique_id.upper()}',
        'sub': f'idir/test_user_{unique_id.lower()}',
        'iss': 'keycloak',
        'idp_userid': f'test_{unique_id}',
        'login_source': 'IDIR',
    }

def make_unique_applicant_data() -> Dict[str, Any]:
    """Generate unique applicant data for name requests."""
    unique_id = str(uuid.uuid4())[:8]
    return {
        'firstName': 'John',
        'lastName': f'Doe{unique_id.upper()}',
        'emailAddress': make_unique_email(),
        'phoneNumber': f'250532{unique_id[:4]}',
        'addrLine1': f'{unique_id[:4]} Test Street',
        'city': 'Victoria',
        'stateProvinceCd': 'BC',
        'postalCd': 'V8R 2P1',
        'countryTypeCd': 'CA',
    }

def make_unique_names_list(count: int = 1, base_name: str = 'TEST COMPANY') -> list:
    """Generate a list of unique names for name requests."""
    names = []
    for i in range(count):
        unique_name = make_unique_name(f'{base_name} {i+1}')
        names.append({
            'choice': i + 1,
            'consent_words': '',
            'conflict1': '',
            'conflict1_num': '',
            'designation': 'LTD.',
            'name': unique_name,
            'name_type_cd': 'CO',
        })
    return names

def make_unique_draft_nr_data() -> Dict[str, Any]:
    """
    Generate a complete set of unique data for creating a draft name request.
    This is the most commonly needed function - use this to replace hardcoded test data.
    """
    return {
        'additionalInfo': 'Test additional info',
        'consentFlag': None,
        'consent_dt': None,
        'corpNum': '',
        'entity_type_cd': 'CR',
        'expirationDate': None,
        'furnished': 'N',
        'hasBeenReset': False,
        'natureBusinessInfo': 'Test business nature',
        'priorityCd': 'N',
        'requestTypeCd': 'CR',
        'request_action_cd': 'NEW',
        'submitCount': 1,
        'submitter_userid': 'name_request_service_account',
        'userId': 'name_request_service_account',
        'xproJurisdiction': '',
        'names': make_unique_names_list(1),
        'applicants': [make_unique_applicant_data()],
    }

# Convenience function for the most common case
def unique_nr_data():
    """Shorthand for make_unique_draft_nr_data()"""
    return make_unique_draft_nr_data()
