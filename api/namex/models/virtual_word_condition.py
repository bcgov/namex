""""word classification classifies all words in a name approved by an exmainer to be used for auto-approval

"""
from . import db, ma

import pandas as pd
from sqlalchemy import create_engine, Column

from namex.services.name_request.auto_analyse import DataFrameFields
from namex.services.name_request.auto_analyse.name_analysis_utils import get_dataframe_list, get_flat_list

POSTGRES_ADDRESS = 'localhost'
POSTGRES_PORT = '5432'
POSTGRES_USERNAME = 'postgres'
POSTGRES_PASSWORD = ' '
POSTGRES_DBNAME = 'namex-auto-analyse'
#POSTGRES_DBNAME_WC = 'namex-local'

postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME,
                                                                                        password=POSTGRES_PASSWORD,
                                                                                        ipaddress=POSTGRES_ADDRESS,
                                                                                        port=POSTGRES_PORT,
                                                                                        dbname=POSTGRES_DBNAME))

#postgres_wc_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME,
#                                                                                           password=POSTGRES_PASSWORD,
#                                                                                           ipaddress=POSTGRES_ADDRESS,
#                                                                                           port=POSTGRES_PORT,
#                                                                                           dbname=POSTGRES_DBNAME_WC))

cnx = create_engine(postgres_str)
#cnx_wc = create_engine(postgres_wc_str)


def get_words_to_avoid():
    query = 'SELECT rc_words FROM virtual_word_condition WHERE rc_allow_use = false;'
    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SPECIAL_WORDS.value)
        response = get_flat_list(response)
        return response
    return None


def get_words_requiring_consent():
    query = 'SELECT rc_words FROM virtual_word_condition WHERE rc_allow_use = true and rc_consent_required = true'

    df = pd.read_sql_query(query, cnx)

    if not df.empty:
        response = get_dataframe_list(df, DataFrameFields.FIELD_SPECIAL_WORDS.value)
        response = get_flat_list(response)
        return response

    return None


# TODO: Remove deprecated duplicate from admin_tables.py
class VirtualWordCondition(db.Model):
    __tablename__ = 'virtual_word_condition'

    id = Column(db.Integer, primary_key=True, autoincrement=True)

    rc_consenting_body = Column(db.VARCHAR(195))
    rc_words = Column(db.VARCHAR(1000))
    rc_condition_text = Column(db.VARCHAR(1000))
    rc_instructions = Column(db.VARCHAR(1000))
    rc_consent_required = db.Column(db.Boolean(), default=False)
    rc_allow_use = db.Column(db.Boolean(), default=True)

    @classmethod
    def get_words_to_avoid(cls):
        return get_words_to_avoid()

    @classmethod
    def get_words_requiring_consent(cls):
        return get_words_requiring_consent()
