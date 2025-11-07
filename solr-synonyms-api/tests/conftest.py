import os

import pytest
from flask_migrate import Migrate, upgrade
from sqlalchemy import text

from config import CONFIGURATION
from synonyms import create_app
from synonyms import db as _db


@pytest.fixture(scope='session')
def app():
    """Return a session-wide application configured in TEST mode."""
    _app = create_app(CONFIGURATION["testing"])
    
    # Push application context to ensure extensions are properly initialized
    with _app.app_context():
        yield _app


@pytest.fixture(scope='function')
def db(app):  # pylint: disable=redefined-outer-name, invalid-name
    """Return a session-wide initialised database.

    Drops all existing tables
    """
    with app.app_context():
        with _db.engine.connect() as conn:
            # Drop all tables first with CASCADE to handle dependencies
            conn.execute(text('DROP SCHEMA public CASCADE;'))
            conn.execute(text('CREATE SCHEMA public;'))
            conn.execute(text('GRANT ALL ON SCHEMA public TO postgres;'))
            conn.execute(text('GRANT ALL ON SCHEMA public TO public;'))
            conn.commit()

        # Use Alembic to load all of the DB revisions including supporting lookup data
        api_dir = os.path.abspath('..').replace('services', 'api')
        api_dir_dir = os.path.join(api_dir, 'migrations')
        Migrate(app, _db, directory=api_dir_dir)
        upgrade()

        return _db