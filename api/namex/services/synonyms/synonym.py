import pandas as pd
from sqlalchemy import create_engine

from namex.services.name_request.auto_analyse import field_synonyms, field_special_words
from namex.services.name_request.auto_analyse.name_analysis_utils import get_list_of_lists

POSTGRES_ADDRESS = 'localhost'
POSTGRES_PORT = '5432'
POSTGRES_USERNAME = 'postgres'
POSTGRES_PASSWORD = 'BVict31C'
POSTGRES_DBNAME = 'namex-local'
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


# TODO: These are ALL the same method, with a single different type... consolidate these functions!
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


class SynonymService:
    @classmethod
    async def get_synonyms(cls):
        return []

    @classmethod
    def get_substitutions(cls):
        return []

    @classmethod
    def get_stop_words(cls):
        return []

    @classmethod
    def get_designated_start_words(cls):
        return []

    @classmethod
    def get_designated_end_words(cls):
        return []

    @classmethod
    def get_designated_any_words(cls):
        return []