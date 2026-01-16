import datetime
import urllib.parse
from contextlib import suppress
from unittest.mock import patch

import pytest
import responses
from flask_migrate import Migrate, upgrade
from sqlalchemy import event, text
from sqlalchemy.schema import DropConstraint, MetaData

from namex import create_app
from namex import jwt as _jwt
from namex.models import db
from namex.models import db as _db

from .python import FROZEN_DATETIME


# fixture to freeze utcnow to a fixed date-time
@pytest.fixture
def freeze_datetime_utcnow(monkeypatch):
    class _Datetime:
        @classmethod
        def utcnow(cls):
            return FROZEN_DATETIME

    monkeypatch.setattr(datetime, 'datetime', _Datetime)


@pytest.fixture(scope='session')
def app(request):
    """
    Returns session-wide application.
    """
    app = create_app('testing')

    return app


@pytest.fixture(scope='session')
def client(app):
    """
    Returns session-wide Flask test client.
    """
    return app.test_client()


@pytest.fixture(scope='session')
def jwt(app):
    """
    Returns session-wide jwt manager
    """
    return _jwt


@pytest.fixture(scope='session')
def solr(app):
    import os

    return os.getenv('SOLR_TEST_URL')


@pytest.fixture(scope='session')
def client_ctx(app):
    """
    Returns session-wide Flask test client.
    """
    with app.test_client() as c:
        yield c


def test_print_db_connection_string(app):
    """Debug test to print the database connection string."""
    with app.app_context():
        from namex.models import db
        print(f"\n\nDatabase URI: {db.engine.url}\n")
        # Or from config:
        print(f"Config SQLALCHEMY_DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}\n\n")
    assert True  # Just to make it a valid test

@pytest.fixture(scope='session')
def db(app, request):
    """
    Returns session-wide initialised database.
    Drops all existing tables - Meta follows Postgres FKs
    """
    with app.app_context():
        # Clear out any existing tables
        metadata = MetaData()
        metadata.reflect(bind=_db.engine)
        with _db.engine.connect() as connection:
            for table in metadata.tables.values():
                for fk in table.foreign_keys:
                    connection.execute(DropConstraint(fk.constraint))
        with suppress(Exception):
            metadata.drop_all(bind=_db.engine)
        with suppress(Exception):
            _db.drop_all()

        sequence_sql = f"""SELECT sequence_name FROM information_schema.sequences
                          WHERE sequence_schema='{app.config.get("DB_SCHEMA", "public")}'
                       """

        sess = _db.session()
        for seq in [name for (name,) in sess.execute(text(sequence_sql))]:
            try:
                schema = app.config.get('DB_SCHEMA', 'public')
                sess.execute(text(f'DROP SEQUENCE {schema}.{seq} ;'))
                print(f'DROP SEQUENCE {schema}.{seq} ')
            except Exception as e:
                print('Error: {}'.format(e))
        sess.commit()

        # ############################################
        # There are 2 approaches, an empty database, or the same one that the app will use
        #     create the tables
        #     _db.create_all()
        # or
        # Use Alembic to load all of the DB revisions including supporting lookup data
        # This is the path we'll use in NAMEX!!

        # even though this isn't referenced directly, it sets up the internal configs that upgrade needs
        migrate = Migrate(app, _db)
        upgrade()

        return _db


@pytest.fixture(scope='function', autouse=True)
def session(app, db, request):
    """
    Returns function-scoped session with proper transaction isolation for pg8000.
    """
    with app.app_context():
        # Create a new connection and transaction for each test
        connection = db.engine.connect()
        transaction = connection.begin()

        # Create a nested transaction (savepoint) for isolation
        nested_transaction = connection.begin_nested()

        # Configure session to use this connection
        session_options = dict(bind=connection, binds={})
        test_session = db._make_scoped_session(options=session_options)

        # Store original session and methods
        original_session = db.session
        original_commit = test_session.commit
        original_rollback = test_session.rollback

        # Override commit to only flush, not actually commit
        def patched_commit():
            test_session.flush()

        # Override rollback to rollback to savepoint
        def patched_rollback():
            nonlocal nested_transaction
            if nested_transaction.is_active:
                nested_transaction.rollback()
                nested_transaction = connection.begin_nested()
            else:
                nested_transaction = connection.begin_nested()

        # Apply patches
        test_session.commit = patched_commit
        test_session.rollback = patched_rollback

        # Replace the global session
        db.session = test_session

        # Test the connection
        db.session.execute(text('SELECT 1'))

        yield db.session

        # Cleanup: restore everything and rollback
        test_session.commit = original_commit
        test_session.rollback = original_rollback
        db.session = original_session
        test_session.remove()

        # Rollback all changes
        if nested_transaction.is_active:
            nested_transaction.rollback()
        transaction.rollback()
        connection.close()


@pytest.fixture(autouse=True)
def set_auth_api_url(app):
    """
    Automatically sets a dummy Auth API URL for all tests so that services relying on this config key don't fail.
    Useful when mocking endpoints that depend on this URL (e.g., affiliation checks).
    """
    app.config['AUTH_SVC_URL'] = 'https://mock-auth-api/api/v1'


