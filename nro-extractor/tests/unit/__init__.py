"""
Expose the custom decorators used skip tests unless their environment variables are set

The presence any of the following env vars will let those tests run
set :
    ORACLE_NAMESDB_TESTS to run integration_oracle_namesdb
    FDW_NAMEX_TESTS to run integration_fdw_namex
    SOLR_TESTS to run integration_solr
    NRO_EXTRACTOR_TESTS to run integration_nro_extractor

"""
from .util import \
    integration_fdw_namex
