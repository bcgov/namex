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
"""All of the configuration for the service is captured here.

All items are loaded, or have Constants defined here that
are loaded into the Flask configuration.
All modules and lookups get their configuration from the
Flask config, rather than reading environment variables directly
or by accessing this configuration directly.
"""

import os

from dotenv import find_dotenv, load_dotenv

# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())


class Config:
    """Base class configuration that should set reasonable defaults.

    Used as the base for all the other configurations.
    """

    DEBUG = False
    DEVELOPMENT = False
    TESTING = False

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    # Retry settings
    SOLR_RETRY_TOTAL = int(os.getenv("SOLR_RETRY_TOTAL", "2"))
    SOLR_RETRY_BACKOFF_FACTOR = int(os.getenv("SOLR_RETRY_BACKOFF_FACTOR", "5"))

    SOLR_API_URL = os.getenv("SOLR_API_URL", "http://")

    BATCH_SIZE = int(os.getenv("SOLR_BATCH_UPDATE_SIZE", "1000"))
    REINDEX_CORE = os.getenv("REINDEX_CORE", "False") == "True"
    ENABLE_OPTIMIZE = os.getenv("ENABLE_OPTIMIZE", "True") == "True"

    MODERNIZED_LEGAL_TYPES = (
        os.getenv("MODERNIZED_LEGAL_TYPES", "BEN,CBEN,CP,GP,SP").upper().split(",")
    )
    # TODO: confirm this list (all other legal types will be ignored)
    CONFLICT_LEGAL_TYPES = (
        os.getenv("CONFLICT_LEGAL_TYPES", "A,BC,BEN,C,CBEN,CCC,CP,CUL,ULC")
        .upper()
        .split(",")
    )

    INCLUDE_COLIN_LOAD = os.getenv("INCLUDE_COLIN_LOAD", "True") == "True"
    INCLUDE_LEAR_LOAD = os.getenv("INCLUDE_LEAR_LOAD", "True") == "True"
    INCLUDE_NAMEX_LOAD = os.getenv("INCLUDE_NAMEX_LOAD", "True") == "True"
    INCLUDE_SYNONYM_LOAD = os.getenv("INCLUDE_SYNONYM_LOAD", "True") == "True"
    RESYNC_OFFSET = os.getenv("RESYNC_OFFSET", "60")

    IS_PARTIAL_IMPORT = not INCLUDE_COLIN_LOAD or not INCLUDE_NAMEX_LOAD

    # Service account details
    ACCOUNT_SVC_AUTH_URL = os.getenv("ACCOUNT_SVC_AUTH_URL")
    ACCOUNT_SVC_CLIENT_ID = os.getenv("ACCOUNT_SVC_CLIENT_ID")
    ACCOUNT_SVC_CLIENT_SECRET = os.getenv("ACCOUNT_SVC_CLIENT_SECRET")
    try:
        ACCOUNT_SVC_TIMEOUT = int(os.getenv("ACCOUNT_SVC_TIMEOUT", "20"))
    except BaseException:  # pylint: disable=bare-except;  # pylint: disable=broad-exception-caught
        ACCOUNT_SVC_TIMEOUT = 20

    # ORACLE - CDEV/CTST/CPRD
    ORACLE_USER = os.getenv("ORACLE_USER", "")
    ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "")
    ORACLE_DB_NAME = os.getenv("ORACLE_DB_NAME", "")
    ORACLE_HOST = os.getenv("ORACLE_HOST", "")
    ORACLE_PORT = int(os.getenv("ORACLE_PORT", "1521"))

    # POSTGRESQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # NameX db
    DB_USER = os.getenv("DATABASE_USERNAME", "")
    DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
    DB_NAME = os.getenv("DATABASE_NAME", "")
    DB_HOST = os.getenv("DATABASE_HOST", "")
    DB_PORT = os.getenv("DATABASE_PORT", "5432")
    DB_CONNECTION_NAME = os.getenv("DATABASE_CONNECTION_NAME")
    GOOGLE_APPLICATION_CREDENTIALS_NAMEX = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS_NAMEX", "sa-secret/namex/secret.json"
    )

    # Lear db
    LEAR_DB_USER = os.getenv("LEAR_DATABASE_USERNAME", "")
    LEAR_DB_PASSWORD = os.getenv("LEAR_DATABASE_PASSWORD", "")
    LEAR_DB_NAME = os.getenv("LEAR_DATABASE_NAME", "")
    LEAR_DB_HOST = os.getenv("LEAR_DATABASE_HOST", "")
    LEAR_DB_PORT = os.getenv("LEAR_DATABASE_PORT", "5432")
    LEAR_DB_CONNECTION_NAME = os.getenv("LEAR_DATABASE_CONNECTION_NAME")
    GOOGLE_APPLICATION_CREDENTIALS_LEAR = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS_LEAR", "sa-secret/lear/secret.json"
    )

    # Connection pool settings
    DB_MIN_POOL_SIZE = os.getenv("DATABASE_MIN_POOL_SIZE", "2")
    DB_MAX_POOL_SIZE = os.getenv("DATABASE_MAX_POOL_SIZE", "10")
    DB_CONN_WAIT_TIMEOUT = os.getenv("DATABASE_CONN_WAIT_TIMEOUT", "5")
    DB_CONN_TIMEOUT = os.getenv("DATABASE_CONN_TIMEOUT", "900")

    SQLALCHEMY_ENGINE_OPTIONS = {  # noqa: RUF012
        "pool_pre_ping": True,
        "pool_size": int(DB_MIN_POOL_SIZE),
        "max_overflow": (int(DB_MAX_POOL_SIZE) - int(DB_MIN_POOL_SIZE)),
        "pool_recycle": int(DB_CONN_TIMEOUT),
        "pool_timeout": int(DB_CONN_WAIT_TIMEOUT),
    }

    # Cache stuff
    CACHE_TYPE = os.getenv("CACHE_TYPE", "FileSystemCache")
    CACHE_DIR = os.getenv("CACHE_DIR", "cache")
    try:
        CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", "300"))
    except (TypeError, ValueError):
        CACHE_DEFAULT_TIMEOUT = 300


