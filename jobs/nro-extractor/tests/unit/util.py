import os

import pytest
from dotenv import load_dotenv, find_dotenv

#this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())


integration_oracle_namesdb = pytest.mark.skipif((os.getenv('ORACLE_NAMESDB_TESTS', False) is False),
                                                reason="requires access to Oracle NamesDB")
