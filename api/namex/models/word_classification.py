"""
Virtual word classification classifies all words in a name approved by an examiner to be used for auto-approval
"""

from . import db, ma

import pandas as pd
from datetime import datetime, date
from sqlalchemy import func, or_
from sqlalchemy.orm import backref


import re
import pandas as pd
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import backref


class WordClassification(db.Model):
    __tablename__ = 'word_classification'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classification = db.Column('word_classification',db.String(4),default='NONE',nullable=False,index=True)
    word = db.Column('word', db.String(1024), nullable=False, index=True)
    last_name_used = db.Column('last_name_used',db.String(1024))
    last_prep_name = db.Column('last_prep_name',db.String(1024))
    frequency = db.Column('frequency', db.BIGINT)
    approved_by = db.Column('approved_by', db.Integer, db.ForeignKey('users.id'))
    approved_dt = db.Column('approved_dt', db.DateTime(timezone=True))
    start_dt = db.Column('start_dt', db.DateTime(timezone=True))
    end_dt = db.Column('end_dt', db.DateTime(timezone=True))
    last_updated_by = db.Column('last_updated_by', db.Integer, db.ForeignKey('users.id'))
    last_updated_dt = db.Column('last_updated_dt', db.DateTime(timezone=True), default=datetime.utcnow,onupdate=datetime.utcnow)

    # relationships
    approver = db.relationship('User', backref=backref('user_word_approver', uselist=False), foreign_keys=[approved_by])
    updater = db.relationship('User',backref=backref('user_word_updater', uselist=False), foreign_keys=[last_updated_by])

    def json(self):
        return {"id": self.id, "classification": self.classification, "word": self.word,
                "lastNameUsed": self. last_name_used, "lastPrepName": self.last_prep_name,
                "frequency": self.frequency,"approvedDate": self.approved_dt,
                "approvedBy": self.approved_by, "startDate": self.start_dt,
                "lastUpdatedBy": self.last_updated_by, "lastUpdatedDate": self.last_updated_dt}

    # TODO: Fix this it's not working...
    '''
    Note: we convert to lower case as word text in the DB will be in all caps.
    '''
    @classmethod
    def find_word_classification(cls, word):
        results = db.session.query(cls.word, cls.classification) \
            .filter(func.lower(cls.word) == func.lower(word)) \
            .filter(cls.end_dt == None) \
            .filter(cls.start_dt <= date.today()) \
            .filter(cls.approved_dt <= date.today()).all()
        print(word)
        print(list(map(lambda x: x.classification, results)))
        return results

    # TODO: This has been moved to WordClassification model!
    @classmethod
    def get_classification(cls, word):
        query = 'SELECT s.word_classification FROM word_classification s WHERE lower(s.word)=' + "'" + word.lower() + "'"
        cf = pd.read_sql_query(query, con=db.engine)

        if not cf.empty and len(cf) == 1:
            return cf['word_classification'].to_string(index=False).lower()

        return 'none'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_to_session(self):
        db.session.add(self)


class WordClassificationSchema(ma.ModelSchema):
    class Meta:
        model = WordClassification
