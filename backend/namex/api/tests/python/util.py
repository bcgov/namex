import os

import pytest
from dotenv import find_dotenv, load_dotenv

# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())


integration_oracle_local_namesdb = pytest.mark.skipif(
    (os.getenv('ORACLE_NAMESDB_LOCAL_TESTS', False) is False), reason='fake schema will be created'
)

integration_oracle_namesdb = pytest.mark.skipif(
    (os.getenv('ORACLE_NAMESDB_TESTS', False) is False), reason='requires access to Oracle NamesDB'
)

integration_fdw_namex = pytest.mark.skipif(
    (os.getenv('FDW_NAMEX_TESTS', False) is False), reason='requires access to PostgresFDW to Oracle NAMEX'
)

integration_solr = pytest.mark.skipif((os.getenv('SOLR_TESTS', False) is False), reason='requires access to Solr')

integration_synonym_api = pytest.mark.skipif(
    (os.getenv('SOLR_SYNONYM_TESTS', False) is False), reason='requires access to Solr Synonym API'
)

integration_postgres_solr = pytest.mark.skipif(
    (os.getenv('POSTGRES_SOLR_TESTS', False) is False), reason='requires access to postgres_solr'
)

integration_nro_extractor = pytest.mark.skipif(
    (os.getenv('NRO_EXTRACTOR_TESTS', False) is False), reason='requires access to nor-extractor via HTTPS POST/PUT'
)

integration_mras = pytest.mark.skipif(
    (os.getenv('MRAS_TESTS', False) is False), reason='requires access to MRAS via HTTPS GET'
)
