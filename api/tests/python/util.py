import os

import pytest
from dotenv import load_dotenv, find_dotenv

#this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())


integration_oracle_namesdb = pytest.mark.skipif((os.getenv('ORACLE_NAMESDB_TESTS', False) is False),
                                                reason="requires access to Oracle NamesDB")

integration_fdw_namex = pytest.mark.skipif((os.getenv('FDW_NAMEX_TESTS', False) is False),
                                           reason="requires access to PostgresFDW to Oracle NAMEX")

integration_solr = pytest.mark.skipif((os.getenv('SOLR_TESTS', False) is False),
                                      reason="requires access to Solr")

integration_nro_extractor = pytest.mark.skipif((os.getenv('NRO_EXTRACTOR_TESTS', False) is False),
                                               reason="requires access to nor-extractor via HTTPS POST/PUT")
