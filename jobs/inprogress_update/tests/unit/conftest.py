# Copyright © 2025 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Common test configuration and fixtures."""

import datetime
import logging
import os
import random
from contextlib import contextmanager
from unittest.mock import patch

import pytest
from flask_migrate import Migrate, upgrade
from sqlalchemy import event, text

from config import TestConfig
from inprogress_update import create_app
from inprogress_update import db as _db

from . import FROZEN_DATETIME

# ----------------------------
# Context managers / helpers
# ----------------------------


@contextmanager
def not_raises(exception):
    """Assures that an exception is NOT thrown."""
    try:
        yield
    except exception:
        raise pytest.fail(f'DID RAISE {exception}')


# ----------------------------
# Fixtures
# ----------------------------

# Mock Pub/Sub queue publish for all tests
@pytest.fixture(autouse=True)
def mock_pubsub_publish():
    with patch('gcp_queue.gcp_queue.GcpQueue.publish') as mock_publish:
        mock_publish.return_value = None
        yield mock_publish


# Fixture to freeze utcnow to a fixed datetime
@pytest.fixture
def freeze_datetime_utcnow(monkeypatch):
    """Return a static time for datetime.utcnow()."""
    class _Datetime:
        @classmethod
        def utcnow(cls):
            return FROZEN_DATETIME

    monkeypatch.setattr(datetime, 'datetime', _Datetime)


@pytest.fixture(scope='session')
def app():
    """Return a session-wide Flask app configured in TEST mode."""
    logging.info(f'Using test DB: {TestConfig().SQLALCHEMY_DATABASE_URI}')
    _app = create_app(TestConfig())
    return _app


@pytest.fixture
def config(app):
    """Return the app config."""
    return app.config


@pytest.fixture(scope='session')
def client(app):
    """Return a session-wide test client."""
    return app.test_client()


@pytest.fixture(scope='session')
def client_ctx(app):
    """Return a session-wide test client context manager."""
    with app.test_client() as _client:
        yield _client


@pytest.fixture(scope='function')
def client_id():
    """Return a unique client ID for testing purposes."""
    _id = random.SystemRandom().getrandbits(0x58)
    return f'client-{_id}'


@pytest.fixture(scope='function', autouse=True)
def session(app, db):
    """Provide a function-scoped rollbacked session for tests."""
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()

        options = dict(bind=connection, binds={})
        session_ = db._make_scoped_session(options=options)
        db.session = session_

        # Begin nested transaction / savepoint
        session_.begin_nested()

        @event.listens_for(session_(), 'after_transaction_end')
        def restart_savepoint(sess2, trans):
            if trans.nested and not trans._parent.nested:
                sess2.expire_all()
                sess2.begin_nested()

        # Simple query to initialize session
        session_.execute(text('SELECT 1'))

        yield session_

        # Rollback and cleanup
        transaction.rollback()
        connection.close()
        session_.remove()


@pytest.fixture(scope='function')
def db(app):
    """Return a session-wide initialized database with all migrations applied."""
    with app.app_context():
        # Drop and recreate public schema
        with _db.engine.connect() as conn:
            conn.execute(text('DROP SCHEMA public CASCADE;'))
            conn.execute(text('CREATE SCHEMA public;'))
            conn.execute(text('GRANT ALL ON SCHEMA public TO postgres;'))
            conn.execute(text('GRANT ALL ON SCHEMA public TO public;'))
            conn.commit()

        # Run Alembic migrations
        api_dir = os.path.abspath('..').replace('jobs', 'api')
        migrations_dir = os.path.join(api_dir, 'migrations')
        Migrate(app, _db, directory=migrations_dir)
        upgrade()

        return _db
