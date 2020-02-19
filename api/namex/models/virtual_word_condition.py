"""
Word classification classifies all words in a name approved by an examiner to be used for auto-approval
"""

from . import db, ma

import pandas as pd
from sqlalchemy import create_engine, Column

from namex.services.name_request.auto_analyse import DataFrameFields
from namex.services.name_request.auto_analyse.name_analysis_utils import get_dataframe_list, get_flat_list


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
        query = 'SELECT rc_words FROM virtual_word_condition WHERE rc_allow_use = false;'
        df = pd.read_sql_query(query, con=db.engine)

        if not df.empty:
            response = get_dataframe_list(df, DataFrameFields.FIELD_SPECIAL_WORDS.value)
            response = get_flat_list(response)
            return response
        return None

    @classmethod
    def get_words_requiring_consent(cls):
        query = 'SELECT rc_words FROM virtual_word_condition WHERE rc_allow_use = true and rc_consent_required = true'

        df = pd.read_sql_query(query, con=db.engine)

        if not df.empty:
            response = get_dataframe_list(df, DataFrameFields.FIELD_SPECIAL_WORDS.value)
            response = get_flat_list(response)
            return response

        return None
