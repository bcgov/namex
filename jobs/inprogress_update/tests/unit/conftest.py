"""This is test config."""

import datetime
import logging
from unittest.mock import patch

import pytest
from sqlalchemy import event, text

from config import TestConfig
from inprogress_update.inprogress_update import create_app
from inprogress_update.inprogress_update import db as _db

from . import FROZEN_DATETIME


# Mock Pub/Sub queue publish for all tests
@pytest.fixture(autouse=True)
def mock_pubsub_publish():
    with patch('gcp_queue.gcp_queue.GcpQueue.publish') as mock_publish:
        mock_publish.return_value = None
        yield mock_publish


# fixture to freeze utcnow to a fixed date-time
@pytest.fixture
def patch_datetime_utcnow(monkeypatch):
    """Return the FROZEN_DATETIME."""
    class _Datetime:
        @classmethod
        def utcnow(cls):
            return FROZEN_DATETIME

    monkeypatch.setattr(datetime, 'datetime', _Datetime)


@pytest.fixture(scope='session')
def app(request):
    """Returns session-wide application."""
    logging.log(logging.INFO, TestConfig().SQLALCHEMY_DATABASE_URI)
    app = create_app(TestConfig())

    return app


@pytest.fixture
def client(app):
    """Returns client."""
    client = app.test_client()

    return client


@pytest.fixture(scope='function')
def session(app, request):
    """
    Returns function-scoped session.
    """
    with app.app_context():
        conn = _db.engine.connect()
        txn = conn.begin()

        sess = _db.session
        # establish a SAVEPOINT just before beginning the test
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
