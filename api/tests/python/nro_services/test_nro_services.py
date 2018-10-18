from datetime import datetime
import os

import cx_Oracle
import pytest

from namex import nro

from tests.python import integration_oracle_namesdb


@integration_oracle_namesdb
def test_nro_connection_type(app):

    conn = nro.connection
    assert type(conn) is cx_Oracle.Connection


@integration_oracle_namesdb
def test_get_last_modified_timestamp(app):

    ts = nro.get_last_update_timestamp(1205761)
    assert type(ts) is datetime


@integration_oracle_namesdb
def test_set_status_2_h(app):

    nro.set_request_status_to_h('NR 5970035', 'anyname')


@integration_oracle_namesdb
def test_set_status_2_h_1(app):

    nro.set_request_status_to_h('NR xx', 'anyname')
