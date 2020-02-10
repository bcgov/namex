import re
import pandas as pd
from sqlalchemy import create_engine

from namex.services.name_request.auto_analyse import field_synonyms, field_special_words

POSTGRES_ADDRESS = 'localhost'
POSTGRES_PORT = '5432'
POSTGRES_USERNAME = 'postgres'
POSTGRES_PASSWORD = 'BVict31C'
POSTGRES_DBNAME = 'local-sandbox-dev'
POSTGRES_DBNAME_WC = 'namex-local'

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


def data_frame_to_list(df):
    df_dist = df.loc[df.word_classification == 'distinctive']
    df_desc = df.loc[df.word_classification == 'descriptive']
    df_none = df.loc[df.word_classification == 'none']

    list_dist = list(df_dist.word)
    list_desc = list(df_desc.word)
    list_none = list(df_none.word)

    return list_dist, list_desc, list_none


def clean_name_words(text, stop_words=[], designation_any=[], designation_end=[], fr_designation_end_list=[], prefix_list=[]):
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


def get_en_designation_any_all_list():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^(english[_ -]+)?designation[s]?[_-]any' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_en_designation_end_all_list():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^english[_ -]+designation[s]?[_-]+end' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_designations_in_name(name):
    en_designation_end_all_list = get_en_designation_end_all_list()
    en_designation_any_all_list = get_en_designation_any_all_list()

    designation_end_regex = '(' + '|'.join(map(str, en_designation_end_all_list)) + ')'
    designation_any_regex = '(' + '|'.join(map(str, en_designation_any_all_list)) + ')'
    regex = r'\b' + designation_any_regex + '(?=\s|$)|' + designation_end_regex + '(?=(\s' + designation_end_regex + ')*$)'

    # Returns list of tuples
    found_designations = re.findall(regex, name.lower())

    # Getting list of lists where the first list contains designations of type "anywhere" and the second list contains designations of type "end".
    # [['association],['limited partnership']
    designation_any_end_all_lists = [list(elem) for elem in found_designations]
    designation_any_end_all_lists = ([list(filter(None, lst)) for lst in designation_any_end_all_lists])

    return designation_any_end_all_lists


def get_entity_type_end_designation(entity_end_designation_dict, all_designation_any_end_list):
    entity_type_end_designation_name = list()

    for designation_end_list in all_designation_any_end_list[1:]:
        for designation_end in designation_end_list:
            entity_type_end_designation_name.append(
                get_entity_type_by_value(entity_end_designation_dict, designation_end))

    return entity_type_end_designation_name


def get_entity_type_any_designation(entity_any_designation_dict, all_designation_any_end_list):
    entity_type_any_designation_name = list()

    for designation_any_list in all_designation_any_end_list[:1]:
        for designation_any in designation_any_list:
            entity_type_any_designation_name.append(get_entity_type_by_value(entity_any_designation_dict, designation_any))

    return entity_type_any_designation_name


def get_en_RLC_entity_type_end_designation():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^rlc.*(english[_ -]+)+designation[s]?[_-]end' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_en_LL_entity_type_end_designation():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^ll.*(english[_ -]+)+designation[s]?[_-]end' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_en_CC_entity_type_end_designation():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^cc.*(english[_ -]+)+designation[s]?[_-]end' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_en_UL_entity_type_end_designation():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^ul.*(english[_ -]+)+designation[s]?[_-]end' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_en_BC_entity_type_end_designation():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^bc.*(english[_ -]+)+designation[s]?[_-]end' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_en_CR_entity_type_end_designation():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^cr.*(english[_ -]+)+designation[s]?[_-]end' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_en_CP_entity_type_any_designation():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^cp.*(english[_ -]+)+designation[s]?[_-]any' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_en_XCP_entity_type_any_designation():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^xcp.*(english[_ -]+)+designation[s]?[_-]any' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_en_CC_entity_type_any_designation():
    query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^cc.*(english[_ -]+)+designation[s]?[_-]any' + "'"
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        return get_list_of_lists(df, field_synonyms)
    return None


def get_entity_type_by_value(entity_type_dicts, designation):
    entity_list = list()
    entity__designation_end_list = entity_type_dicts.items()
    print(entity__designation_end_list)
    for entity_designation in entity__designation_end_list:
        if any(designation in value for value in entity_designation[1]):
            entity_list.append(entity_designation[0])
    return entity_list


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


def remove_french(text, fr_designation_end_list):
    compound = re.findall(r'[^/]+(?://[^/]*)*', text)
    if len(compound) == 2:
        fr_list_text = [x.lower() for x in compound[1].split(" ") if x]
        if any(item in fr_designation_end_list for item in fr_list_text):
            compound.pop()
            text = ' '.join(map(str, compound))
    return text
