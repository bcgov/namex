from flask import current_app
from urllib import request, parse
import json


class SolrQueries:

    CONFLICTS='conflicts'
    HISTORY='histories'
    TRADEMARKS='trademarks'
    RESTRICTED_WORDS='restricted_words'
    VALID_QUERIES=[CONFLICTS, HISTORY, TRADEMARKS, RESTRICTED_WORDS]

    #
    # Prototype: /solr/<core name>/select? ... &start={start}&rows={rows} ... &fl=source,id,name,score ... &q=name:{name} ... &wt=json'
    #
    queries ={
        CONFLICTS: '/solr/possible.conflicts/select?indent=on&start={start}&rows={rows}&defType=dismax&fl=source,id,name,score&hl.fl=name&hl.simple.post=%3C/b%3E&hl.simple.pre=%3Cb%3E&hl=on&pf=name%5E100&q=name:{name}&qf=name&wt=json',
        HISTORY:   '/solr/names/select?indent=on&start={start}&rows={rows}&defType=dismax&fl=nr_num,name,score&hl.fl=name&hl.simple.post=%3C/b%3E&hl.simple.pre=%3Cb%3E&hl=on&pf=name%5E100&q=name:{name}&qf=name&wt=json',
        TRADEMARKS: '/solr/trademarks/select?defType=dismax&indent=on&start={start}&rows={rows}&defType=dismax&fl=application_number,name,status,description,score&hl.fl=name&hl.simple.post=%3C/b%3E&hl.simple.pre=%3Cb%3E&hl=on&pf=name%5E100&q=name:{name}&qf=name&wt=json'
    }


    @classmethod
    def get_results(cls, query_type, name, start=0, rows=10):

        SOLR_BASE_URL = current_app.config.get('SOLR_BASE_URL', None)
        if not SOLR_BASE_URL:
            current_app.logger.error('SOLR: SOLR_BASE_URL is not set')
            raise Exception('SOLR config error')

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
            current_app.logger.error(err, query)
            raise err

        return json.load(connection)

