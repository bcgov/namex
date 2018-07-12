from flask import current_app
from urllib import request, parse
import json


class SolrQueries:

    CONFLICTS='conflicts'
    HISTORY='histories'
    TRADEMARKS='trademarks'
    RESTRICTED_WORDS='restricted_words'
    VALID_QUERIES=[CONFLICTS, HISTORY, TRADEMARKS]

    #
    # Prototype:
    #     /solr/<core name>/select? ... &q=name:{name} ... &wt=json&start={start}&rows={rows}&fl=source,id,name,score
    #
    queries = {
        CONFLICTS: '/solr/possible.conflicts/select?defType=edismax&hl.fl=name&hl.simple.post=%3C/b%3E&'
                   'hl.simple.pre=%3Cb%3E&hl=on&indent=on&mm=75%25&q=name:{name}&qf=name&wt=json&start={start}&'
                   'rows={rows}&fl=source,id,name,score',
        HISTORY: '/solr/names/select?defType=edismax&hl.fl=name&hl.simple.post=%3C/b%3E&hl.simple.pre=%3Cb%3E&hl=on&'
                 'indent=on&mm=75%25&q=name:{name}&qf=name&wt=json&start={start}&rows={rows}&fl=nr_num,name,score',
        TRADEMARKS: '/solr/trademarks/select?defType=edismax&hl.fl=name&hl.simple.post=%3C/b%3E&hl.simple.pre=%3Cb%3E&'
                    'hl=on&indent=on&mm=75%25&q=name:{name}&qf=name&wt=json&start={start}&rows={rows}&'
                    'fl=application_number,name,status,description,score&bq=status:REGISTERED^5.0'
    }

    @classmethod
    def get_results(cls, query_type, name, start=0, rows=10):

        solr_base_url = current_app.config.get('SOLR_BASE_URL', None)
        if not solr_base_url:
            current_app.logger.error('SOLR: SOLR_BASE_URL is not set')
            return None, 'Internal server error', 500

        if query_type not in SolrQueries.VALID_QUERIES:
            return None, 'Not a valid analysis type', 400

        query = solr_base_url + SolrQueries.queries[query_type].format(
            start=start,
            rows=rows,
            name=parse.quote(name)
        )
        try:
            connection = request.urlopen(query)
        except Exception as err:
            current_app.logger.error(err, query)
            return None, 'Internal server error', 500

        solr=json.load(connection)
        results = {"response": {"numFound": solr['response']['numFound'],
                                  "start": solr['response']['start'],
                                  "rows": solr['responseHeader']['params']['rows'],
                                  "maxScore": solr['response']['maxScore'],
                                  "name": solr['responseHeader']['params']['q'][5:]
                                  },
                     'names': solr['response']['docs'],
                     'highlighting': solr['highlighting']}

        return results, '', None

