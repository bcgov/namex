from .solr import SolrQueries
from .restricted_words import RestrictedWords

VALID_ANALYSIS = SolrQueries.VALID_QUERIES + RestrictedWords.VALID_QUERIES
