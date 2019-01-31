import json
import string
from typing import List

from flask import current_app
from urllib import request, parse
from urllib.error import HTTPError
import re
from namex.analytics.phonetic import first_vowels, designations, first_consonants, has_leading_vowel, replace_special_leading_sounds


# Use this character in the search strings to indicate that the word should not by synonymized.
NO_SYNONYMS_INDICATOR = '@'

WILD_CARD = "*"

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
    VALID_QUERIES = [CONFLICTS, HISTORY, TRADEMARKS]

    #
    # Prototype:
    #     /solr/<core name>/select? ... &q={name} ... &wt=json&start={start}&rows={rows}&fl=source,id,name,score
    #
    queries = {
        PROX_SYN_CONFLICTS:
            '/solr/possible.conflicts/select?'
            'hl.fl=name'
            '&hl.simple.post=%3C/b%3E'
            '&hl.simple.pre=%3Cb%3E'
            '&hl=on'
            '&indent=on'
            '&q=name:{start_str}'
            '&wt=json'
            '&start={start}&rows={rows}'
            '&fl=source,id,name,score'
            '&sort=score%20desc,txt_starts_with%20asc'
            '{synonyms_clause}',
        OLD_SYN_CONFLICTS:
            '/solr/possible.conflicts/select?'
            'hl.fl=name'
            '&hl.simple.post=%3C/b%3E'
            '&hl.simple.pre=%3Cb%3E'
            '&hl=on'
            '&indent=on'
            '&q=txt_starts_with:{start_str}'
            '&wt=json'
            '&start={start}&rows={rows}'
            '&fl=source,id,name,score'
            '&sort=score%20desc,txt_starts_with%20asc'
            '{synonyms_clause}{name_copy_clause}',
        COBRS_PHONETIC_CONFLICTS:
            '/solr/possible.conflicts/select?'
            '&q=cobrs_phonetic:{start_str}'
            '&wt=json'
            '&start={start}&rows={rows}'
            '&sort=score%20desc,txt_starts_with%20asc'
            '&fq=-{exact_name}'
            '{synonyms_clause}',
        PHONETIC_CONFLICTS:
            '/solr/possible.conflicts/select?'
            '&q=dblmetaphone_name:{start_str}'
            '&wt=json'
            '&start={start}&rows={rows}'
            '&sort=score%20desc,txt_starts_with%20asc'
            '&fq=-{exact_name}'
            '{synonyms_clause}',
        CONFLICTS:
            '/solr/possible.conflicts/select?'
            'defType=edismax'
            '&hl.fl=name'
            '&hl.simple.post=%3C/b%3E'
            '&hl.simple.pre=%3Cb%3E'
            '&hl=on'
            '&indent=on'
            '&q={compressed_name}%20OR%20{name}'
            '&qf=name_compressed^6%20name_with_synonyms'
            '&wt=json'
            '&start={start}&rows={rows}'
            '&fl=source,id,name,score'
            '&sort=score%20desc'
            '{synonyms_clause}{name_copy_clause}',
        HISTORY:
            '/solr/names/select?sow=false&df=name_exact_match&wt=json&&rows={rows}&q={name}'
            '&fl=nr_num,name,score,submit_count,name_state_type_cd',
        TRADEMARKS:
            '/solr/trademarks/select?'
            'defType=edismax'
            '&hl.fl=name'
            '&hl.simple.post=%3C/b%3E&hl.simple.pre=%3Cb%3E'
            '&hl=on'
            '&indent=on'
            '&q={compressed_name}%20OR%20{name}'
            '&qf=name_compressed^6%20name_with_synonyms'
            '&wt=json'
            '&start={start}&rows={rows}'
            '&fl=application_number,name,status,description,score'
            '&bq=status:%22Registration%20published%22^5.0'
            '&sort=score%20desc{synonyms_clause}{name_copy_clause}'
    }

    @classmethod
    def get_conflict_results(cls, name, bucket, start=0, rows=100):
        solr_base_url = current_app.config.get('SOLR_BASE_URL', None)
        if not solr_base_url:
            current_app.logger.error('SOLR: SOLR_BASE_URL is not set')

            return None, 'Internal server error', 500

        # handle non-ascii chars in name
        name = ''.join([i if ord(i) < 128 else parse.quote(i) for i in name])
        name = cls.remove_stopwords_designations(name)

        if name.find('*') != -1:
            list_name_split = name.split()
        else:
            list_name_split,name = cls.combine_multi_word_synonyms(name, solr_base_url)
            list_name_split = [x.upper() for x in list_name_split]

        prox_search_strs,old_alg_search_strs,phon_search_strs = cls.build_solr_search_strs(name, list_name_split)

        synonyms_for_word = cls.get_synonyms_for_words(list_name_split)
        if bucket == 'synonym':
            connections = cls.get_synonym_results(solr_base_url, name, prox_search_strs, old_alg_search_strs, start, rows)

        elif bucket == 'cobrs_phonetic':
            connections = cls.get_cobrs_phonetic_results(solr_base_url, prox_search_strs, start, rows)

        # bucket == 'phonetic'
        else:
            connections = cls.get_phonetic_results(solr_base_url, name, phon_search_strs)

        try:
            solr = {'response':{'numFound': 0,
                                'start': start,
                                'rows': rows,
                                'maxScore': 0.0,
                                'docs': []},
                    'highlighting': []}

            seen_names = []
            passed_names = []
            previous_stack_title = ''
            stemmed_words = cls.word_pre_processing(list_name_split, 'stems', solr_base_url)['stems']
            stem_count = len(stemmed_words) * 2 + 1
            count = -1
            for connection in connections:
                seen_ordered_names = seen_names.copy()

                result = connection[0]
                solr['response']['numFound'] += result['response']['numFound']
                result_name = parse.unquote(connection[1])
                if previous_stack_title.replace(' ','') != result_name.replace(' ',''):
                    solr['response']['docs'].append({'name_info': {'name':result_name}, 'stems': stemmed_words[:int(stem_count/2)]})
                    stem_count -= 1
                    previous_stack_title = result_name

                if len(result['response']['docs']) > 0:
                    ordered_names = []
                    missed_names = []
                    # if there is a bracket in the stack title then there is a 'synonyms:(...)' clause
                    if 'synonyms:(' in result_name:
                        synonyms = result_name[result_name.find('(') + 1:result_name.find(')')]
                        synonyms = [x.strip() for x in synonyms.split(',')]
                        for synonym in synonyms:
                            if synonym.upper() in synonyms_for_word:
                                processed_synonyms_dict = cls.word_pre_processing(synonyms_for_word[synonym.upper()],
                                                                                  'synonyms',
                                                                                  solr_base_url
                                                                                  )
                                for word in processed_synonyms_dict:
                                    for item in result['response']['docs']:
                                        if item['name'] not in seen_ordered_names and item['name'] not in missed_names:
                                            missed_names.append(item['name'])
                                        if item['name'] not in seen_ordered_names:
                                            processed_name = cls.name_pre_processing(item['name']).upper()
                                            if ' ' + processed_synonyms_dict[word].upper() in ' ' + processed_name.upper():
                                                seen_ordered_names.append(item['name'])
                                                ordered_names.append({'name_info':item, 'stems': [processed_synonyms_dict[word].upper()]})
                                                missed_names.remove(item['name'])
                                            elif ' ' + word.upper() in ' ' + processed_name.upper():
                                                seen_ordered_names.append(item['name'])
                                                ordered_names.append({'name_info': item, 'stems': [word.upper()]})
                                                missed_names.remove(item['name'])

                    else:
                        for item in result['response']['docs']:
                            if item['name'] not in seen_ordered_names:
                                ordered_names.append({'name_info': item, 'stems': []})
                    for missed in missed_names:
                        current_app.logger.error('MISSED results: ', missed)
                    final_names_list = []

                    # order based on alphabetization of swapped in synonyms
                    if bucket == 'synonym':
                        processed_words_dict = cls.word_pre_processing(list_name_split, 'synonyms', solr_base_url)

                        pivot_list = []
                        for key in processed_words_dict:
                            pivot_list.insert(0,key)
                        seen_for_pivot = []
                        if '*' not in connection[1]:
                            count += 1
                        for pivot in pivot_list[count:]:
                            sorted_names = []
                            processed_synonyms_dict = cls.word_pre_processing(synonyms_for_word[pivot], 'synonyms', solr_base_url)
                            for synonym in processed_synonyms_dict:
                                for name in ordered_names:
                                    if name['name_info']['name'] in seen_for_pivot:
                                        pass
                                    else:
                                        processed_name = cls.name_pre_processing(name['name_info']['name'])

                                        if ' ' + processed_synonyms_dict[synonym].upper() in ' ' + processed_name.upper():
                                            stem = [processed_synonyms_dict[synonym].upper()]
                                            if stem not in name['stems']:
                                                sorted_names.append({'name_info': name['name_info'], 'stems': stem + name['stems'].copy()})
                                            else:
                                                sorted_names.append({'name_info': name['name_info'], 'stems': name['stems']})

                                            seen_for_pivot.append(name['name_info']['name'])
                                            if name['name_info']['name'] in passed_names:
                                                passed_names.remove(name['name_info']['name'])

                                        elif ' ' + synonym in ' ' + processed_name.upper():
                                            stem = [synonym.upper()]
                                            if stem not in name['stems']:
                                                sorted_names.append({'name_info': name['name_info'],
                                                                     'stems': stem + name['stems'].copy()})
                                            else:
                                                sorted_names.append(
                                                    {'name_info': name['name_info'], 'stems': name['stems']})

                                            seen_for_pivot.append(name['name_info']['name'])
                                            if name['name_info']['name'] in passed_names:
                                                passed_names.remove(name['name_info']['name'])

                                        elif name['name_info']['name'] not in passed_names:
                                            passed_names.append(name['name_info']['name'])

                            no_duplicates = []
                            duplicate = False
                            for ordered in ordered_names:
                                for sorted in sorted_names:
                                    if ordered['name_info']['name'] == sorted['name_info']['name']:
                                        duplicate = True
                                if not duplicate:
                                    no_duplicates.append(ordered)

                            ordered_names = sorted_names.copy() + no_duplicates.copy()

                            for seen in seen_for_pivot:
                                if seen not in seen_ordered_names:
                                    seen_ordered_names.append(seen)

                            seen_for_pivot.clear()
                            sorted_names.clear()

                        final_names_list += ordered_names
                    else:
                        for item in ordered_names:
                            if item['name_info']['name'] not in seen_ordered_names:
                                final_names_list.append(item)
                                seen_ordered_names.append(item['name_info']['name'])

                    seen_names += seen_ordered_names.copy()
                    seen_ordered_names.clear()

                    solr['response']['docs'] += final_names_list

            results = {"response": {"numFound": solr['response']['numFound'],
                                    "maxScore": solr['response']['maxScore'],
                                    "name": result['responseHeader']['params']['q']
                                    },
                       'names': solr['response']['docs'],
                       'highlighting': solr['highlighting']}

            return results, '', None

        except Exception as err:
            current_app.logger.error(err)
            return None, 'Internal server error', 500

    @classmethod
    def get_synonym_results(cls, solr_base_url, name, prox_search_strs, old_alg_search_strs, start=0, rows=100):

        try:
            connections = []

            for prox_search_tuple, old_alg_search in zip(prox_search_strs, old_alg_search_strs):

                old_alg_search_str = old_alg_search[:-2].replace(' ', '%20') + '*'  # [:-2] takes off the last '\ '

                synonyms_clause = cls._get_synonyms_clause(prox_search_tuple[1])

                for name in prox_search_tuple[0]:
                    # handle non-ascii chars in name
                    prox_search_str = name
                    ### Proximity (name:) search query
                    query = solr_base_url + SolrQueries.queries['proxsynconflicts'].format(
                        start=start,
                        rows=rows,
                        start_str='\"' + parse.quote(prox_search_str).replace('%2A', '') + '\"~{}'.format(prox_search_tuple[2]),
                        synonyms_clause=synonyms_clause,
                    )
                    current_app.logger.debug('Query: ' + query)
                    connections.append((json.load(request.urlopen(query)),
                                        '----' + prox_search_str.replace('\\', '').replace('*','').replace('@','')
                                        + synonyms_clause.replace('&fq=name_with_', ' ').replace('%20', ', ')
                                        + ' - PROXIMITY SEARCH'))

                query = solr_base_url + SolrQueries.queries['oldsynconflicts'].format(
                    start=start,
                    rows=rows,
                    start_str=parse.quote(old_alg_search_str).replace('%2A', '*').replace('%5C%2520', '\\%20'),
                    synonyms_clause=synonyms_clause,
                    name_copy_clause=cls._get_name_copy_clause(name)
                )
                current_app.logger.debug('Query: ' + query)
                connections.append((json.load(request.urlopen(query)), '----' +
                                    old_alg_search_str.replace('\\', '').replace('%20', ' ').replace('**','*') +
                                    synonyms_clause.replace('&fq=name_with_', ' ').replace('%20', ', ') +
                                    ' - EXACT WORD ORDER'))
            return connections

        except Exception as err:
            current_app.logger.error(err, query)
            return None, 'Internal server error', 500

    @classmethod
    def get_cobrs_phonetic_results(cls, solr_base_url, search_strs, start=0, rows=100):
        try:
            connections = []
            for str_tuple in search_strs:
                synonyms_clause = cls._get_synonyms_clause(str_tuple[1])
                for name in str_tuple[0]:
                    start_str = name
                    query = solr_base_url + SolrQueries.queries['cobrsphonconflicts'].format(
                        start=start,
                        rows=rows,
                        start_str='\"' + parse.quote(start_str).replace('%2A', '') + '\"~{}'.format(str_tuple[2]),
                        synonyms_clause=synonyms_clause,
                        exact_name='name_no_synonyms:\"' + start_str.replace(' ', '%20') + '\"~{}'.format(str_tuple[2]),
                    )
                    current_app.logger.debug('Query: ' + query)
                    result = json.load(request.urlopen(query))

                    connections.append((result, '----' + start_str.replace('*','').replace('@','') +
                                        synonyms_clause.replace('&fq=name_with_', ' ').replace('%20', ', ')))

            return connections

        except Exception as err:
            current_app.logger.error(err, query)
            return None, 'Internal server error', 500

    @classmethod
    def get_phonetic_results(cls, solr_base_url, name, search_strs, start=0, rows=100):
        try:
            connections = []
            for str_tuple in search_strs:
                synonyms_clause = cls._get_synonyms_clause(str_tuple[1])
                start_str = str_tuple[0]
                query = solr_base_url + SolrQueries.queries['phonconflicts'].format(
                    start=start,
                    rows=rows,
                    start_str='\"' + parse.quote(start_str).replace('%2A', '') + '\"~{}'.format(str_tuple[2]),
                    synonyms_clause=synonyms_clause,
                    exact_name='name_no_synonyms:\"' + start_str.replace(' ', '%20') + '\"~{}'.format(str_tuple[2]),
                )
                current_app.logger.debug('Query: ' + query)
                result = json.load(request.urlopen(query))

                docs = result['response']['docs']
                result['response']['docs'] = cls.post_treatment(docs, start_str)

                connections.append((result, '----' + start_str.replace('*','').replace('@','') +
                                    synonyms_clause.replace('&fq=name_with_', ' ').replace('%20', ', ')))

            return connections

        except Exception as err:
            current_app.logger.error(err, query)
            return None, 'Internal server error', 500

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

        try:
            query = solr_base_url + SolrQueries.queries[query_type].format(
                start=start,
                rows=rows,
                name=cls._get_parsed_name(name),
                compressed_name=cls._compress_name(name),
                synonyms_clause=cls._get_synonyms_clause(name),
                name_copy_clause=cls._get_name_copy_clause(name)
            )
            current_app.logger.debug('Query: ' + query)
            connection = request.urlopen(query)
        except Exception as err:
            current_app.logger.error(err, query)
            return None, 'Internal server error', 500

        try:
            solr = json.load(connection)
            results = {"response": {"numFound": solr['response']['numFound'],
                                    "start": solr['response']['start'],
                                    "rows": solr['responseHeader']['params']['rows'],
                                    "maxScore": solr['response']['maxScore'],
                                    "name": solr['responseHeader']['params']['q']
                                    },
                       'names': solr['response']['docs'],
                       'highlighting': solr['highlighting'] if 'highlighting' in solr.keys() else ''}
            return results, '', None
        except Exception as err:
            current_app.logger.error(err, query)
            return None, 'Internal server error', 500

    @classmethod
    def _get_parsed_name(cls, name):
        return parse.quote(name.lower().replace(WILD_CARD, "").replace(NO_SYNONYMS_INDICATOR, ''))

    # Compress the name by removing designations and then striping all non-alpha characters. Solr eventually converts to
    # lowercase so we'll choose that over doing everything in uppercase.
    @classmethod
    def _compress_name(cls, name):
        name = name.lower()

        # TODO: these should be loaded from somewhere.
        designations = [
            'corp.', 'corporation', 'inc.', 'incorporated', 'incorporee', 'l.l.c.', 'limited liability co.',
            'limited liability company', 'limited liability partnership', 'limited partnership','limitee', 'llc', 'llp', 'ltd.', 'ltee',
            'sencrl', 'societe a responsabilite limitee', 'societe en nom collectif a responsabilite limitee', 'srl',
            'ulc', 'unlimited liability company', 'limited',]

        # Match the designation with whitespace before and either followed by whitespace or end of line.
        for designation in designations:
            name = re.sub(' ' + designation + '(\s|$)', '', name)

        return re.sub('[^a-z]', '', name)

    @classmethod
    def _tokenize(cls, line: str, categories: List[str] = []) -> List[str]:
        """
        Builds a list of tokens based upon the categories defined
        The tokens are in the same order as the original input

        Categories are scanned left->right,
           so if you do repeat the contents in categories, the one to the left wins

        example in Doctest format <- because like, why not?!

        >>> _tokenize('a set of tokens', [' ', string.ascii_lowercase])
        ['a', ' ', 'set', ' ', 'of', ' ', 'tokens']
        >>> _tokenize('a "set of" tokens', [' ', string.ascii_lowercase])
        ['a', ' ', '"', 'set', ' ', 'of', '"', ' ', 'tokens']
        >>> _tokenize('a +"set of" tokens', [' ', '+"', ' "' string.ascii_lowercase])
        ['a', ' ', '+"', 'set', ' ', 'of', '"', ' ', 'tokens']

        :param line: str: the string to tokenize
        :param categories: List[str]: a list of strings used as categories to classify the tokens
        :return: List[str]: a list of string tokens that can be parsed left-> as order is preserved
        """
        tokens = [] # yep, lazy format
        start_token: int = 0
        idx: int
        category: List[str] = None
        for idx, char in enumerate(line):

            if category and char not in category:
                tokens.append(line[start_token:idx])
                category = None

            if not category:
                category = '\u0000'
                for cat in categories:
                    if char in cat:
                        category = cat
                        break
                start_token = idx

        if start_token <= idx:
            tokens.append(line[start_token:])
        return tokens

    @classmethod
    def _parse_for_synonym_candidates(cls, tokens: List[str]) -> List[str]:
        """
        A list of tokens is passed in.
        We parse with the following rules:
        prefix " str str str .. str " -  prefix is applied to all terms inside of the "  " tokens
        token after a '-' token is ignored unless it is between quotes, then it is ignored
        '@' mean ignore next token, if next token is ", ignore everything until the balancing " or until end of list
        :param tokens:
        :return: List[str] of tokens that are candidates as synonym tokens
        """

        candidates: List[str] = []
        previous_token: str = None
        double_quote_flag: bool = False
        skip_token_flag: bool = False

        for token in tokens:
            if token in string.whitespace:
                previous_token = token
                if not double_quote_flag:
                    skip_token_flag = False
                continue

            elif token is DOUBLE_QUOTE:
                if double_quote_flag:
                    skip_token_flag = False
                double_quote_flag = not double_quote_flag
                previous_token = token
                continue

            elif token is HYPHEN:
                if double_quote_flag:
                    previous_token = token
                    continue

                if previous_token in string.whitespace:
                    skip_token_flag = True
                    previous_token = token
                    continue

            elif token is NO_SYNONYMS_INDICATOR:
                skip_token_flag = True
                previous_token = token
                continue

            else:
                if skip_token_flag:
                    if not double_quote_flag:
                        skip_token_flag = False

                    previous_token = token
                    continue

                candidates.append(token)

            previous_token = token

        candidates.extend(cls._get_concatenated_terms(candidates))

        return candidates


    @classmethod
    def _get_concatenated_terms(cls, candidates):

        if len(candidates) < 2:
            return []

        multiples = []

        for x in range(len(candidates)):
            if x < len(candidates) - 1:
                multiples.append("".join(candidates[x:x+2]))
                if x < len(candidates) - 2:
                    multiples.append("".join(candidates[x:x+3]))

        return multiples


    # Call the synonyms API for the given token.
    @classmethod
    def _synonyms_exist(cls, token):
        solr_synonyms_api_url = current_app.config.get('SOLR_SYNONYMS_API_URL', None)
        if not solr_synonyms_api_url:
            raise Exception('SOLR: SOLR_SYNONYMS_API_URL is not set')

        # If the web service call fails, the caller will catch and then return a 500 for us.
        query = solr_synonyms_api_url + '/' + parse.quote(token)

        try:
            connection = request.urlopen(query)
        except HTTPError as http_error:
            # Expected when the token does not have synonyms.
            if http_error.code == 404:
                return False

            # Not sure what it is, pass it up.
            raise http_error

        return connection.status == 200

    # Call the synonyms API for list of synonyms matching the given token.
    @classmethod
    def _get_synonym_list(cls, token):
        solr_synonyms_api_url = current_app.config.get('SOLR_SYNONYMS_API_URL', None)
        if not solr_synonyms_api_url:
            raise Exception('SOLR: SOLR_SYNONYMS_API_URL is not set')

        # If the web service call fails, the caller will catch and then return a 500 for us.
        query = solr_synonyms_api_url + '/' + parse.quote(token)

        try:
            connection = request.urlopen(query)
        except HTTPError as http_error:
            # Expected when the token does not have synonyms.
            if http_error.code == 404:
                return []

            # Not sure what it is, pass it up.
            raise http_error

        return json.load(connection)[1][0].split(',')

    # Look up each token in name, and if it is in the synonyms then we need to search for it separately.
    @classmethod
    def _get_synonyms_clause(cls, name):
        # name = re.sub(' +', ' ', name)
        current_app.logger.debug('getting synonyms for: {}'.format(name))
        clause = ''
        synonyms = []

        if name:
            tokens = cls._tokenize(name.lower(), [string.digits,
                                                  string.whitespace,
                                                  RESERVED_CHARACTERS,
                                                  string.punctuation,
                                                  string.ascii_lowercase])
            candidates = cls._parse_for_synonym_candidates(tokens)
            for token in candidates:
                if cls._synonyms_exist(token):
                    synonyms.append(token)

        if synonyms:
            clause = SYNONYMS_PREFIX + '(' + parse.quote(' '.join(synonyms)) + ')'

        return clause

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
            'corp.', 'corp', 'corporation', 'inc.', 'inc', 'incorporated', 'incorporee', 'l.l.c.', 'llc', 'limited partnership',
            'limited liability co.', 'limited liability co','limited liability company', 'limited liability partnership', 'limitee',
            'llp', 'ltd.', 'ltd', 'ltee', 'sencrl', 'societe a responsabilite limitee',
            'societe en nom collectif a responsabilite limitee', 'limited', 'srl', 'ulc', 'unlimited liability company']

        stop_words = []
        try:
            with open('stopwords.txt') as stop_words_file:
                stop_words = []
                for line in stop_words_file.readlines():
                    if line.find('#') == -1:
                        stop_words.append(line.strip('\n').strip())
        except Exception as err:
            current_app.logger.error(err)

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
    def combine_multi_word_synonyms(cls, name, solr_base_url):

        max_len = len(name.split()) * 2
        query = solr_base_url + \
                '/solr/possible.conflicts/analysis/field?analysis.fieldvalue={name}&analysis.fieldname=name' \
                '&wt=json&indent=true'.format(name=parse.quote(name.strip()).replace('%2A', ''))

        processed_words = json.load(request.urlopen(query))

        count = 0
        for item in processed_words['analysis']['field_names']['name']['index']:
            if item == 'org.apache.lucene.analysis.synonym.SynonymGraphFilter':
                count += 1
                break
            count += 1

        name = ''
        word_count = 0
        for text in processed_words['analysis']['field_names']['name']['index'][count]:
            if word_count < max_len:
                name += text['text'] + ' '
            else:
                name += text['text']
            word_count += 1
        name = parse.unquote(name)
        processed_list = name.split()

        return processed_list,name.strip()

    @classmethod
    def build_solr_search_strs(cls, name, list_name_split):
        def replace_nth(string, deleted_substr, added_substr, n):
            nth_index = [m.start() for m in re.finditer(deleted_substr, string)][n - 1]
            before = string[:nth_index]
            after = string[nth_index:]
            after = after.replace(deleted_substr, added_substr, 1)
            newString = before + after
            return newString

        num_terms = 0
        prox_combined_terms = ''
        prox_search_strs = []
        phon_search_strs = []
        old_alg_combined_terms = ''
        old_alg_search_strs = []
        for term in list_name_split:
            num_terms += 1

            prox_combined_terms += term + ' '
            prox_compounded_words = [prox_combined_terms.strip()]

            if num_terms > 2:
                prox_compounded_words.append(prox_combined_terms.replace(' ',''))

            # concat for compound versions of combined terms
            combined_terms_list = prox_combined_terms.split()

            n = 1
            while n < len(combined_terms_list):
                compunded_name = replace_nth(prox_combined_terms, ' ', '', n)
                prox_compounded_words.append(compunded_name)
                n += 1

            prox_search_strs.insert(0, (prox_compounded_words, name[len(prox_combined_terms):], num_terms))
            phon_search_strs.insert(0, (prox_combined_terms.strip(), name[len(prox_combined_terms):], num_terms))
            old_alg_combined_terms += term + '\ '
            old_alg_search_strs.insert(0, old_alg_combined_terms)

        return prox_search_strs, old_alg_search_strs, phon_search_strs

    @classmethod
    def get_synonyms_for_words(cls, list_name_split):
        # get synonym list for each word in the name
        list_name_split = [wrd.replace('*','').upper() for wrd in list_name_split]
        synonyms_for_word = {}
        for word in list_name_split:
            synonyms_for_word[word] = [x.upper().strip() for x in cls._get_synonym_list(word)]

            if synonyms_for_word[word]:
                synonyms_for_word[word].remove(word)
                synonyms_for_word[word].sort()

                for synonym in synonyms_for_word[word]:
                    temp_list = synonyms_for_word[word].copy()
                    temp_list.remove(synonym)
                    swaps = [s for s in temp_list if synonym in s]
                    swaps.reverse()
                    for swap in swaps:
                        synonyms_for_word[word].remove(swap)
                        index = synonyms_for_word[word].index(synonym)
                        synonyms_for_word[word].insert(index, swap)

            synonyms_for_word[word].insert(0, word)

        return synonyms_for_word

    @classmethod
    def word_pre_processing(cls, list_of_words, type, solr_base_url):
        list_of_words = [w.replace('*', '') for w in list_of_words]
        words_to_process = ''
        for item in list_of_words:
            words_to_process += ' ' + item

        return_dict = {}
        if words_to_process != '':
            query = solr_base_url + \
                    '/solr/possible.conflicts/analysis/field?analysis.fieldvalue={words}&analysis.fieldname=name' \
                    '&wt=json&indent=true'.format(words=parse.quote(words_to_process.strip()))

            processed_words = json.load(request.urlopen(query))

            count = 0

            if type == 'synonyms':
                for item in processed_words['analysis']['field_names']['name']['index']:
                    if item == 'org.apache.lucene.analysis.core.FlattenGraphFilter':
                        count += 1
                        break
                    count += 1

                processed_list = []
                for text in processed_words['analysis']['field_names']['name']['index'][count]:
                    processed_list.append(text['text'])

                for original, processed in zip(list_of_words, processed_list):
                    return_dict[original] = processed

            # type == 'stems'
            else:
                for item in processed_words['analysis']['field_names']['name']['index']:
                    if item == 'org.apache.lucene.analysis.snowball.SnowballFilter':
                        count += 1
                        break
                    count += 1

                processed_list = []
                for text in processed_words['analysis']['field_names']['name']['index'][count]:
                    processed_list.append(text['text'])

                stem_in_name = False
                for item in list_of_words:
                    for processed_synonym in processed_list:
                        if processed_synonym.upper() in item.upper():
                            stem_in_name = True
                            break
                    if not stem_in_name:
                        processed_list.insert(0, item)
                return_dict['stems'] = processed_list
        return return_dict

    @classmethod
    def name_pre_processing(cls, name):
        processed_name = name.lower() \
            .replace('!', '') \
            .replace('@', '') \
            .replace('#', '') \
            .replace('%', '') \
            .replace('&', '') \
            .replace('\\', '') \
            .replace('/', '') \
            .replace('{', '') \
            .replace('}', '') \
            .replace('[', '') \
            .replace(']', '') \
            .replace('+', '') \
            .replace('-', '') \
            .replace('|', '') \
            .replace('?', '') \
            .replace('.', '') \
            .replace(',', '') \
            .replace('_', '') \
            .replace('\'', '') \
            .replace('\"', '') \
            .replace('britishcolumbia', 'bc') \
            .replace('britishcolumbias', 'bc') \
            .replace('britishcolumbian', 'bc') \
            .replace('britishcolumbians', 'bc')
        return processed_name

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
            names.append({'name': name, 'id': candidate['id'], 'source': candidate['source']})

