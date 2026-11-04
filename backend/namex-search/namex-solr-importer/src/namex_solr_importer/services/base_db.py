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
"""Base db connection class."""

import os
from dataclasses import dataclass

from google.cloud.sql.connector import Connector
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker


@dataclass
class DBConfig:
    """Database configuration settings for IAM authentication."""

    database: str
    user: str  # IAM user email format: "user@project.iam"
    enable_iam_auth: bool = True
    credentials_path: str | None = None
    instance_connection_name: str | None = None  # Format: "project:region:instance"
    # NOTE: below is only used when not connecting via instance_connection_name
    host: str | None = None
    password: str | None = None
    port: str | None = None


class BaseDB:
    """Database connection using IAM authentication."""

    def __init__(self, db_config: DBConfig, test_connection=True):
        """Initialize the db connection."""
        if not db_config.instance_connection_name:
            connect_string = f"postgresql://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}"
            self.engine = create_engine(connect_string)
        else:
            # NOTE: GOOGLE_APPLICATION_CREDENTIALS is used during the connector init
            # - this can be changed safely afterwards for other db connections using this base class
            # - alternatively, this could be altered to get the google credentials ourselves via the path instead
            #   and pass those into the connector init. This is relying on the default which relies on this env var during init
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = db_config.credentials_path
            self.connector = Connector()
            self.engine = create_engine(
                "postgresql+pg8000://",
                creator=lambda: self._get_iam_connection(db_config),
                pool_size=5,
                max_overflow=2,
                pool_timeout=10,
                pool_recycle=1800,
                connect_args={"use_native_uuid": False},
            )

        if test_connection:
            self._test_connection()

    def _get_iam_connection(self, db_config: DBConfig):
        """Establish connection using IAM authentication."""
        return self.connector.connect(
            db_config.instance_connection_name,
            "pg8000",
            ip_type="public",
            db=db_config.database,
            user=db_config.user,
            enable_iam_auth=db_config.enable_iam_auth,
        )

    def _test_connection(self):
        """Test the database connection using proper SQLAlchemy text() construct."""
        with self.engine.connect() as conn:
            # Wrap the SQL string in text() for proper execution
            result = conn.execute(text("SELECT version()")).fetchone()
            print(f"Connection successful. Database version: {result[0]}")  # noqa: T201

    def teardown(self):
        """Clean up resources."""
        if self.connector:
            self.connector.close()

    @property
    def session(self):
        """Provide a database session."""
        return scoped_session(sessionmaker(bind=self.engine))
