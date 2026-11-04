# Copyright © 2023 Province of British Columbia
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
"""Create Oracle database connection.

These will get initialized by the application.
"""

from __future__ import annotations

import oracledb
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
            except oracledb.DatabaseError as err:
                current_app.logger.debug(err)

    @staticmethod
    def _create_pool():
        """Create the oracledb connection pool from the Flask Config Environment.

        :return: an instance of the OCI Session Pool
        """

        if not getattr(oracledb, "thick_mode", False):
            oracledb.init_oracle_client()

        def init_session(conn, *args):
            cursor = conn.cursor()
            cursor.execute("alter session set TIME_ZONE = 'America/Vancouver'")

        dsn_val = (
            f"{current_app.config.get('ORACLE_HOST')}:"
            f"{current_app.config.get('ORACLE_PORT')}/"
            f"{current_app.config.get('ORACLE_DB_NAME')}"
        )

        return oracledb.SessionPool(
            user=current_app.config.get("ORACLE_USER"),
            password=current_app.config.get("ORACLE_PASSWORD"),
            dsn=dsn_val,
            min=1,
            max=10,
            increment=1,
            getmode=oracledb.SPOOL_ATTRVAL_NOWAIT,
            wait_timeout=1500,
            timeout=3600,
            session_callback=init_session,
        )

    @property
    def connection(self):  # pylint: disable=inconsistent-return-statements
        """Create connection property.

        If this is running in a Flask context,
        then either get the existing connection pool or create a new one
        and then return an acquired session
        :return: oracledb.connection type
        """
        if "_oracle_pool" not in g:
            g._oracle_pool = self._create_pool()  # pylint: disable=protected-access

        return g._oracle_pool.acquire()  # pylint: disable=protected-access
