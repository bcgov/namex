from app import api
from urllib import request, parse
import json
import logging


SOLR_BASE_URL = api.app.config.get('SOLR_BASE_URL', None)

if not SOLR_BASE_URL:
    logging.log(logging.ERROR, 'SOLR: SOLR_BASE_URL is not set')
    raise Exception('SOLR config error')


class SolrQueries:

    CONFLICTS='conflicts'
    HISTORY='histories'
    TRADEMARKS='trademarks'
    RESTRICTED_WORDS='restricted_words'
    VALID_QUERIES=[CONFLICTS, HISTORY, TRADEMARKS, RESTRICTED_WORDS]

    queries ={
        'similar': '/solr/{core}/select?q=id:{name}&wt=json',
        CONFLICTS: '/solr/possible.conflicts/select?indent=on&start={start}&rows={rows}&defType=dismax&fl=source,id,name,score&hl.fl=name&hl.simple.post=%3C/b%3E&hl.simple.pre=%3Cb%3E&hl=on&indent=on&pf=name%5E100&q=name:{name}&qf=name&wt=json',
        HISTORY: '/solr/names/select?defType=dismax&indent=on&start={start}&rows={rows}&defType=dismax&fl=source,id,name,score&hl.fl=name&hl.simple.post=%3C/b%3E&hl.simple.pre=%3Cb%3E&hl=on&pf=name%5E100&q=name:{name}&qf=name&wt=json',
        TRADEMARKS: '/solr/trademarks/select?defType=dismax&indent=on&start={start}&rows={rows}&defType=dismax&fl=source,id,name,score&hl.fl=name&hl.simple.post=%3C/b%3E&hl.simple.pre=%3Cb%3E&hl=on&pf=name%5E100&q=name:{name}&qf=name&wt=json'
    }


    @classmethod
    def get_results(cls, query_type, name, start=0, rows=10):

        if query_type not in SolrQueries.VALID_QUERIES:
            return None

        query = SOLR_BASE_URL + SolrQueries.queries[query_type].format(
            start=start,
            rows=rows,
            name=parse.quote(name)
        )
        try:
            connection = request.urlopen(query)
        except Exception as err:
            logging.log(logging.ERROR, err, query)
            raise err
        return json.load(connection)

