import itertools
import re
import pandas as pd
import collections
from sqlalchemy import create_engine
from toolz import unique

from namex.services.name_request.auto_analyse import DataFrameFields

POSTGRES_ADDRESS = 'localhost'
POSTGRES_PORT = '5432'
POSTGRES_USERNAME = 'postgres'
POSTGRES_PASSWORD = ' '
POSTGRES_DBNAME = 'namex-auto-analyse'
# POSTGRES_DBNAME_WC = 'namex-local'

postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME,
                                                                                        password=POSTGRES_PASSWORD,
                                                                                        ipaddress=POSTGRES_ADDRESS,
                                                                                        port=POSTGRES_PORT,
                                                                                        dbname=POSTGRES_DBNAME))

# postgres_wc_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME,
#                                                                                           password=POSTGRES_PASSWORD,
#                                                                                           ipaddress=POSTGRES_ADDRESS,
#                                                                                           port=POSTGRES_PORT,
#                                                                                           dbname=POSTGRES_DBNAME_WC))

cnx = create_engine(postgres_str)


# cnx_wc = create_engine(postgres_wc_str)

# TODO: Fix caps and stuff...
def data_frame_to_list(df):
    df_dist = df.loc[df.word_classification == DataFrameFields.DISTINCTIVE.value]
    df_desc = df.loc[df.word_classification == DataFrameFields.DESCRIPTIVE.value]
    df_none = df.loc[df.word_classification == DataFrameFields.UNCLASSIFIED.value]

    list_dist = list(df_dist.word)
    list_desc = list(df_desc.word)
    list_none = list(df_none.word)

    return list_dist, list_desc, list_none


def clean_name_words(text, stop_words=[], designation_any=[], designation_end=[], fr_designation_end_list=[],
                     prefix_list=[]):
    # TODO: Warn or something if params aren't set!
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
            exceptions_ws.append(word)

    if not exceptions_ws:
        exceptions_ws.append('null')

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


def get_dataframe_list(df, field):
    # subs_list = []
    return df[field].str.split(',').tolist()

    # subs_list = [item for sublist in subs_list for item in sublist]
    # subs_list = [x.strip() for x in subs_list]

    # return dataframe_list


def get_flat_list(lst):
    subs_list = [item for sublist in lst for item in sublist]
    return [x.strip() for x in subs_list]
    # return subs_list


# TODO: This has been moved to Synonym model!
def is_substitution_word(word):
    df = pd.read_sql_query(
        'SELECT s.synonyms_text FROM synonym s where lower(s.category) LIKE ' + "'" + '%% ' + "sub'" + 'and ' + \
        's.synonyms_text ~ ' + "'" + '\\y' + word.lower() + '\\y' + "'", cnx)
    if not df.empty:
        return True
    return False


# TODO: This has been moved to Synonym model!
def get_substitution_list(word):
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) LIKE ' + "'" + '%% ' + "sub'" + ' AND ' + \
            's.synonyms_text ~ ' + "'" + '\\y' + word.lower() + '\\y' + "';"
    df = pd.read_sql_query(query, cnx)
    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
        response = get_flat_list(response)
        return response
    return None


# TODO: This has been moved to Synonym model!
def get_synonym_list(word):
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '(?!(sub|stop)$)' + "'" + ' AND ' + \
            's.synonyms_text ~ ' + "'" + '\\y' + word.lower() + '\\y' + "';"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
        response = get_flat_list(response)
        return response
    return None


# TODO: This has been moved to Synonym model!
def get_stop_word_list():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^stop[_ -]+word[s]?' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
        response = get_flat_list(response)
        return response
    return None


# TODO: This has been moved to Synonym model!
def get_prefix_list():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^prefix(es)?' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
        response = get_flat_list(response)
        return response
    return None


# TODO: This has been moved to Synonym model!
def get_en_designation_any_all_list():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^(english[_ -]+)?designation[s]?[_-]any' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
        response = get_flat_list(response)
        return response
    return None


# TODO: This has been moved to Synonym model!
def get_en_designation_end_all_list():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^english[_ -]+designation[s]?[_-]+end' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
        response = get_flat_list(response)
        return response
    return None


