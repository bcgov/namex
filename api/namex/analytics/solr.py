import json
import re
import string
from typing import List

from flask import current_app
from urllib import request, parse
from urllib.error import HTTPError


# Use this character in the search strings to indicate that the word should not by synonymized.
NO_SYNONYMS_INDICATOR = '@'

# Constant names for useful chars used by the functions below
RESERVED_CHARACTERS = '-+@"'
DOUBLE_QUOTE = '"'
HYPHEN = '-'

# Prefix used to indicate that words are not to have synonyms.
NO_SYNONYMS_PREFIX = '&fq=name_copy:'

# Prefix used to indicate that we have synonyms.
SYNONYMS_PREFIX = '&fq=name_with_synonyms:'


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
        CONFLICTS:
            '/solr/possible.conflicts/select?defType=edismax&hl.fl=name&hl.simple.post=%3C/b%3E&hl.simple.pre=%3Cb%3E&'
            'hl=on&indent=on&q={compressed_name}%20OR%20{name}&qf=name_compressed^6%20name_with_synonyms&wt=json&'
            'start={start}&rows={rows}&fl=source,id,name,score&sort=score%20desc{synonyms_clause}{name_copy_clause}',
        HISTORY:
            '/solr/names/select?defType=edismax&hl.fl=name&hl.simple.post=%3C/b%3E&hl.simple.pre=%3Cb%3E&hl=on&'
            'indent=on&q={compressed_name}%20OR%20{name}&qf=name_compressed^6%20name_with_synonyms&wt=json&'
            'start={start}&rows={rows}&fl=nr_num,name,score,submit_count,name_state_type_cd&sort=score%20desc'
            '{synonyms_clause}{name_copy_clause}',
        TRADEMARKS:
            '/solr/trademarks/select?defType=edismax&hl.fl=name&hl.simple.post=%3C/b%3E&hl.simple.pre=%3Cb%3E&hl=on&'
            'indent=on&q={compressed_name}%20OR%20{name}&qf=name_compressed^6%20name_with_synonyms&wt=json&'
            'start={start}&rows={rows}&fl=application_number,name,status,description,score&'
            'bq=status:%22Registration%20published%22^5.0&sort=score%20desc{synonyms_clause}{name_copy_clause}'
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

        try:
            query = solr_base_url + SolrQueries.queries[query_type].format(
                start=start,
                rows=rows,
                name=parse.quote(name.replace(NO_SYNONYMS_INDICATOR, '')),
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
                       'highlighting': solr['highlighting']}
            return results, '', None
        except Exception as err:
            current_app.logger.error(err, query)
            return None, 'Internal server error', 500

    # Compress the name by removing designations and then striping all non-alpha characters. Solr eventually converts to
    # lowercase so we'll choose that over doing everything in uppercase.
    @classmethod
    def _compress_name(cls, name):
        name = name.lower()

        # TODO: these should be loaded from somewhere.
        designations = [
            'corp.', 'corporation', 'inc.', 'incorporated', 'incorporee', 'l.l.c.', 'limited', 'limited liability co.',
            'limited liability company', 'limited liability partnership', 'limitee', 'llc', 'llp', 'ltd.', 'ltee',
            'sencrl', 'societe a responsabilite limitee', 'societe en nom collectif a responsabilite limitee', 'srl',
            'ulc', 'unlimited liability company']

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

        return candidates

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

    # Look up each token in name, and if it is in the synonyms then we need to search for it separately.
    @classmethod
    def _get_synonyms_clause(cls, name):

        current_app.logger.debug('getting synonyms for: {}'.format(name))
        clause = ''
        synonyms = []

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
