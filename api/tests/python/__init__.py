"""
Expose the custom decorators used skip tests unless their environment variables are set

The presence any of the following env vars will let those tests run
set :
    ORACLE_NAMESDB_TESTS to run integration_oracle_namesdb
    FDW_NAMEX_TESTS to run integration_fdw_namex
    SOLR_TESTS to run integration_solr
    NRO_EXTRACTOR_TESTS to run integration_nro_extractor
"""

import datetime

from .util import (
    integration_oracle_local_namesdb,
    integration_oracle_namesdb,
    integration_fdw_namex,
    integration_solr,
    integration_synonym_api,
    integration_postgres_solr,
    integration_mras,
    integration_nro_extractor,
)

EPOCH_DATETIME = datetime.datetime.utcfromtimestamp(0)
FROZEN_DATETIME = datetime.datetime(2001, 8, 5, 7, 7, 58, 272362)