def get_designation_by_entity_type(entity_type):
    query = 'SELECT s.category, s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^' + entity_type.lower() + '.*(english[_ -]+)+designation[s]?[_-]' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        designation_value_list = {
            re.sub(r'.*(any).*|.*(end).*', r'\1\2', x[0], 0, re.IGNORECASE): ''.join(x[1:]).split(",") for x in
            df.itertuples(index=False)}
        return designation_value_list

    return None


def get_designation_end_in_name(name):
    en_designation_end_all_list = get_en_designation_end_all_list()
    designation_end_rgx = '(' + '|'.join(map(str, en_designation_end_all_list)) + ')'
    designation_end_regex = r'' + designation_end_rgx + '(?=(\s' + designation_end_rgx + ')*$)'

    # Returns list of tuples
    found_designation_end = re.findall(designation_end_regex, name.lower())

    # Getting list of lists where the first list contains designations of type "anywhere" and the second list contains designations of type "end".
    # [['association],['limited partnership']
    designation_end_list = [list(elem) for elem in found_designation_end]
    if any(isinstance(el, list) for el in designation_end_list):
        designation_end_list = get_flat_list(designation_end_list)
    designation_end_list = list(filter(None, designation_end_list))
    designation_end_list = list(dict.fromkeys(designation_end_list))

    return designation_end_list


def get_designation_any_in_name(name):
    en_designation_any_all_list = get_en_designation_any_all_list()
    designation_any_rgx = '(' + '|'.join(map(str, en_designation_any_all_list)) + ')'
    designation_any_regex = r'\b' + designation_any_rgx + '(?=\s)'

    # Returns list of tuples
    found_designation_any = re.findall(designation_any_regex, name.lower())

    return found_designation_any


def get_wrong_place_any_designations(name):
    en_designation_any_all_list = get_en_designation_any_all_list()

    designation_end_rgx = '(' + '|'.join(map(str, en_designation_any_all_list)) + ')'
    designation_end_regex = r'' + designation_end_rgx + '(?=(\s' + designation_end_rgx + ')*$)'

    # Returns list of tuples
    found_designation_end = re.findall(designation_end_regex, name.lower())

    # Getting list of lists where the first list contains designations of type "anywhere" and the second list contains designations of type "end".
    # [['association],['limited partnership']
    wrong_designation_end_list = [list(elem) for elem in found_designation_end]
    if any(isinstance(el, list) for el in wrong_designation_end_list):
        wrong_designation_end_list = get_flat_list(wrong_designation_end_list)
    wrong_designation_end_list = list(filter(None, wrong_designation_end_list))
    wrong_designation_end_list = list(dict.fromkeys(wrong_designation_end_list))

    return wrong_designation_end_list


def get_wrong_place_end_designations(name):
    en_designation_end_all_list = get_en_designation_end_all_list()
    designation_any_rgx = '(' + '|'.join(map(str, en_designation_end_all_list)) + ')'
    designation_any_regex = r'\b' + designation_any_rgx + '(?=\s)'

    # Returns list of tuples
    wrong_designation_any_list = re.findall(designation_any_regex, name.lower())

    return wrong_designation_any_list


def get_entity_type_end_designation(entity_end_designation_dict, all_designation_any_end_list):
    entity_type_end_designation_name = list()
    for designation_end in all_designation_any_end_list:
        entity_type_end_designation_name.extend(get_entity_type_by_value(entity_end_designation_dict, designation_end))

    all_entity_types = [item for item, count in collections.Counter(entity_type_end_designation_name).items() if
                        count > 1]

    if all_entity_types:
        return all_entity_types

    return entity_type_end_designation_name


def get_entity_type_any_designation(entity_any_designation_dict, all_designation_any_end_list):
    entity_type_any_designation_name = list()

    for designation_any in all_designation_any_end_list:
        entity_type_any_designation_name.extend(
            get_entity_type_by_value(entity_any_designation_dict, designation_any))

    return entity_type_any_designation_name


# TODO: This has been moved to Synonym model!
# TODO: These are ALL the same method, with a single different type... consolidate these functions!
def get_en_RLC_entity_type_end_designation():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^rlc.*(english[_ -]+)+designation[s]?[_-]end' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
        response = get_flat_list(response)
        return response
    return None


# TODO: This has been moved to Synonym model!
# TODO: These are ALL the same method, with a single different type... consolidate these functions!
def get_en_LL_entity_type_end_designation():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^ll.*(english[_ -]+)+designation[s]?[_-]end' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
        response = get_flat_list(response)
        return response
    return None


