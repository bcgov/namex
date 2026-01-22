"""
Centralized test data factory for creating unique test data across all tests.
This ensures test isolation by generating unique identifiers for all shared resources.
"""
import random
import string
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from namex.models import Applicant, Name, Request, State, User, db


class TestDataFactory:
    """Factory for creating unique test data that prevents conflicts between tests."""

    @staticmethod
    def generate_unique_id(prefix: str = '') -> str:
        """Generate a unique identifier."""
        return f'{prefix}{uuid.uuid4().hex[:8]}'

    @staticmethod
    def generate_unique_username() -> str:
        """Generate a unique username for test users."""
        return f'test_user_{uuid.uuid4().hex[:8]}'

    @staticmethod
    def generate_unique_sub() -> str:
        """Generate a unique sub identifier for test users."""
        return f'idir/test_{uuid.uuid4().hex[:8]}'

    @staticmethod
    def generate_unique_nr_num() -> str:
        """Generate a unique NR number for testing."""
        return f'NR {random.randint(1000000, 9999999)}'

    @staticmethod
    def generate_unique_name(suffix: str = 'LTD') -> str:
        """Generate a unique company name."""
        unique_part = ''.join(random.choices(string.ascii_uppercase, k=6))
        return f'TEST COMPANY {unique_part} {suffix}'

    @classmethod
    def create_test_user(cls, username: Optional[str] = None, commit: bool = True) -> User:
        """Create a unique test user."""
        user = User(
            username=username or cls.generate_unique_username(),
            firstname='Test',
            lastname='User',
            sub=cls.generate_unique_sub(),
            iss='keycloak',
            idp_userid=cls.generate_unique_id(),
            login_source='IDIR'
        )

        if commit:
            db.session.add(user)
            db.session.flush()  # Get the ID without committing

        return user

    @classmethod
    def create_test_nr_data(cls, **overrides) -> Dict[str, Any]:
        """Create unique name request data."""
        unique_suffix = cls.generate_unique_id()

        base_data = {
            'additionalInfo': '',
            'consentFlag': None,
            'consent_dt': None,
            'corpNum': '',
            'entity_type_cd': 'CR',
            'expirationDate': None,
            'furnished': 'N',
            'hasBeenReset': False,
            'natureBusinessInfo': f'Test business {unique_suffix}',
            'priorityCd': 'N',
            'requestTypeCd': 'CR',
            'request_action_cd': 'NEW',
            'submitCount': 1,
            'submitter_userid': cls.generate_unique_username(),
            'userId': cls.generate_unique_username(),
            'xproJurisdiction': '',
            'names': [
                {
                    'name': cls.generate_unique_name(),
                    'choice': 1,
                    'designation': 'LTD',
                    'name_type_cd': 'CO',
                    'consent_words': '',
                    'conflict1': '',
                    'conflict2': '',
                    'conflict3': ''
                }
            ],
            'applicants': {
                'firstName': 'John',
                'lastName': f'Doe{unique_suffix[:6]}',
                'addrLine1': f'{random.randint(100, 999)} Test St',
                'city': 'Victoria',
                'stateProvinceCd': 'BC',
                'countryCd': 'CA',
                'postalCd': 'V8W 3P6',
                'phoneNumber': f'250-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
                'emailAddress': f'test{unique_suffix}@example.com'
            }
        }

        # Apply any overrides
        base_data.update(overrides)
        return base_data


class TestNameRequestBuilder:
    """Builder pattern for creating test name requests with proper isolation."""

    def __init__(self, factory: TestDataFactory = None):
        self.factory = factory or TestDataFactory()
        self.data = self.factory.create_test_nr_data()
        self.user = None

    def with_user(self, user: User = None) -> 'TestNameRequestBuilder':
        """Set or create a user for this name request."""
        self.user = user or self.factory.create_test_user()
        self.data['submitter_userid'] = self.user.username
        self.data['userId'] = self.user.username
        return self

    def with_entity_type(self, entity_type: str) -> 'TestNameRequestBuilder':
        """Set the entity type."""
        self.data['entity_type_cd'] = entity_type
        return self

    def with_request_action(self, action: str) -> 'TestNameRequestBuilder':
        """Set the request action."""
        self.data['request_action_cd'] = action
        return self

    def with_names(self, names: list) -> 'TestNameRequestBuilder':
        """Set custom names."""
        if isinstance(names, list) and names:
            self.data['names'] = []
            for i, name in enumerate(names):
                if isinstance(name, str):
                    name_data = {
                        'name': name,
                        'choice': i + 1,
                        'designation': 'LTD',
                        'name_type_cd': 'CO',
                        'consent_words': '',
                        'conflict1': '',
                        'conflict2': '',
                        'conflict3': ''
                    }
                else:
                    name_data = name
                self.data['names'].append(name_data)
        return self

    def build_data(self) -> Dict[str, Any]:
        """Build the data dictionary."""
        return self.data.copy()

    def create_draft_nr(self) -> Request:
        """Create a draft name request in the database."""
        if not self.user:
            self.with_user()

        # Create the request
        nr = Request()
        nr.nrNum = None  # Draft NRs don't have numbers yet
        nr.stateCd = 'DRAFT'
        nr.requestTypeCd = self.data['requestTypeCd']
        nr.request_action_cd = self.data['request_action_cd']
        nr.entity_type_cd = self.data['entity_type_cd']
        nr.natureBusinessInfo = self.data['natureBusinessInfo']
        nr.priorityCd = self.data['priorityCd']
        nr.submitCount = self.data['submitCount']
        nr.submitter_userid = self.user.username
        nr.userId = self.user.id
        nr.furnished = self.data['furnished']

        db.session.add(nr)
        db.session.flush()  # Get the ID

        # Create applicant
        applicant_data = self.data['applicants']
        applicant = Applicant()
        applicant.nrId = nr.id
        applicant.firstName = applicant_data['firstName']
        applicant.lastName = applicant_data['lastName']
        applicant.addrLine1 = applicant_data['addrLine1']
        applicant.city = applicant_data['city']
        applicant.stateProvinceCd = applicant_data['stateProvinceCd']
        applicant.countryCd = applicant_data['countryCd']
        applicant.postalCd = applicant_data['postalCd']
        applicant.phoneNumber = applicant_data['phoneNumber']
        applicant.emailAddress = applicant_data['emailAddress']

        db.session.add(applicant)
        db.session.flush()

        # Create names
        for name_data in self.data['names']:
            name = Name()
            name.nrId = nr.id
            name.name = name_data['name']
            name.choice = name_data['choice']
            name.designation = name_data.get('designation', '')
            name.name_type_cd = name_data.get('name_type_cd', 'CO')

            db.session.add(name)

        db.session.flush()
        return nr
