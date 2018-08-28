from flask import current_app
from urllib import request, parse
import json


# Use this character in the search strings to indicate that the word should not by synonymized.
NO_SYNONYMS_INDICATOR = '@'

# Prefix used to indicate that words are not to have synonyms.
NO_SYNONYMS_PREFIX = '&fq=name_copy:'


class SolrQueries:

    CONFLICTS = 'conflicts'
    HISTORY = 'histories'
    TRADEMARKS = 'trademarks'
    RESTRICTED_WORDS = 'restricted_words'
    VALID_QUERIES = [CONFLICTS, HISTORY, TRADEMARKS]

    #
    # Prototype:
    #     /solr/<core name>/select? ... &q={name} ... &wt=json&start={start}&rows={rows}&fl=source,id,name,score
    #
    queries = {
        CONFLICTS: '/solr/possible.conflicts/select?defType=edismax&hl.fl=name&hl.simple.post=%3C/b%3E&'
                   'hl.simple.pre=%3Cb%3E&hl=on&indent=on&mm=75%25&q={name}&qf=name&wt=json&start={start}&'
                   'rows={rows}&fl=source,id,name,score{name_copy_clause}',
        HISTORY: '/solr/names/select?defType=edismax&hl.fl=name&hl.simple.post=%3C/b%3E&hl.simple.pre=%3Cb%3E&hl=on&'
                 'indent=on&mm=75%25&q={name}&qf=name&wt=json&start={start}&rows={rows}&'
                 'fl=nr_num,name,score,submit_count,name_state_type_cd{name_copy_clause}',
        TRADEMARKS: '/solr/trademarks/select?defType=edismax&hl.fl=name&hl.simple.post=%3C/b%3E&hl.simple.pre=%3Cb%3E&'
                    'hl=on&indent=on&mm=75%25&q={name}&qf=name&wt=json&start={start}&rows={rows}&'
                    'fl=application_number,name,status,description,score&bq=status:REGISTERED^5.0{name_copy_clause}'
    }

    @classmethod
    def get_results(cls, query_type, name, start=0, rows=10):

        solr_base_url = current_app.config.get('SOLR_BASE_URL', None)
        if not solr_base_url:
            current_app.logger.error('SOLR: SOLR_BASE_URL is not set')
            return None, 'Internal server error', 500

        if query_type not in SolrQueries.VALID_QUERIES:
            return None, 'Not a valid analysis type', 400

        current_app.logger.debug('Solr Query - type:{qtype} - name:{name}'
                                 .format(qtype=query_type, name=parse.quote(name)))
        query = solr_base_url + SolrQueries.queries[query_type].format(
            start=start,
            rows=rows,
            name=parse.quote(name.replace(NO_SYNONYMS_INDICATOR, '')),
            name_copy_clause=cls._get_name_copy_clause(name)
        )
        current_app.logger.debug('Query: ' + query)
        try:
            connection = request.urlopen(query)
        except Exception as err:
            current_app.logger.error(err, query)
            return None, 'Internal server error', 500

        solr = json.load(connection)
        results = {"response": {"numFound": solr['response']['numFound'],
                                "start": solr['response']['start'],
                                "rows": solr['responseHeader']['params']['rows'],
                                "maxScore": solr['response']['maxScore'],
                                "name": solr['responseHeader']['params']['q']
                                },
                   'names': solr['response']['docs'],
                   'highlighting': solr['highlighting']}

        return results, '', None

    # The NO_SYNONYMS_INDICATOR is used to prefix a word or phrase that is not to be to synonymized. The decision was
    # made that the indicator would not be used within double quotes, and that mixing it with search meta-characters is
    # not a defined operation.
    #
    # - 'NO INDICATOR' > ''
    # - '@ONE INDICATOR' > 'ONE'
    # - '@MAYBE @TWO INDICATORS' > 'MAYBE TWO'
    # - '@"SOME PHRASE" ALLOWED' > '"SOME PHRASE"'
    #
    # This is far from exhaustive and very GIGO.
    @classmethod
    def _get_name_copy_clause(cls, name):
        clause = ''

        # There's no easy way to split the name with whitespace as a delimiter, because quotes can be used to preserve
        # terms with internal whitespace and additionally the quotes may also be prefixed with +, -, or *, or
        # combinations of such.
        unsynonymed_words = []

        word = ''
        indicator_on = False
        quotes_on = False
        for letter in name:
            if letter == NO_SYNONYMS_INDICATOR:
                # Only allow the indicator outside of quotes.
                if not quotes_on:
                    indicator_on = True
    
                continue

            if letter == '"':
                quotes_on = not quotes_on

                if not indicator_on:
                    continue

            if letter == ' ' and not quotes_on:
                if indicator_on:
                    unsynonymed_words.append(word)
                    word = ''
                    indicator_on = False

                continue

            if indicator_on:
                word += letter

        # Handle when the last word was prefixed with the indicator.
        if indicator_on:
            unsynonymed_words.append(word)

        if len(unsynonymed_words) != 0:
            clause = NO_SYNONYMS_PREFIX + ' '.join(unsynonymed_words)

        return clause


'''
https://namex-solr-test.pathfinder.gov.bc.ca/solr/names/select?defType=edismax&fq=name_copy:RED&indent=on&mm=75%&q=RED
CLEANING SERVICES LTD.&qf=name&wt=json

this is the one that will get passed from the front-end with the *RED CLEANING SERVICES LTD so that Red will not be
substituted with the synonyms. the clause &fq=name_copy:RED is what says only give me back he ones with RED.
'''
