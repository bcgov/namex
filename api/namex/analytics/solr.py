import json
import re
from urllib import parse, request

import requests
from flask import current_app

from namex.analytics.phonetic import (
    designations,
    first_consonants,
    first_vowels,
    has_leading_vowel,
    replace_special_leading_sounds,
)

# Use this character in the search strings to indicate that the word should not by synonymized.
NO_SYNONYMS_INDICATOR = '@'

WILD_CARD = '*'

# Constant names for useful chars used by the functions below
RESERVED_CHARACTERS = '-+@"'
DOUBLE_QUOTE = '"'
HYPHEN = '-'

# Prefix used to indicate that words are not to have synonyms.
NO_SYNONYMS_PREFIX = '&fq=name_copy:'

# Prefix used to indicate that we have synonyms.
SYNONYMS_PREFIX = '&fq=name_with_synonyms:'


class SolrQueries:
    PROX_SYN_CONFLICTS = 'proxsynconflicts'
    OLD_SYN_CONFLICTS = 'oldsynconflicts'
    COBRS_PHONETIC_CONFLICTS = 'cobrsphonconflicts'
    PHONETIC_CONFLICTS = 'phonconflicts'
    CONFLICTS = 'conflicts'
    HISTORY = 'histories'
    TRADEMARKS = 'trademarks'
    RESTRICTED_WORDS = 'restricted_words'
    NAME_NR_SEARCH = 'name_nr_search'
    VALID_QUERIES = [CONFLICTS, HISTORY, TRADEMARKS]


    @classmethod
    def get_bearer_token(cls) -> str:
        auth_url = current_app.config.get('ENTITY_SVC_AUTH_URL', '')
        client_id = current_app.config.get('ENTITY_SERVICE_ACCOUNT_CLIENT_ID', '')
        client_secret = current_app.config.get('ENTITY_SERVICE_ACCOUNT_CLIENT_SECRET', '')

        resp = requests.post(
            auth_url,
            auth=(client_id, client_secret),
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': client_secret
            }
        )

        if resp.status_code != 200:
            return None
        return resp.json().get('access_token')


    @classmethod
    def get_conflict_results(cls, name, start=0, rows=100):
        solr_api_url = current_app.config.get('SOLR_API_URL', None)
        solr_api_version = current_app.config.get('SOLR_API_VERSION', None)

        if not solr_api_url :
            current_app.logger.error('SOLR: SOLR_API_URL is not set')
            return None, 'Internal server error', 500

        if not solr_api_version :
            current_app.logger.error('SOLR: SOLR_API_VERSION is not set')
            return None, 'Internal server error', 500

        url =  solr_api_url + solr_api_version + '/search/possible-conflict-names'

        # handle non-ascii chars in name
        name = ''.join([i if ord(i) < 128 else parse.quote(i) for i in name])
        name = cls.remove_stopwords_designations(name)

        request_json = {
            'query': {
                'value': name,
                'corp_num': '',
                'nr_num': '',
                'name': ''
            },
            'start': start,
            'rows': rows
        }

        resp = requests.post(
            url=url,
            json=request_json,
            headers={'Authorization': f'Bearer {cls.get_bearer_token()}'}
        )

        if resp.status_code != 200:
            return None, 'Internal server error', 500

        data = resp.json()
        seen = set()
        exact_matches = []
        similar_matches = []

        for r in data.get('searchResults', {}).get('results', []):
            n = r.get('name')
            if n in seen:
                continue
            seen.add(n)

            if n == name:
                r['type'] = 'exact'
                exact_matches.append(r)
            else:
                r['type'] = 'similar'
                similar_matches.append(r)

        return {
            'names': similar_matches,
            'exactNames': exact_matches
        }, '', None

    @classmethod
    def get_name_nr_search_results(cls, solr_query, start=0, rows=10):
        """Search for the query param in `names` core."""
        solr_base_url = current_app.config.get('SOLR_BASE_URL', None)
        if not solr_base_url:
            current_app.logger.error('SOLR: SOLR_BASE_URL is not set')
            return None, 'Internal server error', 500

        try:
            query = solr_base_url + SolrQueries.queries[SolrQueries.NAME_NR_SEARCH].format(
                start=start, rows=rows, query=solr_query
            )
            current_app.logger.debug('Query: ' + query)
            connection = request.urlopen(query)
        except Exception as err:
            current_app.logger.error(err, query)
            return None, 'Internal server error', 500

        try:
            solr = json.load(connection)
            results = {
                'response': {
                    'numFound': solr['response']['numFound'],
                    'start': solr['response']['start'],
                    'rows': solr['responseHeader']['params']['rows'],
                    'maxScore': solr['response']['maxScore'],
                    'name': solr['responseHeader']['params']['q'],
                },
                'names': solr['response']['docs'],
            }
            return results, '', None
        except Exception as err:
            current_app.logger.error(err, query)
            return None, 'Internal server error', 500

    @classmethod
    def get_parsed_query_name_nr_search(cls, value: str):
        """Build query to search nr number or name.

        - `None` -> *:*
        - NR 1234567 -> nr_num:*1234567*
        - HNR239 HOLDINGS -> (name_copy:*HNR239* AND name_copy:*HOLDINGS*)
        - NR 955 HNR239 HOLDINGS -> nr_num:*955* AND (name_copy:*HNR239* AND name_copy:*HOLDINGS)
        - HNR239 HOLDINGS NR 955 -> nr_num:*955* AND (name_copy:*HNR239* AND name_copy:*HOLDINGS)
        - HNR239 NR 955 HOLDINGS -> nr_num:*955* OR
                                (name_copy:*HNR239* AND name_copy:*NR* AND name_copy:*955* AND name_copy:*HOLDINGS)
        """
        solr_query = '*:*'
        nr_number = None
        if value:
            value = value.strip()

            nr_num = ''
            # match whole/start/end string  NR 1234567, NR1234567
            nr_num_regex = r'(^(NR( |)[0-9]+)$)|(^(NR( |)[0-9]+)\s)|(\s(NR( |)[0-9]+)$)'
            nr_num_fallback_regex = r'(^[0-9]+$)|(^[0-9]+\s)|(\s[0-9]+$)'  # 1234567
            if result := re.search(nr_num_regex, value, re.IGNORECASE):
                matching_nr = result.group()
                nr_number = re.sub('NR', '', matching_nr, flags=re.IGNORECASE).strip()
                value = value.replace(matching_nr, '', 1).strip()  # removing nr num
                nr_num = 'nr_num:*' + nr_number + '*'
                if value:
                    nr_num += ' AND'  # Get results which match nr_num and name
                else:
                    return nr_num, nr_number, value
            elif result := re.search(nr_num_fallback_regex, value):
                nr_number = result.group().strip()
                nr_num = 'nr_num:*' + nr_number + '* OR'

            name_copy = 'name_copy:*'
            name_copy += '* AND name_copy:*'.join(value.split())
            name_copy += '*'  # name_copy += '* AND'

            # name = f'({name_copy} name:(*"{value}"*))'
            name = f'({name_copy})'

            solr_query = parse.quote(f'{nr_num} {name}'.strip())

            # 'nr_num:*0285176* OR (name_copy:*0285176* AND name:(*"0285176"*))'

        return solr_query, nr_number, value

    @classmethod
    def get_results(cls, query_type, name, start=0, rows=10):
        solr_base_url = current_app.config.get('SOLR_BASE_URL', None)
        if not solr_base_url:
            current_app.logger.error('SOLR: SOLR_BASE_URL is not set')

            return None, 'Internal server error', 500

        if query_type not in SolrQueries.VALID_QUERIES:
            return None, 'Not a valid analysis type', 400

        current_app.logger.debug(
            'Solr Query - type:{qtype} - name:{name}'.format(qtype=query_type, name=parse.quote(name))
        )

        try:
            query = solr_base_url + SolrQueries.queries[query_type].format(
                start=start,
                rows=rows,
                name=cls._get_parsed_name(name),
                compressed_name=cls._compress_name(name),
                name_copy_clause=cls._get_name_copy_clause(name),
            )
            current_app.logger.debug('Query: ' + query)
            connection = request.urlopen(query)
        except Exception as err:
            current_app.logger.error(err, query)
            return None, 'Internal server error', 500

        try:
            solr = json.load(connection)
            results = {
                'response': {
                    'numFound': solr['response']['numFound'],
                    'start': solr['response']['start'],
                    'rows': solr['responseHeader']['params']['rows'],
                    'maxScore': solr['response']['maxScore'],
                    'name': solr['responseHeader']['params']['q'],
                },
                'names': solr['response']['docs'],
                'highlighting': solr['highlighting'] if 'highlighting' in solr.keys() else '',
            }
            return results, '', None
        except Exception as err:
            current_app.logger.error(err, query)
            return None, 'Internal server error', 500

    @classmethod
    def _get_parsed_name(cls, name):
        return parse.quote(name.lower().replace(WILD_CARD, '').replace(NO_SYNONYMS_INDICATOR, ''))

    # Compress the name by removing designations and then striping all non-alpha characters. Solr eventually converts to
    # lowercase so we'll choose that over doing everything in uppercase.
    @classmethod
    def _compress_name(cls, name):
        name = name.lower()

        # TODO: these should be loaded from somewhere.
        designations = [
            'corp.',
            'corporation',
            'inc.',
            'incorporated',
            'incorporee',
            'l.l.c.',
            'limited liability co.',
            'limited liability company',
            'limited liability partnership',
            'limited partnership',
            'limitee',
            'llc',
            'llp',
            'ltd.',
            'ltee',
            'sencrl',
            'societe a responsabilite limitee',
            'societe en nom collectif a responsabilite limitee',
            'srl',
            'ulc',
            'unlimited liability company',
            'limited',
        ]

        # Match the designation with whitespace before and either followed by whitespace or end of line.
        for designation in designations:
            name = re.sub(' ' + designation + '(\\s|$)', '', name)

        return re.sub('[^a-z]', '', name)


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
                    if word != '':
                        unsynonymed_words.append(word)
                        word = ''

                    indicator_on = False

                continue

            if indicator_on:
                word += letter

        # Handle when the last word was prefixed with the indicator.
        if indicator_on and word != '':
            unsynonymed_words.append(word)

        if len(unsynonymed_words) != 0:
            clause = NO_SYNONYMS_PREFIX + '(' + parse.quote(' '.join(unsynonymed_words)) + ')'

        return clause

    @classmethod
    def remove_stopwords_designations(cls, name):
        # TODO: these should be loaded from somewhere.
        designations = [
            'corp.',
            'corp',
            'corporation',
            'inc.',
            'inc',
            'incorporated',
            'incorporee',
            'l.l.c.',
            'llc',
            'limited partnership',
            'limited liability co.',
            'limited liability co',
            'limited liability company',
            'limited liability partnership',
            'limitee',
            'llp',
            'ltd.',
            'ltd',
            'ltee',
            'sencrl',
            'societe a responsabilite limitee',
            'societe en nom collectif a responsabilite limitee',
            'limited',
            'srl',
            'ulc',
            'unlimited liability company',
        ]

        # TODO: these should be loaded from somewhere.
        stop_words = [
            'an',
            'and',
            'are',
            'as',
            'at',
            'be',
            'but',
            'by',
            'corp',
            'if',
            'in',
            'incorporation',
            'into',
            'is',
            'it',
            'no',
            'not',
            'of',
            'on',
            'or',
            'such',
            'that',
            'the',
            'their',
            'then',
            'there',
            'these',
            'they',
            'this',
            'to',
        ]

        # remove designations if they are at the end of the name
        for designation in designations:
            index = name.upper().find(' ' + designation.upper())
            # checks if there is a designation AND if that designation is at the end of the string
            if index != -1 and (index + len(designation) + 1) is len(name):
                name = name[:index]
                break

        for stop_word in stop_words:
            name = ' ' + name + ' '
            name = name.upper().replace(' ' + stop_word.upper() + ' ', ' ').strip()

        # # handle non-ascii chars in name
        # name = ''.join([i if ord(i) < 128 else parse.quote(i) for i in name])
        name = name.upper().replace(' AND ', ' ').replace('&', ' ').replace('+', ' ')
        return name

    @classmethod
    def post_treatment(cls, docs, query_name):
        query_name = query_name.upper()
        names = []
        count = 0
        for candidate in docs:
            count += 1
            candidate_name = candidate['name'].upper()
            words = candidate_name.split()
            qwords = query_name.split()

            count = 0
            for qword in qwords:
                found = False
                for word in words:
                    if word not in designations() and qword not in designations():
                        should_keep = cls.keep_phonetic_match(word, qword)
                        if should_keep:
                            if not found:
                                count += 1
                            found = True

            if count == len(qwords):
                cls.keep_candidate(candidate, candidate_name, names)

        return names

    @classmethod
    def keep_phonetic_match(cls, word, query):
        word = replace_special_leading_sounds(word)
        query = replace_special_leading_sounds(query)

        word_has_leading_vowel = has_leading_vowel(word)
        query_has_leading_vowel = has_leading_vowel(query)

        word_first_consonant = first_consonants(word)
        query_first_consonant = first_consonants(query)

        query_first_vowels = first_vowels(query, query_has_leading_vowel)
        word_first_vowels = first_vowels(word, word_has_leading_vowel)

        if query_has_leading_vowel:
            query_sound = query_first_vowels + query_first_consonant
        else:
            query_sound = query_first_consonant + query_first_vowels

        if word_has_leading_vowel:
            word_sound = word_first_vowels + word_first_consonant
        else:
            word_sound = word_first_consonant + word_first_vowels

        if word_sound == query_sound:
            return True

        return False

    @classmethod
    def keep_candidate(cls, candidate, name, names):
        if len([doc['id'] for doc in names if doc['id'] == candidate['id']]) == 0:
            names.append(
                {
                    'name': name,
                    'id': candidate['id'],
                    'source': candidate['source'],
                    'jurisdiction': candidate.get('jurisdiction', ''),
                    'start_date': candidate.get('start_date', ''),
                }
            )