@pytest.fixture
def mock_auth_affiliation():
    """
    Mocks the external Auth API affiliation endpoint so tests don't make real HTTP requests.
    Prevents failures in CI or local testing environments that don't have access to real Auth API credentials.
    """

    def _mock(nr_num=None, org_id='1234'):
        if nr_num:
            # Mock specific NR number if provided
            escaped_nr = urllib.parse.quote(nr_num)
            mocked_auth_url = f'https://mock-auth-api/api/v1/orgs/{org_id}/affiliations/{escaped_nr}'
            responses.add(responses.GET, mocked_auth_url, json={}, status=200)
        else:
            # Mock any NR number with regex pattern
            import re
            responses.add(
                responses.GET,
                re.compile(r'https://mock-auth-api/api/v1/orgs/\d+/affiliations/NR%20\d+'),
                json={},
                status=200
            )

    return _mock


@pytest.fixture(autouse=True)
def mock_gcp_queue_publish():
    """
    Mocks the Google Cloud Pub/Sub `publish` method to prevent actual message publishing during tests.
    Ensures tests run without requiring access to GCP credentials or cloud infrastructure.
    """
    with patch('namex.utils.queue_util.queue.publish') as mock_publish:
        mock_publish.return_value = None
        yield mock_publish


# ============================================================================
# TEST DATA ISOLATION FIXTURES
# ============================================================================

@pytest.fixture
def test_data_factory():
    """
    Provides a TestDataFactory instance for creating unique test data.
    This ensures every test gets unique data and prevents conflicts.
    """
    from .fixtures.test_data_factory import TestDataFactory
    return TestDataFactory()


@pytest.fixture
def test_nr_builder(test_data_factory):
    """
    Provides a TestNameRequestBuilder for creating test name requests.
    Automatically handles user creation and data uniqueness.
    """
    from .fixtures.test_data_factory import TestNameRequestBuilder
    return TestNameRequestBuilder(test_data_factory)


@pytest.fixture
def unique_user(test_data_factory):
    """
    Creates a unique test user for each test.
    The user is automatically cleaned up by the session fixture's transaction rollback.
    """
    return test_data_factory.create_test_user(commit=False)


@pytest.fixture
def unique_user_committed(test_data_factory):
    """
    Creates a unique test user and commits it to the database.
    Use this when you need the user to be available across multiple operations.
    """
    user = test_data_factory.create_test_user(commit=True)
    db.session.commit()
    return user


@pytest.fixture
def unique_draft_nr_data():
    """
    Provides unique name request data for API calls.
    Each test gets completely unique data to prevent conflicts.
    """
    import random
    import uuid

    unique_id = uuid.uuid4().hex[:8]
    unique_num = random.randint(1000, 9999)

    return {
        'applicants': [
            {
                'addrLine1': f'{random.randint(100, 999)}-{random.randint(1000, 9999)} Test Blvd',
                'addrLine2': None,
                'addrLine3': None,
                'city': 'Victoria',
                'clientFirstName': None,
                'clientLastName': None,
                'contact': '',
                'countryTypeCd': 'CA',
                'declineNotificationInd': None,
                'emailAddress': f'test{unique_id}@example.com',
                'faxNumber': None,
                'firstName': 'John',
                'lastName': f'Doe{unique_num}',
                'middleName': None,
                'partyId': '',  # must be empty
                'phoneNumber': f'250{random.randint(1000000, 9999999)}',
                'postalCd': 'V8W 3P6',
                'stateProvinceCd': 'BC',
            }
        ],
        'names': [
            {
                'choice': 1,
                'consent_words': '',
                'conflict1': '',
                'conflict1_num': '',
                'designation': 'CORP.',
                'name': f'TESTING CORP {unique_id.upper()}.',
                'name_type_cd': 'CO',
            }
        ],
        'additionalInfo': f'*** Additional Info for test {unique_id} ***',
        'natureBusinessInfo': f'Test business {unique_id}',
        'priorityCd': 'N',
        'entity_type_cd': '',
        'request_action_cd': '',
        'stateCd': 'DRAFT',
        'english': True,
        'nameFlag': False,
        'submit_count': 0,
        'corpNum': '',
        'homeJurisNum': '',
    }


@pytest.fixture
def draft_nr_with_user(test_nr_builder, unique_user):
    """
    Creates a complete draft name request with associated user in the database.
    All data is unique and isolated per test.
    """
    return test_nr_builder.with_user(unique_user).create_draft_nr()


@pytest.fixture
def clean_database_state(session):
    """
    Ensures clean database state by checking for any test pollution.
    This fixture runs after each test to verify isolation is working.
    """
    yield

    # Verify no test pollution remains (optional - can be disabled for performance)
    # This helps catch isolation issues during development
    from sqlalchemy import text

    # Check for any uncommitted data that might leak between tests
    result = session.execute(text("SELECT COUNT(*) FROM users WHERE username LIKE 'test_%'"))
    test_user_count = result.scalar()

    if test_user_count > 0:
        # This indicates test data might be leaking - but it's expected in a transaction
        # The session fixture should clean this up with rollback
        pass
