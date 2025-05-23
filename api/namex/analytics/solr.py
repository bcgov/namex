import json
import re
import string
from typing import List
from urllib import parse, request
from urllib.error import HTTPError

from flask import current_app
from google.auth.transport.requests import Request
from google.oauth2 import id_token

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

    #
    # Prototype:
    #     /solr/<core name>/select? ... &q={name} ... &wt=json&start={start}&rows={rows}&fl=source,id,name,score
    #
    queries = {
        PROX_SYN_CONFLICTS: '/solr/possible.conflicts/select?'
        'hl.fl=name'
        '&hl.simple.post=%3C/b%3E'
        '&hl.simple.pre=%3Cb%3E'
        '&hl=on'
        '&indent=on'
        '&q=name:{start_str}'
        '&wt=json'
        '&start={start}&rows={rows}'
        '&fl=source,id,name,score,start_date,jurisdiction'
        '&sort=score%20desc,txt_starts_with%20asc'
        '{synonyms_clause}'
        '{exact_phrase_clause}',
        OLD_SYN_CONFLICTS: '/solr/possible.conflicts/select?'
        'hl.fl=name'
        '&hl.simple.post=%3C/b%3E'
        '&hl.simple.pre=%3Cb%3E'
        '&hl=on'
        '&indent=on'
        '&q=txt_starts_with:{start_str}'
        '&wt=json'
        '&start={start}&rows={rows}'
        '&fl=source,id,name,score,start_date,jurisdiction'
        '&sort=score%20desc,txt_starts_with%20asc'
        '{synonyms_clause}{exact_phrase_clause}{name_copy_clause}',
        COBRS_PHONETIC_CONFLICTS: '/solr/possible.conflicts/select?'
        '&q=cobrs_phonetic:{start_str}'
        '&wt=json'
        '&start={start}&rows={rows}'
        '&fl=source,id,name,score,start_date,jurisdiction'
        '&sort=score%20desc,txt_starts_with%20asc'
        '&fq=-{exact_name}'
        '{synonyms_clause}',
        PHONETIC_CONFLICTS: '/solr/possible.conflicts/select?'
        '&q=dblmetaphone_name:{start_str}'
        '&wt=json'
        '&start={start}&rows={rows}'
        '&fl=source,id,name,score,start_date,jurisdiction'
        '&sort=score%20desc,txt_starts_with%20asc'
        '&fq=-{exact_name}'
        '{synonyms_clause}',
        CONFLICTS: '/solr/possible.conflicts/select?'
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
        '&fl=source,id,name,score,start_date,jurisdiction'
        '&sort=score%20desc'
        '{synonyms_clause}{name_copy_clause}',
        HISTORY: '/solr/names/select?sow=false&df=name_exact_match&wt=json&&rows={rows}&q={name}'
        '&fl=nr_num,name,score,submit_count,name_state_type_cd,start_date,jurisdiction'
        '&fq=name_state_type_cd:(A%20OR%20R)',
        TRADEMARKS: '/solr/trademarks/select?'
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
        '&sort=score%20desc'
        '{name_copy_clause}',
        NAME_NR_SEARCH: '/solr/names/select?'
        'indent=on'
        '&q={query}'
        '&sort=score%20desc,start_date%20desc'
        '&wt=json'
        '&start={start}&rows={rows}'
        '&fl=nr_num,score',
    }

    @classmethod
    def get_conflict_results(cls, name, bucket, exact_phrase, start=0, rows=100):
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
            list_name_split, name = cls.combine_multi_word_synonyms(name, solr_base_url)
            list_name_split = [x.upper() for x in list_name_split]
        stemmed_words = cls.word_pre_processing(list_name_split, 'stems', solr_base_url)['stems']
        stemmed_name = ''
        for stem in stemmed_words:
            stemmed_name += ' ' + stem
        stemmed_name = stemmed_name.strip().upper()

        name_tokens = {'full_words': list_name_split, 'stemmed_words': stemmed_words}
        prox_search_strs, old_alg_search_strs, phon_search_strs = cls.build_solr_search_strs(
            name, stemmed_name, name_tokens
        )

        synonyms_for_word = cls.get_synonyms_for_words(name_tokens['stemmed_words'])
        if bucket == 'synonym':
            connections = cls.get_synonym_results(
                solr_base_url, name, prox_search_strs, old_alg_search_strs, name_tokens, exact_phrase, start, rows
            )

        elif bucket == 'cobrs_phonetic':
            connections = cls.get_cobrs_phonetic_results(solr_base_url, prox_search_strs, name_tokens, start, rows)

        # bucket == 'phonetic'
        else:
            connections = cls.get_phonetic_results(solr_base_url, name, phon_search_strs, name_tokens)

        try:
            solr = {
                'response': {'numFound': 0, 'start': start, 'rows': rows, 'maxScore': 0.0, 'docs': []},
                'highlighting': [],
            }

            seen_ids = []
            # commented out here and below because it is updated but never used for anything
            # passed_names = []
            previous_stack_title = ''
            stem_count = len(stemmed_words) * 2 + 1
            count = -1

            for connection in connections:
                seen_ordered_ids = seen_ids.copy()

                result = connection[0]
                solr['response']['numFound'] += result['response']['numFound']
                result_name = parse.unquote(connection[1])
                if previous_stack_title.replace(' ', '') != result_name.replace(' ', ''):
                    stack_title_info = {
                        'name_info': {'name': result_name},
                        'stems': stemmed_words[: int(stem_count / 2)],
                    }
                    for word in list_name_split[: int(stem_count / 2)]:
                        for stem in stemmed_words[: int(stem_count / 2)]:
                            if stem in word:
                                break
                            elif stem[:-1] in word:
                                stack_title_info['stems'] += [stem[:-1]]
                    solr['response']['docs'].append(stack_title_info)
                    stem_count -= 1
                    previous_stack_title = result_name

                if len(result['response']['docs']) > 0:
                    ordered_names = []
                    missed_ids = []
                    # if there is a bracket in the stack title then there is a 'synonyms:(...)' clause
                    if 'synonyms:(' in result_name:
                        synonyms = result_name[result_name.find('(') + 1 : result_name.find(')')]
                        synonyms = [x.strip() for x in synonyms.split(',')]
                        for synonym in synonyms:
                            if synonym.upper() in synonyms_for_word:
                                for word in synonyms_for_word[synonym.upper()]:
                                    for item in result['response']['docs']:
                                        processed_name = cls.name_pre_processing(item['name']).upper()
                                        if item['id'] not in seen_ordered_ids and item['id'] not in missed_ids:
                                            missed_ids.append(item['id'])
                                        if item['id'] not in seen_ordered_ids:
                                            if word.upper() in processed_name.upper():
                                                seen_ordered_ids.append(item['id'])
                                                ordered_names.append({'name_info': item, 'stems': [word.upper()]})
                                                missed_ids.remove(item['id'])

                                            elif word.upper()[:-1] in processed_name.upper() and len(word) > 4:
                                                seen_ordered_ids.append(item['id'])
                                                ordered_names.append({'name_info': item, 'stems': [word.upper()[:-1]]})
                                                missed_ids.remove(item['id'])

                    else:
                        for item in result['response']['docs']:
                            if item['id'] not in seen_ordered_ids:
                                seen_ordered_ids.append(item['id'])
                                ordered_names.append({'name_info': item, 'stems': []})

                    if len(missed_ids) > 0:
                        current_app.logger.debug(f'In {previous_stack_title} stack UNSORTED results: {missed_ids}')
                        for missed in missed_ids.copy():
                            for item in result['response']['docs']:
                                if missed == item['id']:
                                    ordered_names.append({'name_info': item, 'stems': []})
                                    missed_ids.remove(missed)
                                    break

                        if len(missed_ids) > 0:
                            # should never get here
                            current_app.logger.error(f'In {previous_stack_title} stack MISSED results: {missed_ids}')

                    final_names_list = []

                    # order based on alphabetization of swapped in synonyms
                    if bucket == 'synonym':
                        pivot_list = []
                        for key in name_tokens['stemmed_words']:
                            pivot_list.insert(0, key.upper())
                        seen_for_pivot = []
                        if '*' not in connection[1]:
                            count += 1
                        for pivot in pivot_list[count:]:
                            sorted_names = []
                            if pivot in synonyms_for_word:
                                for synonym in synonyms_for_word[pivot]:
                                    for name in ordered_names:
                                        if name['name_info']['id'] in seen_for_pivot:
                                            pass
                                        else:
                                            processed_name = cls.name_pre_processing(name['name_info']['name'])

                                            if ' ' + synonym.upper() in ' ' + processed_name.upper():
                                                stem = [synonym.upper()]
                                                if stem[0] not in name['stems']:
                                                    sorted_names.append(
                                                        {
                                                            'name_info': name['name_info'],
                                                            'stems': stem + name['stems'].copy(),
                                                        }
                                                    )
                                                else:
                                                    sorted_names.append(
                                                        {'name_info': name['name_info'], 'stems': name['stems']}
                                                    )

                                                seen_for_pivot.append(name['name_info']['id'])
                                                # if name['name_info']['name'] in passed_names:
                                                #     passed_names.remove(name['name_info']['name'])

                                            elif (
                                                ' ' + synonym.upper()[:-1] in ' ' + processed_name.upper()
                                                and len(synonym) > 4
                                            ):
                                                stem = [synonym.upper()[:-1]]
                                                stack_title_info = solr['response']['docs'].pop()
                                                if stem[0] not in name['stems']:
                                                    sorted_names.append(
                                                        {
                                                            'name_info': name['name_info'],
                                                            'stems': stem + name['stems'].copy(),
                                                        }
                                                    )
                                                    if (
                                                        stem[0] not in stack_title_info['stems']
                                                        and synonym.upper() in stack_title_info['stems']
                                                    ):
                                                        stack_title_info['stems'] += stem
                                                else:
                                                    sorted_names.append(
                                                        {'name_info': name['name_info'], 'stems': name['stems']}
                                                    )
                                                solr['response']['docs'].append(stack_title_info)

                                                seen_for_pivot.append(name['name_info']['id'])
                                                # if name['name_info']['name'] in passed_names:
                                                #     passed_names.remove(name['name_info']['name'])

                                            # elif name['name_info']['name'] not in passed_names:
                                            #     passed_names.append(name['name_info']['name'])

                            no_duplicates = []
                            for ordered in ordered_names:
                                duplicate = False
                                for sorted in sorted_names:
                                    if ordered['name_info']['name'] == sorted['name_info']['name']:
                                        duplicate = True
                                if not duplicate:
                                    no_duplicates.append(ordered)

                            ordered_names = sorted_names.copy() + no_duplicates.copy()

                            for seen in seen_for_pivot:
                                if seen not in seen_ordered_ids:
                                    seen_ordered_ids.append(seen)

                            seen_for_pivot.clear()
                            sorted_names.clear()

                        final_names_list += ordered_names
                    else:
                        for item in ordered_names:
                            final_names_list.append(item)
                            seen_ordered_ids.append(item['name_info']['id'])

                    seen_ids += seen_ordered_ids.copy()
                    seen_ordered_ids.clear()

                    solr['response']['docs'] += final_names_list

            results = {
                'response': {
                    'numFound': solr['response']['numFound'],
                    'maxScore': solr['response']['maxScore'],
                    'name': result['responseHeader']['params']['q'],
                },
                'names': solr['response']['docs'],
                'highlighting': solr['highlighting'],
            }

            return results, '', None

        except Exception as err:
            current_app.logger.error(err)
            return None, 'Internal server error', 500

    @classmethod
    def get_synonym_results(
        cls, solr_base_url, name, prox_search_strs, old_alg_search_strs, name_tokens, exact_phrase, start=0, rows=100
    ):
        try:
            connections = []
            if name == '':
                name = '*'
                prox_search_strs.append((['*'], '', '', 1))
                old_alg_search_strs.append('*')

            for prox_search_tuple, old_alg_search in zip(prox_search_strs, old_alg_search_strs):
                old_alg_search_str = old_alg_search[:-2].replace(' ', '%20') + '*'  # [:-2] takes off the last '\ '
                synonyms_clause = (
                    cls._get_synonyms_clause(prox_search_tuple[1], prox_search_tuple[2], name_tokens)
                    if exact_phrase == ''
                    else ''
                )
                exact_phrase_clause = (
                    '&fq=contains_exact_phrase:' + '"' + parse.quote(exact_phrase).replace('%2A', '') + '"'
                    if exact_phrase != ''
                    else ''
                )

                if name.find('*') == -1:
                    for name in prox_search_tuple[0]:
                        prox_search_str = name
                        query = solr_base_url + SolrQueries.queries['proxsynconflicts'].format(
                            start=start,
                            rows=rows,
                            start_str='"'
                            + parse.quote(prox_search_str).replace('%2A', '')
                            + '"~{}'.format(prox_search_tuple[3]),
                            synonyms_clause=synonyms_clause,
                            exact_phrase_clause=exact_phrase_clause,
                        )
                        current_app.logger.debug('Query: ' + query)
                        connections.append(
                            (
                                json.load(request.urlopen(query)),
                                '----'
                                + prox_search_str.replace('\\', '').replace('*', '').replace('@', '')
                                + synonyms_clause.replace('&fq=name_with_', ' ').replace('%20', ', ')
                                + ' - PROXIMITY SEARCH',
                            )
                        )

                query = solr_base_url + SolrQueries.queries['oldsynconflicts'].format(
                    start=start,
                    rows=rows,
                    start_str=parse.quote(old_alg_search_str).replace('%2A', '*').replace('%5C%2520', '\\%20'),
                    synonyms_clause=synonyms_clause,
                    exact_phrase_clause=exact_phrase_clause,
                    name_copy_clause=cls._get_name_copy_clause(name),
                )
                current_app.logger.debug('Query: ' + query)
                connections.append(
                    (
                        json.load(request.urlopen(query)),
                        '----'
                        + old_alg_search_str.replace('\\', '').replace('%20', ' ').replace('**', '*')
                        + synonyms_clause.replace('&fq=name_with_', ' ').replace('%20', ', ')
                        + ' - EXACT WORD ORDER',
                    )
                )
            return connections

        except Exception as err:
            current_app.logger.error(err, query)
            return None, 'SOLR query error', 500

    @classmethod
    def get_cobrs_phonetic_results(cls, solr_base_url, search_strs, name_tokens, start=0, rows=100):
        try:
            if search_strs == []:
                connections = [
                    ({'response': {'numFound': 0, 'docs': []}, 'responseHeader': {'params': {'q': '*'}}}, '----*')
                ]
            else:
                connections = []
                for str_tuple in search_strs:
                    synonyms_clause = cls._get_synonyms_clause(str_tuple[1], str_tuple[2], name_tokens)
                    for name in str_tuple[0]:
                        start_str = name
                        query = solr_base_url + SolrQueries.queries['cobrsphonconflicts'].format(
                            start=start,
                            rows=rows,
                            start_str='"' + parse.quote(start_str).replace('%2A', '') + '"~{}'.format(str_tuple[3]),
                            synonyms_clause=synonyms_clause,
                            exact_name='name_no_synonyms:"'
                            + start_str.replace(' ', '%20')
                            + '"~{}'.format(str_tuple[3]),
                        )
                        current_app.logger.debug('Query: ' + query)
                        result = json.load(request.urlopen(query))
                        connections.append(
                            (
                                result,
                                '----'
                                + start_str.replace('*', '').replace('@', '')
                                + synonyms_clause.replace('&fq=name_with_', ' ').replace('%20', ', '),
                            )
                        )
            return connections

        except Exception as err:
            current_app.logger.error(err, query)
            return None, 'SOLR query error', 500

    @classmethod
    def get_phonetic_results(cls, solr_base_url, name, search_strs, name_tokens, start=0, rows=100):
        try:
            if search_strs == []:
                connections = [
                    ({'response': {'numFound': 0, 'docs': []}, 'responseHeader': {'params': {'q': '*'}}}, '----*')
                ]
            else:
                connections = []
                for str_tuple in search_strs:
                    synonyms_clause = cls._get_synonyms_clause(str_tuple[1], str_tuple[2], name_tokens)
                    start_str = str_tuple[0]
                    query = solr_base_url + SolrQueries.queries['phonconflicts'].format(
                        start=start,
                        rows=rows,
                        start_str='"' + parse.quote(start_str).replace('%2A', '') + '"~{}'.format(str_tuple[3]),
                        synonyms_clause=synonyms_clause,
                        exact_name='name_no_synonyms:"' + start_str.replace(' ', '%20') + '"~{}'.format(str_tuple[3]),
                    )
                    current_app.logger.debug('Query: ' + query)
                    result = json.load(request.urlopen(query))
                    docs = result['response']['docs']
                    result['response']['docs'] = cls.post_treatment(docs, start_str)
                    connections.append(
                        (
                            result,
                            '----'
                            + start_str.replace('*', '').replace('@', '')
                            + synonyms_clause.replace('&fq=name_with_', ' ').replace('%20', ', '),
                        )
                    )
            return connections

        except Exception as err:
            current_app.logger.error(err, query)
            return None, 'SOLR query error', 500

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

    @classmethod
    def _tokenize(cls, line: str, categories: List[str] = None) -> List[str]:
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
        tokens = []  # yep, lazy format
        if categories is None:
            categories = []
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
                multiples.append(''.join(candidates[x : x + 2]))
                if x < len(candidates) - 2:
                    multiples.append(''.join(candidates[x : x + 3]))

        return multiples

    # Call the synonyms API for the given token.

    @classmethod
    def _get_identity_token(cls, audience):
        """Get an identity token for authenticating with solr-synonyms-api."""
        try:
            token = id_token.fetch_id_token(Request(), audience)

            if not token or not isinstance(token, str):
                current_app.logger.warning('Failed to get identity token')
                return None

            return token
        except Exception:
            current_app.logger.warning('Error in getting identity token.')
            return None


    @classmethod
    def _synonyms_exist(cls, token, col):
        solr_synonyms_api_url = current_app.config.get('SOLR_SYNONYMS_API_URL', None)
        if not solr_synonyms_api_url:
            raise Exception('SOLR: SOLR_SYNONYMS_API_URL is not set')

        # Get identity token and make header
        id_token = cls._get_identity_token(solr_synonyms_api_url)

        # If the web service call fails, the caller will catch and then return a 500 for us.
        query = solr_synonyms_api_url + '/synonyms/' + col + '/' + parse.quote(token)
        current_app.logger.debug('Query: ' + query)

        try:
            if id_token is None:
                connection = request.urlopen(query)
            else:
                connection = request.urlopen(request.Request(
                    query, headers={'Authorization': f'Bearer {id_token}'}
                ))
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

        # Get identity token and make header
        id_token = cls._get_identity_token(solr_synonyms_api_url)

        # If the web service call fails, the caller will catch and then return a 500 for us.
        query = solr_synonyms_api_url + '/synonyms/' + 'stems_text' + '/' + parse.quote(token)
        current_app.logger.debug('Query: ' + query)

        try:
            if id_token is None:
                connection = request.urlopen(query)
            else:
                connection = request.urlopen(request.Request(
                    query, headers={'Authorization': f'Bearer {id_token}'}
                ))
        except HTTPError as http_error:
            # Expected when the token does not have synonyms.
            if http_error.code == 404:
                return []

            # Not sure what it is, pass it up.
            raise http_error

        results = json.load(connection)
        synonym_list = []
        # in case a token is part of multiple synonym lists
        for synonyms in results[1]:
            synonym_list += synonyms.split(',')

        return synonym_list

    # Look up each token in name, and if it is in the synonyms then we need to search for it separately.
    @classmethod
    def _get_synonyms_clause(cls, name, stemmed_name, name_tokens={'full_words': [], 'stemmed_words': []}):  # noqa: B006
        # name = re.sub(' +', ' ', name)
        current_app.logger.debug('getting synonyms for: {}'.format(name))
        clause = ''
        synonyms = []
        if name:
            tokens = cls._tokenize(
                name.lower(),
                [string.digits, string.whitespace, RESERVED_CHARACTERS, string.punctuation, string.ascii_lowercase],
            )
            candidates = cls._parse_for_synonym_candidates(tokens)
            for token in candidates:
                for full, stem in zip(name_tokens['full_words'], name_tokens['stemmed_words']):
                    if token.upper() == full.upper():
                        token = stem
                        break
                if cls._synonyms_exist(token, 'synonyms_text'):
                    synonyms.append(token.upper())

        if stemmed_name:
            tokens = cls._tokenize(
                stemmed_name.lower(),
                [string.digits, string.whitespace, RESERVED_CHARACTERS, string.punctuation, string.ascii_lowercase],
            )
            candidates = cls._parse_for_synonym_candidates(tokens)
            for token in candidates:
                if cls._synonyms_exist(token, 'stems_text') and token.upper() not in synonyms:
                    synonyms.append(token.upper())

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
    def combine_multi_word_synonyms(cls, name, solr_base_url):
        max_len = len(name.split()) * 2
        query = (
            solr_base_url
            + '/solr/possible.conflicts/analysis/field?analysis.fieldvalue={name}&analysis.fieldname=name'
            '&wt=json&indent=true'.format(name=parse.quote(name.strip()).replace('%2A', ''))
        )
        current_app.logger.debug('Query: ' + query)

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

        return processed_list, name.strip()

    @classmethod
    def build_solr_search_strs(cls, name, stemmed_name, name_tokens):
        def replace_nth(string, deleted_substr, added_substr, n):
            nth_index = [m.start() for m in re.finditer(deleted_substr, string)][n - 1]
            before = string[:nth_index]
            after = string[nth_index:]
            after = after.replace(deleted_substr, added_substr, 1)
            newString = before + after
            return newString

        num_terms = 0
        prox_combined_terms = ''
        prox_stemmed_combined_terms = ''
        prox_search_strs = []
        phon_search_strs = []
        old_alg_combined_terms = ''
        old_alg_search_strs = []
        full_words = name_tokens['full_words']
        stemmed_words = name_tokens['stemmed_words']

        for index in range(len(full_words)):
            term = full_words[index]
            try:
                stemmed_term = stemmed_words[index]
            except IndexError:
                stemmed_term = ''
            num_terms += 1

            prox_combined_terms += term + ' '
            prox_stemmed_combined_terms += stemmed_term + ' '
            prox_compounded_words = [prox_combined_terms.strip()]

            if num_terms > 2:
                prox_compounded_words.append(prox_combined_terms.replace(' ', ''))

            # concat for compound versions of combined terms
            combined_terms_list = prox_combined_terms.split()

            n = 1
            while n < len(combined_terms_list):
                compunded_name = replace_nth(prox_combined_terms, ' ', '', n)
                prox_compounded_words.append(compunded_name)
                n += 1
            prox_search_strs.insert(
                0,
                (
                    prox_compounded_words,
                    name[len(prox_combined_terms) :],
                    stemmed_name[len(prox_stemmed_combined_terms) :],
                    num_terms,
                ),
            )
            phon_search_strs.insert(
                0,
                (
                    prox_combined_terms.strip(),
                    name[len(prox_combined_terms) :],
                    stemmed_name[len(prox_stemmed_combined_terms) :],
                    num_terms,
                ),
            )
            old_alg_combined_terms += term + '\\ '
            old_alg_search_strs.insert(0, old_alg_combined_terms)

        return prox_search_strs, old_alg_search_strs, phon_search_strs

    @classmethod
    def get_synonyms_for_words(cls, list_name_split):
        # get synonym list for each word in the name
        list_name_split = [wrd.replace('*', '').upper() for wrd in list_name_split]
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

        return_dict = {'stems': []}
        if words_to_process != '':
            query = (
                solr_base_url
                + '/solr/possible.conflicts/analysis/field?analysis.fieldvalue={words}&analysis.fieldname=name'
                '&wt=json&indent=true'.format(words=parse.quote(words_to_process.strip()))
            )
            current_app.logger.debug('Query: ' + query)

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
                    processed_list.append(text['text'].upper())

                # removal_list = []
                # for item in list_of_words:
                #     stem_in_name = False
                #     for processed_synonym in processed_list:
                #         if processed_synonym.upper() in item.upper():
                #             stem_in_name = True
                #             break
                #         elif processed_synonym.upper()[:-1] in item.upper():
                #             removal_list.append(processed_synonym)
                #     if not stem_in_name:
                #         processed_list.insert(0, item)
                # for processed in processed_list:
                #     if processed in removal_list:
                #         processed_list.remove(processed)
                return_dict['stems'] = processed_list
        return return_dict

    @classmethod
    def name_pre_processing(cls, name):
        processed_name = (
            (' ' + name.lower() + ' ')
            .replace('!', '')
            .replace('@', '')
            .replace('#', '')
            .replace('%', '')
            .replace('&', '')
            .replace('\\', '')
            .replace('/', '')
            .replace('{', '')
            .replace('}', '')
            .replace('[', '')
            .replace(']', '')
            .replace(')', '')
            .replace('(', '')
            .replace('+', '')
            .replace('-', '')
            .replace('|', '')
            .replace('?', '')
            .replace('.', '')
            .replace(',', '')
            .replace('_', '')
            .replace("'n", '')
            .replace("'", '')
            .replace('"', '')
            .replace(' $ ', 'dollar')
            .replace('$', 's')
            .replace(' ¢ ', 'cent')
            .replace('¢', 'c')
            .replace('britishcolumbia', 'bc')
            .replace('britishcolumbias', 'bc')
            .replace('britishcolumbian', 'bc')
            .replace('britishcolumbians', 'bc')
            .replace('british columbia', 'bc')
            .replace('british columbias', 'bc')
            .replace('british columbian', 'bc')
            .replace('british columbians', 'bc')
        )
        return processed_name.strip()

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
