# Copyright © 2019 Province of British Columbia
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
"""Common setup and fixtures for the pytest suite used by this service."""
import contextlib
import datetime
import os
import random
import time
from contextlib import contextmanager, suppress
from typing import Final
from sqlalchemy.sql.ddl import DropConstraint

import psycopg2
import pytest
import sqlalchemy
from flask import Flask
from flask_migrate import Migrate, upgrade
from sqlalchemy import event, text
from sqlalchemy.schema import MetaData

from namex_pay import create_app
from namex_pay import db as _db
from namex_pay.config import TestConfig

from . import FROZEN_DATETIME

DB_TEST_NAME: Final = os.getenv("DATABASE_TEST_NAME")

@pytest.fixture
def create_mock_coro(mocker, monkeypatch):
    """Return a mocked coroutine, and optionally patch-it in."""
    def _create_mock_patch_coro(to_patch=None):
        mock = mocker.Mock()

        async def _coro(*args, **kwargs):
            return mock(*args, **kwargs)

        if to_patch:  # <-- may not need/want to patch anything
            monkeypatch.setattr(to_patch, _coro)
        return mock, _coro

    return _create_mock_patch_coro

@contextmanager
def not_raises(exception):
    """Corallary to the pytest raises builtin.

    Assures that an exception is NOT thrown.
    """
    try:
        yield
    except exception:
        raise pytest.fail(f'DID RAISE {exception}')


# fixture to freeze utcnow to a fixed date-time
@pytest.fixture
def freeze_datetime_utcnow(monkeypatch):
    """Fixture to return a static time for utcnow()."""
    class _Datetime:
        @classmethod
        def utcnow(cls):
            return FROZEN_DATETIME

    monkeypatch.setattr(datetime, 'datetime', _Datetime)


# @pytest.fixture(scope='session')
# def app():
#     """Return a session-wide application configured in TEST mode."""
#     _app = Flask('testing')    
#     print(config)
#     _app.config.from_object(get_named_config('testing'))
#     _db.init_app(_app)
#     queue.init_app(_app, asyncio.new_event_loop())

#     return _app

@pytest.fixture(scope="session")
def app():
    """Return a session-wide application configured in TEST mode."""
    _app = create_app(TestConfig)

    return _app


@pytest.fixture
def config(app):
    """Return the application config."""
    return app.config


@pytest.fixture(scope='session')
def client(app):  # pylint: disable=redefined-outer-name
    """Return a session-wide Flask test client."""
    return app.test_client()


@pytest.fixture(scope='session')
def client_ctx(app):  # pylint: disable=redefined-outer-name
    """Return session-wide Flask test client."""
    with app.test_client() as _client:
        yield _client


@pytest.fixture(scope='function')
def client_id():
    """Return a unique client_id that can be used in tests."""
    _id = random.SystemRandom().getrandbits(0x58)
    # _id = (base64.urlsafe_b64encode(uuid.uuid4().bytes)).replace('=', '')

    return f'client-{_id}'



@pytest.fixture(scope='session')
def db(app):  # pylint: disable=redefined-outer-name, invalid-name
    """Return a session-wide initialised database.

    Drops all existing tables - Meta follows Postgres FKs
    """
    with app.app_context():
        # Clear out any existing tables
        metadata = MetaData(_db.engine)
        metadata.reflect()
        for table in metadata.tables.values():
            for fk in table.foreign_keys:  # pylint: disable=invalid-name
                _db.engine.execute(DropConstraint(fk.constraint))
        metadata.drop_all()
        _db.drop_all()

        sequence_sql = """SELECT sequence_name FROM information_schema.sequences
                          WHERE sequence_schema='public'
                       """

        sess = _db.session()
        for seq in [name for (name,) in sess.execute(text(sequence_sql))]:
            try:
                sess.execute(text('DROP SEQUENCE public.%s ;' % seq))
                print('DROP SEQUENCE public.%s ' % seq)
            except Exception as err:  # pylint: disable=broad-except
                print(f'Error: {err}')
        sess.commit()

        # ##############################################
        # There are 2 approaches, an empty database, or the same one that the app will use
        #     create the tables
        #     _db.create_all()
        # or
        # Use Alembic to load all of the DB revisions including supporting lookup data
        # This is the path we'll use in legal_api!!

        # even though this isn't referenced directly, it sets up the internal configs that upgrade needs
        api_dir = os.path.abspath('..').replace('services', 'api')
        api_dir_dir = os.path.join(api_dir, 'migrations')
        Migrate(app, _db, directory=api_dir_dir)
        upgrade()

        return _db


# def create_test_db(
#     user: str = None,
#     password: str = None,
#     database: str = None,
#     host: str = "localhost",
#     port: int = 1521,
#     database_uri: str = None,
# ) -> bool:
#     """Create the database in our .devcontainer launched postgres DB.

#     Parameters
#     ------------
#         user: str
#             A datbase user that has create database privledges
#         password: str
#             The users password
#         database: str
#             The name of the database to create
#         host: str, Optional
#             The network name of the server
#         port: int, Optional
#             The numeric port number
#     Return
#     -----------
#         : bool
#             If the create database succeeded.
#     """
#     if database_uri:
#         DATABASE_URI = database_uri
#     else:
#         DATABASE_URI = f"postgresql://{user}:{password}@{host}:{port}/{user}"

#     DATABASE_URI = DATABASE_URI[: DATABASE_URI.rfind("/")] + "/postgres"