class DevelopmentConfig(Config):
    """Config object for development environment."""

    DEBUG = True
    DEVELOPMENT = True
    TESTING = False


class UnitTestingConfig(Config):
    """Config object for unit testing environment."""

    DEBUG = True
    DEVELOPMENT = False
    TESTING = True
    # TODO: update these when tests are ready
    INCLUDE_NAMEX_LOAD = False
    INCLUDE_SYNONYM_LOAD = False
    INCLUDE_COLIN_LOAD = False
    INCLUDE_LEAR_LOAD = False

    SOLR_API_URL = "http://test.SOLR_API_URL.fake"

    # Service account details
    ACCOUNT_SVC_AUTH_URL = "http://test.account-svc-url.fake"

    # ORACLE - CDEV/CTST/CPRD
    ORACLE_USER = os.getenv("ORACLE_TEST_USER", "")
    ORACLE_PASSWORD = os.getenv("ORACLE_TEST_PASSWORD", "")
    ORACLE_DB_NAME = os.getenv("ORACLE_TEST_DB_NAME", "")
    ORACLE_HOST = os.getenv("ORACLE_TEST_HOST", "")
    ORACLE_PORT = int(os.getenv("ORACLE_TEST_PORT", "1521"))

    # NameX
    DB_USER = os.getenv("DATABASE_TEST_USERNAME", "")
    DB_PASSWORD = os.getenv("DATABASE_TEST_PASSWORD", "")
    DB_NAME = os.getenv("DATABASE_TEST_NAME", "")
    DB_HOST = os.getenv("DATABASE_TEST_HOST", "")
    DB_PORT = os.getenv("DATABASE_TEST_PORT", "5432")
    DB_CONNECTION_NAME = os.getenv("DATABASE_TEST_CONNECTION_NAME")
    GOOGLE_APPLICATION_CREDENTIALS_NAMEX = "fake"

    # Lear db
    LEAR_DB_USER = os.getenv("LEAR_TEST_DATABASE_USERNAME", "")
    LEAR_DB_PASSWORD = os.getenv("LEAR_TEST_DATABASE_PASSWORD", "")
    LEAR_DB_NAME = os.getenv("LEAR_TEST_DATABASE_NAME", "")
    LEAR_DB_HOST = os.getenv("LEAR_TEST_DATABASE_HOST", "")
    LEAR_DB_PORT = os.getenv("LEAR_TEST_DATABASE_PORT", "5432")
    LEAR_DB_CONNECTION_NAME = os.getenv("LEAR_TEST_DATABASE_CONNECTION_NAME")
    GOOGLE_APPLICATION_CREDENTIALS_LEAR = "fake"

    # Synonyms db
    SYN_DB_USER = os.getenv("SYN_TEST_DATABASE_USERNAME", "")
    SYN_DB_PASSWORD = os.getenv("SYN_TEST_DATABASE_PASSWORD", "")
    SYN_DB_NAME = os.getenv("SYN_TEST_DATABASE_NAME", "")
    SYN_DB_HOST = os.getenv("SYN_TEST_DATABASE_HOST", "")
    SYN_DB_PORT = os.getenv("SYN_TEST_DATABASE_PORT", "5432")
    SYN_DB_CONNECTION_NAME = os.getenv("SYN_TEST_DATABASE_CONNECTION_NAME")
    GOOGLE_APPLICATION_CREDENTIALS_SYN = "fake"


class ProductionConfig(Config):
    """Config object for production environment."""

    DEBUG = False
    DEVELOPMENT = False
    TESTING = False
