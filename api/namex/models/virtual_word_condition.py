"""
Word classification classifies all words in a name approved by an examiner to be used for auto-approval
"""

from . import db, ma

import pandas as pd
from sqlalchemy import Column
from sqlalchemy import and_

from namex.services.name_request.auto_analyse import DataFrameFields
from namex.services.name_request.auto_analyse.name_analysis_utils import get_dataframe_list, get_flat_list

# TODO: Remove deprecated duplicate from admin_tables.py
from ..criteria.virtual_word_condition.query_criteria import VirtualWordConditionCriteria


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
    def find_by_criteria(cls, criteria=None):
        VirtualWordConditionCriteria.is_valid_criteria(criteria)

        query = cls.query.with_entities(*criteria.fields).filter(and_(*criteria.filters))

        results = query.all()
        cls.close_session()
        # print(query.statement)
        return results

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_to_session(self):
        db.session.add(self)

    @classmethod
    def close_session(cls):
        db.session.close()


class VirtualWordConditionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = VirtualWordCondition
