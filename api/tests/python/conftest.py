import pytest
from pytest_mock import mocker

from app import create_app, jwt as _jwt
from flask import current_app
from app.models import db as _db
from sqlalchemy import event, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData, DropConstraint
from flask_migrate import Migrate, upgrade
import sys
import os

@pytest.fixture(scope="session")
def app(request):
    """
    Returns session-wide application.
    """
    app = create_app('testing')

    return app


@pytest.fixture(scope="session")
def client(app):
    """
    Returns session-wide Flask test client.
    """
    return app.test_client()

@pytest.fixture(scope="session")
def jwt(app):
    """
    Returns session-wide jwt manager
    """
    return _jwt


@pytest.fixture(scope="session")
def client_ctx(app):
    """
    Returns session-wide Flask test client.
    """
    with app.test_client() as c:
        yield c


@pytest.fixture(scope="session")
def db(app, request):
    """
    Returns session-wide initialised database.
    Drops all existing tables - Meta follows Postgres FKs
    """
    with app.app_context():
        # Clear out any existing tables
        metadata = MetaData(_db.engine)
        metadata.reflect()
        for table in metadata.tables.values():
            for fk in table.foreign_keys:
                _db.engine.execute(DropConstraint(fk.constraint))
        metadata.drop_all()
        _db.drop_all()

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


@pytest.fixture(scope="function", autouse=True)
def session(app, db, request):
    """
    Returns function-scoped session.
    """
    with app.app_context():
        conn = _db.engine.connect()
        txn = conn.begin()

        options = dict(bind=conn, binds={})
        sess = _db.create_scoped_session(options=options)

        # establish  a SAVEPOINT just before beginning the test
        # (http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#using-savepoint)
        sess.begin_nested()

        @event.listens_for(sess(), 'after_transaction_end')
        def restart_savepoint(sess2, trans):
            # Detecting whether this is indeed the nested transaction of the test
            if trans.nested and not trans._parent.nested:
                # Handle where test DOESN'T session.commit(),
                sess2.expire_all()
                sess.begin_nested()

        _db.session = sess

        sql = text('select 1')
        sess.execute(sql)

        yield sess

        # Cleanup
        sess.remove()
        # This instruction rollsback any commit that were executed in the tests.
        txn.rollback()
        conn.close()
