# Copyright © 2025 Province of British Columbia
#
# Licensed under the BSD 3 Clause License, (the "License");
# you may not use this file except in compliance with the License.
# The template for the license can be found here
#    https://opensource.org/license/bsd-3-clause/
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""Create Oracle database connection.

These will get initialized by the application.
"""

from __future__ import annotations

import cx_Oracle
from flask import Flask, current_app, g


class OracleDB:  # pylint: disable=duplicate-code
    """Oracle database connection object for re-use in application."""

    def __init__(self, app=None):
        """initializer, supports setting the app context on instantiation."""
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Create setup for the extension.

        :param app: Flask app
        :return: naked
        """
        self.app = app
        app.teardown_appcontext(self.teardown)

    @staticmethod
    def teardown(exc=None):
        """Oracle session pool cleans up after itself."""
        print(f"teardown {exc}")  # noqa: T201
        pool = g.pop("_oracle_pool", None)

        if pool is not None:
            try:
                pool.close()
            except cx_Oracle.DatabaseError as err:
                current_app.logger.debug(err)

    @staticmethod
    def _create_pool():
        """Create the cx_oracle connection pool from the Flask Config Environment.

        :return: an instance of the OCI Session Pool
        """

        def init_session(conn, *args):
            cursor = conn.cursor()
            cursor.execute("alter session set TIME_ZONE = 'America/Vancouver'")

        dsn_val = (
            f"{current_app.config.get('ORACLE_HOST')}:"
            f"{current_app.config.get('ORACLE_PORT')}/"
            f"{current_app.config.get('ORACLE_DB_NAME')}"
        )

        return cx_Oracle.SessionPool(
            user=current_app.config.get("ORACLE_USER"),
            password=current_app.config.get("ORACLE_PASSWORD"),
            dsn=dsn_val,
            min=1,
            max=10,
            increment=1,
            getmode=cx_Oracle.SPOOL_ATTRVAL_NOWAIT,
            wait_timeout=1500,
            timeout=3600,
            session_callback=init_session,
        )

    @property
    def connection(self):
        """Create connection property.

        If this is running in a Flask context,
        then either get the existing connection pool or create a new one
        and then return an acquired session
        :return: cx_Oracle.connection type
        """
        if "_oracle_pool" not in g:
            g._oracle_pool = self._create_pool()  # pylint: disable=protected-access

        return g._oracle_pool.acquire()  # pylint: disable=protected-access


# export instance of this class
oracle_db = OracleDB()
