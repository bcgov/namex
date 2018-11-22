import os

import pytest
from dotenv import load_dotenv, find_dotenv

#this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())


integration_fdw_namex = pytest.mark.skipif((os.getenv('FDW_NAMEX_TESTS', False) is False),
                                           reason="requires access to PostgresFDW to Oracle NAMEX")
