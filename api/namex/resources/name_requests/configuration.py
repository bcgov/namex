import os

SOLR_CORE = 'possible.conflicts'

SOLR_URL = os.getenv('SOLR_BASE_URL')
SOLR_API_URL = SOLR_URL + '/solr/'
