"""
Centralized test helpers for ensuring test isolation and preventing database conflicts.
"""

import uuid
from typing import Any, Dict, List

import pytest

from namex.models import Request as RequestDAO
from namex.models import State, User
from namex.models.nr_number import NRNumber


class TestDataFactory:
    """Factory class for generating unique test data to prevent database conflicts."""

    @staticmethod
    def generate_unique_suffix() -> str:
        """Generate a unique 8-character suffix for test data."""
        return str(uuid.uuid4())[:8].upper()

    @staticmethod
    def generate_unique_name(base_name: str = 'TEST COMPANY') -> str:
        """Generate a unique company name for tests."""
        suffix = TestDataFactory.generate_unique_suffix()
        return f'{base_name} {suffix}'

    @staticmethod
    def generate_unique_nr_num() -> str:
        """Generate a unique NR number for tests."""
        suffix = TestDataFactory.generate_unique_suffix()
        return f'NR L{suffix[:6]}'

    @staticmethod
    def generate_unique_email() -> str:
        """Generate a unique email for tests."""
        suffix = TestDataFactory.generate_unique_suffix().lower()
        return f'test-{suffix}@example.com'

    @staticmethod
    def generate_unique_user_data() -> Dict[str, Any]:
        """Generate unique user data for tests."""
        suffix = TestDataFactory.generate_unique_suffix()
        return {
            'username': f'test_user_{suffix.lower()}',
            'firstname': 'Test',
            'lastname': f'User{suffix}',
            'sub': f'idir/test_user_{suffix.lower()}',
            'iss': 'keycloak',
            'idp_userid': f'test_{suffix}',
            'login_source': 'IDIR',
        }

    @staticmethod
    def generate_unique_names_data(count: int = 2) -> List[Dict[str, Any]]:
        """Generate unique names data for name requests."""
        suffix = TestDataFactory.generate_unique_suffix()
        names = []

        base_names = ['ABC ENGINEERING', 'ABC PLUMBING', 'XYZ CONSULTING', 'DEF SERVICES']

        for i in range(count):
            base_name = base_names[i % len(base_names)]
            unique_name = f'{base_name} {suffix}'
            names.append({
                'name': unique_name,
                'choice': i + 1,
                'designation': 'LTD.',
                'name_type_cd': 'CO',
                'consent_words': '',
                'conflict1': f'{unique_name} LTD.',
                'conflict1_num': '0515211',
            })

        return names

    @staticmethod
    def generate_unique_applicant_data() -> Dict[str, Any]:
        """Generate unique applicant data for tests."""
        suffix = TestDataFactory.generate_unique_suffix()
        return {
            'firstName': 'John',
            'lastName': f'Doe{suffix}',
            'emailAddress': TestDataFactory.generate_unique_email(),
            'phoneNumber': f'250532{suffix[:4]}',
            'addrLine1': f'{suffix[:4]} Test Street',
            'city': 'Victoria',
            'stateProvinceCd': 'BC',
            'postalCd': 'V8R 2P1',
            'countryTypeCd': 'CA',
        }

    @staticmethod
    def ensure_states_exist():
        """Ensure all required states exist in the database."""
        required_states = [
            ('DRAFT', 'Unexamined name, submitted by a client'),
            ('INPROGRESS', 'An examiner is working on this request'),
            ('CANCELLED', 'The request is cancelled and cannot be changed'),
            ('HOLD', 'A name approval was halted for some reason'),
            ('APPROVED', 'Approved request, this is a final state'),
            ('REJECTED', 'Rejected request, this is a final state'),
            ('CONDITIONAL', 'Approved, but with conditions to be met. This is a final state'),
            ('HISTORICAL', 'Historical state'),
            ('COMPLETED', 'Completed - legacy state'),
            ('EXPIRED', 'Expired - legacy state'),
            ('NRO_UPDATING', 'Internal state used when updating records from NRO'),
            ('COND-RESERVE', 'Temporary reserved state with consent required'),
            ('RESERVED', 'Temporary reserved state between name available and paid'),
            ('CONSUMED', 'Name has been consumed/used'),
            ('REFUND_REQUESTED', 'Refund has been requested'),
        ]

        for code, description in required_states:
            existing_state = State.query.filter_by(cd=code).first()
            if not existing_state:
                state = State(cd=code, description=description)
                state.save_to_db()

    @staticmethod
    def ensure_test_user_exists() -> User:
        """Ensure a test user exists and return it."""
        user_data = {
            'username': 'name_request_service_account',
            'firstname': 'Test',
            'lastname': 'User',
            'sub': 'idir/name_request_service_account',
            'iss': 'keycloak',
            'idp_userid': '123',
            'login_source': 'IDIR',
        }

        existing_user = User.query.filter_by(sub=user_data['sub']).first()
        if existing_user:
            return existing_user

        user = User(**user_data)
        user.save_to_db()
        return user


@pytest.fixture(scope='function')
def unique_test_data():
    """Fixture that provides unique test data for each test function."""
    return TestDataFactory()


@pytest.fixture(scope='session', autouse=True)
def setup_test_environment(app):
    """Auto-run fixture that sets up the test environment."""
    with app.app_context():
        # Ensure required states exist
        TestDataFactory.ensure_states_exist()

        # Ensure test user exists
        TestDataFactory.ensure_test_user_exists()


class TestNameRequestBuilder:
    """Builder class for creating Name Requests with unique data."""

    def __init__(self, factory: TestDataFactory = None):
        self.factory = factory or TestDataFactory()
        self.data = {
            'requestTypeCd': 'CR',
            'request_action_cd': 'NEW',
            'entity_type_cd': 'CR',
            'stateCd': 'DRAFT',
            'priorityCd': 'N',
            'furnished': 'N',
            'hasBeenReset': False,
            'submitCount': 1,
            'submitter_userid': 'name_request_service_account',
            'userId': 'name_request_service_account',
            'additionalInfo': 'Test additional info',
            'natureBusinessInfo': 'Test business',
            'xproJurisdiction': '',
        }
        self.names_data = self.factory.generate_unique_names_data(1)
        self.applicant_data = self.factory.generate_unique_applicant_data()

    def with_state(self, state: str):
        """Set the state of the name request."""
        self.data['stateCd'] = state
        return self

    def with_names(self, names_data: List[Dict[str, Any]]):
        """Set custom names data."""
        self.names_data = names_data
        return self

    def with_unique_names(self, count: int = 1):
        """Generate unique names."""
        self.names_data = self.factory.generate_unique_names_data(count)
        return self

    def with_applicant(self, applicant_data: Dict[str, Any]):
        """Set custom applicant data."""
        self.applicant_data = applicant_data
        return self

    def with_request_type(self, request_type: str, action: str = 'NEW'):
        """Set request type and action."""
        self.data['requestTypeCd'] = request_type
        self.data['request_action_cd'] = action
        return self

    def build_for_api(self) -> Dict[str, Any]:
        """Build data structure for API calls."""
        api_data = self.data.copy()
        api_data['names'] = self.names_data
        api_data['applicants'] = [self.applicant_data]
        return api_data

    def build_for_model(self) -> RequestDAO:
        """Build a RequestDAO model instance."""
        from tests.python.unit.test_setup_utils.build_nr import build_nr

        # Use the centralized build_nr with unique names
        return build_nr(
            nr_state=self.data['stateCd'],
            data=self.data,
            test_names=self.names_data,
            use_unique_names=False  # We're providing our own unique names
        )


@pytest.fixture
def unique_nr_builder(unique_test_data):
    """Fixture that provides a name request builder with unique data."""
    return TestNameRequestBuilder(unique_test_data)
