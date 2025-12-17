import os

import pytest
from dotenv import find_dotenv, load_dotenv

# Load environment variables from .env in project root
load_dotenv(find_dotenv())

integration_solr = pytest.mark.skipif(
    not os.getenv("SOLR_TESTS", False), reason="requires access to Solr"
)

integration_synonym_api = pytest.mark.skipif(
    not os.getenv("SOLR_SYNONYM_TESTS", False), reason="requires access to Solr Synonym API"
)

integration_postgres_solr = pytest.mark.skipif(
    not os.getenv("POSTGRES_SOLR_TESTS", False), reason="requires access to postgres_solr"
)
