import itertools
import re
import collections
from sqlalchemy import create_engine
from toolz import unique

from namex.services.name_request.auto_analyse import field_synonyms, field_special_words

POSTGRES_ADDRESS = 'localhost'
POSTGRES_PORT = '5432'
POSTGRES_USERNAME = 'postgres'
POSTGRES_PASSWORD = 'BVict31C'
POSTGRES_DBNAME = 'local-sandbox-dev'
POSTGRES_DBNAME_WC = 'namex-local-dev'

postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME,
                                                                                        password=POSTGRES_PASSWORD,
                                                                                        ipaddress=POSTGRES_ADDRESS,
                                                                                        port=POSTGRES_PORT,
                                                                                        dbname=POSTGRES_DBNAME))

postgres_wc_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME,
                                                                                           password=POSTGRES_PASSWORD,
                                                                                           ipaddress=POSTGRES_ADDRESS,
                                                                                           port=POSTGRES_PORT,
                                                                                           dbname=POSTGRES_DBNAME_WC))

cnx = create_engine(postgres_str)
cnx_wc = create_engine(postgres_wc_str)


# TODO: Fix caps and stuff...
def data_frame_to_list(df):
    df_dist = df.loc[df.word_classification == DataFrameFields.DISTINCTIVE.value]
    df_desc = df.loc[df.word_classification == DataFrameFields.DESCRIPTIVE.value]
    df_none = df.loc[df.word_classification == DataFrameFields.UNCLASSIFIED.value]

    list_dist = list(df_dist.word)
    list_desc = list(df_desc.word)
    list_none = list(df_none.word)

    return list_dist, list_desc, list_none


def clean_name_words(text, stop_words, designation_any, designation_end, fr_designation_end_list, prefix_list):
    words = text.lower()
    words = ' '.join([word for x, word in enumerate(words.split(" ")) if x == 0 or word not in stop_words])
    words = remove_french(words, fr_designation_end_list)
    tokens = regex_transform(words, designation_any, designation_end, prefix_list)
    tokens = tokens.split()

    return [x.lower() for x in tokens if x]


def regex_transform(text, designation_any, designation_end, prefix_list):
    designation_end_regex = '((lot)+\\s+\\d+|\\d*|' + '|'.join(map(str, designation_end)) + ')'
    designation_any_regex = "(" + '|'.join(designation_any) + ")"
    prefixes = '|'.join(prefix_list)

    exceptions_ws = []
    for word in re.sub(r'[^a-zA-Z0-9 -\']+', ' ', text, 0, re.IGNORECASE).split():
        if get_substitution_list(word):
            exceptions_ws.extend(word)

    if not exceptions_ws:
        exceptions_ws.extend(['null'])

    exception_ws_rx = '|'.join(map(re.escape, exceptions_ws))
    ws_generic_rx = r'(?<=\d)(?=[^\d\s])|(?<=[^\d\s])(?=\d)'
    ws_rx = re.compile(rf'({exception_ws_rx})|{ws_generic_rx}', re.I)

    text = re.sub(r'\s+',
                  ' ',
                  re.sub(
                      r'^(?:\d+(?:ST|[RN]D|TH)?\s+)+(?=[^\d]+$)(?!.*?(?:HOLDINGS$|BC$|VENTURES$))|(?<=\b[A-Za-z]\b) +(?=[a-zA-Z]\b)',
                      '',
                      re.sub(r'(?<=[A-Za-z]\b )([ 0-9]*(ST|[RN]D|TH)?\b)',
                             '',
                             re.sub(r'(?<=\b[A-Za-z]\b) +(?=[a-zA-Z]\b)|^\s+|\s+$',
                                    '',
                                    re.sub(r'[&/-]',
                                           ' ',
                                           ws_rx.sub(lambda x: x.group(1) or " ",
                                                     re.sub(r'\b(\d+(ST|[RN]D|TH))(\w+)\b',
                                                            r'\1 \3',
                                                            re.sub(r'\b(\w{2,})(\b\W+\b\1\b)*',
                                                                   r'\1',
                                                                   re.sub(
                                                                       r'(?<=[a-zA-Z])\'[Ss]|\(?No.?\s*\d+\)?|\(?lot.?\s*\d+[-]?\d*\)?|[^a-zA-Z0-9 &/-]+',
                                                                       ' ',
                                                                       re.sub(
                                                                           r'\.COM|(?<=\d),(?=\d)|(?<=[A-Za-z])+[\/&-](?=[A-Za-z]\b)|\b' + designation_any_regex + '\\b|\\s' + designation_end_regex + '(?=(\\s' + designation_end_regex + ')*$)',
                                                                           '',
                                                                           text,
                                                                           0,
                                                                           re.IGNORECASE),
                                                                       0,
                                                                       re.IGNORECASE),
                                                                   0,
                                                                   re.IGNORECASE),
                                                            0,
                                                            re.IGNORECASE),
                                                     ),
                                           0,
                                           re.IGNORECASE),
                                    0,
                                    re.IGNORECASE),
                             0,
                             re.IGNORECASE),
                      0,
                      re.IGNORECASE),
                  0,
                  re.IGNORECASE)
    return text