#     try:
#         with sqlalchemy.create_engine(DATABASE_URI, isolation_level="AUTOCOMMIT").connect() as conn:
#             conn.execute(text(f"CREATE DATABASE {database}"))

#         return True
#     except sqlalchemy.exc.ProgrammingError as err:
#         print(err)  # used in the test suite, so on failure print something
#         return False


# def drop_test_db(
#     user: str = None,
#     password: str = None,
#     database: str = None,
#     host: str = "localhost",
#     port: int = 1521,
#     database_uri: str = None,
# ) -> bool:
#     """Delete the database in our .devcontainer launched postgres DB."""
#     if database_uri:
#         DATABASE_URI = database_uri
#     else:
#         DATABASE_URI = f"postgresql://{user}:{password}@{host}:{port}/{user}"

#     DATABASE_URI = DATABASE_URI[: DATABASE_URI.rfind("/")] + "/postgres"

#     close_all = f"""
#         SELECT pg_terminate_backend(pg_stat_activity.pid)
#         FROM pg_stat_activity
#         WHERE pg_stat_activity.datname = '{database}'
#         AND pid <> pg_backend_pid();
#     """
#     with contextlib.suppress(sqlalchemy.exc.ProgrammingError, psycopg2.OperationalError, Exception):
#         with sqlalchemy.create_engine(DATABASE_URI, isolation_level="AUTOCOMMIT").connect() as conn:
#             conn.execute(text(close_all))
#             conn.execute(text(f"DROP DATABASE {database}"))


# @contextmanager
# def not_raises(exception):
#     """Corallary to the pytest raises builtin.

#     Assures that an exception is NOT thrown.
#     """
#     try:
#         yield
#     except exception:
#         raise pytest.fail(f"DID RAISE {exception}")


# # fixture to freeze utcnow to a fixed date-time
# @pytest.fixture
# def freeze_datetime_utcnow(monkeypatch):
#     """Fixture to return a static time for utcnow()."""

#     class _Datetime:
#         @classmethod
#         def utcnow(cls):
#             return FROZEN_DATETIME

#     monkeypatch.setattr(datetime, "datetime", _Datetime)


# @pytest.fixture(scope="session")
# def app():
#     """Return a session-wide application configured in TEST mode."""
#     _app = create_app(TestConfig)

#     return _app


# @pytest.fixture
# def config(app):
#     """Return the application config."""
#     return app.config


# @pytest.fixture(scope="session")
# def client(app):  # pylint: disable=redefined-outer-name
#     """Return a session-wide Flask test client."""
#     return app.test_client()


# @pytest.fixture(scope="session")
# def db(app):  # pylint: disable=redefined-outer-name, invalid-name
#     """Return a session-wide initialised database.

#     Drops all existing tables - Meta follows Postgres FKs
#     """
#     with app.app_context():
#         create_test_db(
#             database=app.config.get("DB_NAME"),
#             database_uri=app.config.get("SQLALCHEMY_DATABASE_URI"),
#         )

#         # The current DEV database uses UTC.
#         sess = _db.session()
#         sess.execute(text("SET TIME ZONE 'UTC';"))

#         _db.create_all()

#         yield _db

#         drop_test_db(
#             database=app.config.get("DB_NAME"),
#             database_uri=app.config.get("SQLALCHEMY_DATABASE_URI"),
#         )


@pytest.fixture(scope='function')
def session(app, db):  # pylint: disable=redefined-outer-name, invalid-name
    """Return a function-scoped session."""
    with app.app_context():
        conn = db.engine.connect()
        txn = conn.begin()

        options = dict(bind=conn, binds={})
        sess = db.create_scoped_session(options=options)

        # establish  a SAVEPOINT just before beginning the test
        # (http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#using-savepoint)
        sess.begin_nested()

        @event.listens_for(sess(), 'after_transaction_end')
        def restart_savepoint(sess2, trans):  # pylint: disable=unused-variable
            # Detecting whether this is indeed the nested transaction of the test
            if trans.nested and not trans._parent.nested:  # pylint: disable=protected-access
                # Handle where test DOESN'T session.commit(),
                sess2.expire_all()
                sess.begin_nested()

        db.session = sess

        sql = text('select 1')
        sess.execute(sql)

        yield sess

        # Cleanup
        sess.remove()
        # This instruction rollsback any commit that were executed in the tests.
        txn.rollback()
        conn.close()
    

# @pytest.fixture(scope="function")
# def session(app, db):  # pylint: disable=redefined-outer-name, invalid-name
#     """Return a function-scoped session."""
#     with app.app_context():
#         conn = db.engine.connect()
#         txn = conn.begin()

#         try:
#             options = dict(bind=conn, binds={})
#             # sess = db.create_scoped_session(options=options)
#             sess = db._make_scoped_session(options=options)
#         except Exception as err:
#             print(err)
#             print("done")

#         # establish  a SAVEPOINT just before beginning the test
#         # (http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#using-savepoint)
#         sess.begin_nested()

#         @event.listens_for(sess(), "after_transaction_end")
#         def restart_savepoint(sess2, trans):  # pylint: disable=unused-variable
#             # Detecting whether this is indeed the nested transaction of the test
#             if trans.nested and not trans._parent.nested:  # pylint: disable=protected-access
#                 # Handle where test DOESN'T session.commit(),
#                 sess2.expire_all()
#                 sess.begin_nested()

#         db.session = sess

#         sql = text("select 1")
#         sess.execute(sql)

#         yield sess

#         # Cleanup
#         sess.remove()
#         # This instruction rollsback any commit that were executed in the tests.
#         txn.rollback()
#         conn.close()