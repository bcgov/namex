import os

SOLR_CORE = 'possible.conflicts'

SOLR_URL = os.getenv('SOLR_BASE_URL', 'http://localhost:8983')
SOLR_API_URL = SOLR_URL + '/solr/'