def get_list_of_lists(df, field):
    subs_list = []
    subs_list = df[field].str.split(',').tolist()
    subs_list = [item for sublist in subs_list for item in sublist]
    subs_list = [x.strip() for x in subs_list]

    return subs_list


def is_substitution_word(word):
    df = pd.read_sql_query(
        'SELECT s.synonyms_text FROM synonym s where lower(s.category) LIKE ' + "'" + '%% ' + "sub'" + 'and ' + \
        's.synonyms_text ~ ' + "'" + '\\y' + word.lower() + '\\y' + "'", cnx)
    if not df.empty:
        return True
    return False


def get_substitution_list(word):
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) LIKE ' + "'" + '%% ' + "sub'" + ' AND ' + \
            's.synonyms_text ~ ' + "'" + '\\y' + word.lower() + '\\y' + "';"
    df = pd.read_sql_query(query, cnx)
    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_synonym_list(word):
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '(?!(sub|stop)$)' + "'" + ' AND ' + \
            's.synonyms_text ~ ' + "'" + '\\y' + word.lower() + '\\y' + "';"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_stop_word_list():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^stop[_ -]+word[s]?' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_prefix_list():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^prefix(es)?' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_en_designation_any_list():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '(english[_ -]+)?designation[s]?[_-]any' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_en_designation_end_list():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + 'english[_ -]+designation[s]?[_-]+end' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_fr_designation_end_list():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '(?=french[/_ -]+designation[s]?[/_-]+end)' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_stand_alone_list():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '(?=stand[/_ -]?alone)' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_words_to_avoid():
    query = 'SELECT rc_words FROM virtual_word_condition WHERE rc_allow_use = false;'
    df = pd.read_sql_query(query, cnx_wc)

    if not df.empty:
        words_to_avoid_list = get_list_of_lists(df, field_special_words)
        return words_to_avoid_list
    return None


def get_words_requiring_consent():
    query = 'SELECT rc_words FROM virtual_word_condition WHERE rc_allow_use = true and rc_consent_required = true'

    df = pd.read_sql_query(query, cnx_wc)

    if not df.empty:
        return get_list_of_lists(df, field_special_words)

    return None


def get_classification(word):
    query = 'SELECT s.word_classification FROM word_classification s WHERE lower(s.word)=' + "'" + word.lower() + "'"
    cf = pd.read_sql_query(query, cnx_wc)

    if not cf.empty and len(cf) == 1:
        return cf['word_classification'].to_string(index=False).lower()

    return 'none'


def build_query_distinctive(dist_all_permutations):
    query = "select n.name " + \
            "from requests r, names n " + \
            "where r.id = n.nr_id and " + \
            "r.state_cd IN ('APPROVED','CONDITIONAL') and " + \
            "r.request_type_cd IN ('PA','CR','CP','FI','SO', 'UL','CUL','CCR','CFI','CCP','CSO','CCC','CC') and " + \
            "n.state IN ('APPROVED','CONDITION') and " + \
            "lower(n.name) similar to " + "'"
    permutations = "|".join("%s %s" % tup for tup in dist_all_permutations)
    query += "(" + permutations + ")%%" + "'"

    return query


def build_query_descriptive(desc_substitution_list, query):
    query += " and lower(n.name) similar to "
    substitutions = ' ?| '.join(map(str, desc_substitution_list))
    query += "'" + "%%( " + substitutions + " ?)%%" + "'"

    return query


'''
def remove_french(text, fr_designation_end_list):
    compound = re.findall(r'[^/]+(?://[^/]*)*', text)
    if len(compound) == 2:
        fr_list_text = [x.lower() for x in compound[1].split(" ") if x]
        if any(item in fr_designation_end_list for item in fr_list_text):
            compound.pop()
            text = ' '.join(map(str, compound))
    return text
'''

'''
Previous behaviour: The section after slash considered french designations to imply the section was in French.
Current behaviour: The section after slash is not longer considering french designation.
Rules:  1) Before and after slash has to be at least two words to removed string after slash.
           Eg.
           ABC ENGINEERING/CENTRAL CARE  --> ABC ENGINEERING
        2) In the case just having a word at the beginning then the string is kept with no changes.
           Eg.
           RE/MAX WALNUT DEVELOPMENT  --> RE/MAX WALNUT DEVELOPMENT
        3) In the case just having a word at the end, this is kept removing the slash.
           Eg.
           ABC ENGINEERING 7/24 --> ABC ENGINEERING 7 24
'''


