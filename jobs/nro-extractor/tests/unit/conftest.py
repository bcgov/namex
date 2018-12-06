import os
import logging
import json
import datetime

import cx_Oracle
import pytest
from flask import Flask, Blueprint
from flask.testing import FlaskClient
from sqlalchemy import event, text

from extractor.app import create_app, db as _db, nro as _nro
from config import TestConfig

from . import FROZEN_DATETIME, EPOCH_DATETIME


# fixture to freeze utcnow to a fixed date-time
@pytest.fixture
def patch_datetime_utcnow(monkeypatch):

    class _Datetime:
        @classmethod
        def utcnow(cls):
            return FROZEN_DATETIME

    monkeypatch.setattr(datetime, 'datetime', _Datetime)


@pytest.fixture(scope="session")
def app(request):
    """
    Returns session-wide application.
    """
    logging.log(logging.INFO, TestConfig().SQLALCHEMY_DATABASE_URI)
    app = create_app(TestConfig())

    return app

@pytest.fixture(scope="session")
def nro_connection(app):
    """
    so that we can use just one of the connections form the pool
    :param app: the app fixture
    :return: an cx_Oracle connection from namex.NROServices
    """
    return _nro.connection

@pytest.fixture
def client(app):

    client = app.test_client()

    return client


@pytest.fixture(scope="function")
def session(app, request):
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


@pytest.fixture(scope="function")
def namex_feeder(app, nro_connection):

    schema = """
    DROP TABLE NAMEX.NAMEX_FEEDER CASCADE CONSTRAINTS;

    CREATE TABLE NAMEX.NAMEX_FEEDER
    (
      ID              NUMBER(10)                    NOT NULL,
      TRANSACTION_ID  NUMBER(10)                    NOT NULL,
      STATUS          CHAR(1 BYTE)                  DEFAULT 'P'                   NOT NULL,
      NR_NUM          VARCHAR2(10 BYTE),
      ACTION          CHAR(1 BYTE),
      SEND_COUNT      NUMBER(10)                    DEFAULT 0,
      SEND_TIME       TIMESTAMP(6),
      ERROR_MSG       VARCHAR2(4000 BYTE)
);
"""
    cursor = nro_connection.cursor()

    print('creating namex feeder')

    # create schema
    schema_sql = [sql for sql in [x.strip() for x in schema.replace('\n','').replace('\t','').split(';')] if len(sql)>0]
    for sql in schema_sql:
        try:
            cursor.execute(sql)
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            if error.code != 942: # eat it, if it's a table not found in a drop call
                raise e