# TODO: This has been moved to Synonym model!
# TODO: These are ALL the same method, with a single different type... consolidate these functions!
def get_en_CC_entity_type_end_designation():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^cc.*(english[_ -]+)+designation[s]?[_-]end' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
        response = get_flat_list(response)
        return response
    return None


# TODO: This has been moved to Synonym model!
# TODO: These are ALL the same method, with a single different type... consolidate these functions!
def get_en_UL_entity_type_end_designation():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^ul.*(english[_ -]+)+designation[s]?[_-]end' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
        response = get_flat_list(response)
        return response
    return None


# TODO: These are ALL the same method, with a single different type... consolidate these functions!
def get_en_BC_entity_type_end_designation():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^bc.*(english[_ -]+)+designation[s]?[_-]end' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
        response = get_flat_list(response)
        return response
    return None


# TODO: This has been moved to Synonym model!
# TODO: These are ALL the same method, with a single different type... consolidate these functions!
def get_en_CR_entity_type_end_designation():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^cr.*(english[_ -]+)+designation[s]?[_-]end' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
        response = get_flat_list(response)
        return response
    return None


# TODO: This has been moved to Synonym model!
# TODO: These are ALL the same method, with a single different type... consolidate these functions!
def get_en_CP_entity_type_any_designation():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^cp.*(english[_ -]+)+designation[s]?[_-]any' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
        response = get_flat_list(response)
        return response
    return None


# TODO: This has been moved to Synonym model!
# TODO: These are ALL the same method, with a single different type... consolidate these functions!
def get_en_XCP_entity_type_any_designation():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^xcp.*(english[_ -]+)+designation[s]?[_-]any' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
        response = get_flat_list(response)
        return response
    return None


# TODO: This has been moved to Synonym model!
# TODO: These are ALL the same method, with a single different type... consolidate these functions!
def get_en_CC_entity_type_any_designation():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^cc.*(english[_ -]+)+designation[s]?[_-]any' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
        response = get_flat_list(response)
        return response
    return None


def get_entity_type_by_value(entity_type_dicts, designation):
    entity_list = list()
    entity__designation_end_list = entity_type_dicts.items()
    print(entity__designation_end_list)
    for entity_designation in entity__designation_end_list:
        if any(designation in value for value in entity_designation[1]):
            entity_list.append(entity_designation[0])
    return entity_list


# TODO: This has been moved to Synonym model!
# TODO: These are ALL the same method, with a single different type... consolidate these functions!
def get_fr_designation_end_list():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '(?=french[/_ -]+designation[s]?[/_-]+end)' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
        response = get_flat_list(response)
        return response
    return None


# TODO: This has been moved to Synonym model!
# TODO: These are ALL the same method, with a single different type... consolidate these functions!
def get_stand_alone_list():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '(?=stand[/_ -]?alone)' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
        response = get_flat_list(response)
        return response
    return None


# TODO: This has been moved to VirtualWordCondition model!
def get_words_to_avoid():
    query = 'SELECT rc_words FROM virtual_word_condition WHERE rc_allow_use = false;'
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SPECIAL_WORDS.value)
        response = get_flat_list(response)
        return response
    return None


# TODO: This has been moved to VirtualWordCondition model!
def get_words_requiring_consent():
    query = 'SELECT rc_words FROM virtual_word_condition WHERE rc_allow_use = true and rc_consent_required = true'

    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SPECIAL_WORDS.value)
        response = get_flat_list(response)
        return response

    return None


# TODO: This has been moved to WordClassification model!
def get_classification(word):
    query = 'SELECT s.word_classification FROM word_classification s WHERE lower(s.word)=' + "'" + word.lower() + "'"
    cf = pd.read_sql_query(query, cnx)

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


def words_distinctive_descriptive(name_list):
    queue = collections.deque(name_list)
    dist_list = []
    desc_list = []

    while 1 < len(queue):
        queue.pop()
        dist_list.append(list(queue))
    dist_list.reverse()

    for dist in dist_list:
        desc_list.append([i for i in name_list if i not in dist])

    idx = 0
    for dist, desc in zip(dist_list, desc_list):
        if not dist + desc == name_list:
            dist_list.pop(idx)
            desc_list.pop(idx)
        idx += 1

    return dist_list, desc_list