def remove_french(text):
    text = re.sub(r'(^\w+(?:[^\w\n]+\w+)+[^\w\n]*)/(\w+(?:[^\w\n]+\w+)+[^\w\n]*$)?',
                  r'\1 ',
                  text,
                  0,
                  re.IGNORECASE)
    return " ".join(text.split())


def remove_stop_words(original_name, stop_words):
    stop_words_rgx = '|'.join(stop_words)
    regex = re.compile(r'\b({})\b'.format(stop_words_rgx))
    found_stop_words = regex.findall(original_name.lower())

    for word in found_stop_words:
        original_name = original_name.replace(word, "")

    return re.sub(' +', ' ', original_name)


def list_distinctive_descriptive_same(name_list):
    queue = collections.deque(name_list)
    dist_list = []
    desc_list = []

    while 1 < len(queue):
        queue.pop()
        dist_list.append(list(queue))
    dist_list.reverse()

    for dist in dist_list:
        desc_list.append([i for i in name_list if i not in dist])

    return dist_list, desc_list


def validate_distinctive_descriptive_lists(list_name, list_dist, list_desc):
    current_category = None
    list_dist_tmp = []
    list_desc_tmp = []
    list_incorrect_classification = []
    for idx, token_name, has_more in lookahead(list_name):
        if idx == 0:
            current_category = None
        if ((token_name in list_dist and token_name in list_desc) or (
                token_name not in list_dist and token_name not in list_desc)) and has_more and (
                current_category is None):
            list_dist_tmp.extend([token_name])
            current_category = DataFrameFields.DISTINCTIVE.value
        elif ((token_name in list_dist and token_name in list_desc) or (
                token_name not in list_dist and token_name not in list_desc)) and has_more and (
                current_category == DataFrameFields.DISTINCTIVE.value):
            list_dist_tmp.extend([token_name])
            list_desc_tmp.extend([token_name])
            current_category = DataFrameFields.DISTINCTIVE.value
        elif ((token_name in list_dist and token_name in list_desc) or (
                token_name not in list_dist and token_name not in list_desc)) and has_more and (
                current_category is None or current_category == DataFrameFields.DESCRIPTIVE.value):
            list_desc_tmp.extend([token_name])
            current_category = DataFrameFields.DESCRIPTIVE.value
        elif token_name in list_dist and token_name not in list_desc and (
                current_category is None or current_category == DataFrameFields.DISTINCTIVE.value) and has_more:
            current_category = DataFrameFields.DISTINCTIVE.value
            list_dist_tmp.extend([token_name])
        elif token_name in list_desc and (
                current_category == DataFrameFields.DISTINCTIVE.value or current_category == DataFrameFields.DESCRIPTIVE.value):
            current_category = DataFrameFields.DESCRIPTIVE.value
            list_desc_tmp.extend([token_name])
        else:
            list_incorrect_classification.append({token_name: idx})
            # break

    return list_dist_tmp, list_desc_tmp, list_incorrect_classification


def list_distinctive_descriptive(name_list, dist_list, desc_list):
    queue_dist = collections.deque(dist_list)

    if dist_list == name_list:
        queue_dist.pop()

    dist_list_tmp, dist_list_all, desc_list_tmp, desc_list_all = [], [], [], []

    dist_list_tmp.append(list(queue_dist))

    while len(queue_dist) > 1:
        queue_dist.pop()
        dist_list_tmp.append(list(queue_dist))

    dist_list_tmp.reverse()

    for dist in dist_list_tmp:
        desc_list_tmp.append([i for i in name_list if i not in dist and i in desc_list])

    # Validate generation of list of lists of distinctives and descriptives with the correct combinations:
    for idx, element in enumerate(dist_list_tmp):
        if (dist_list_tmp[idx] + desc_list_tmp[idx]) == name_list:
            dist_list_all.append(dist_list_tmp[idx])
            desc_list_all.append(desc_list_tmp[idx])

    return dist_list_all, desc_list_all


def lookahead(iterable):
    """Pass through all values from the given iterable, augmented by the
    information if there are more values to come after the current one
    (True), or if it is the last value (False).
    """
    # Get an iterator and pull the first value.
    it = iter(iterable)
    last = next(it)
    # Run the iterator to exhaustion (starting from the second value).
    idx = 0
    for idx, val in enumerate(it):
        # Report the *previous* value (more to come).
        yield idx, last, True
        last = val
    # Report the last value.
    yield idx + 1, last, False
