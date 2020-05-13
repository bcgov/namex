"""
skeleton word classification model for flask admin app
"""

from . import db
from datetime import datetime


class WordClassification(db.Model):
    __tablename__ = 'word_classification'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classification = db.Column('word_classification',db.String(4),default='NONE',nullable=False,index=True)
    word = db.Column('word', db.String(1024), nullable=False, index=True)
    last_name_used = db.Column('last_name_used',db.String(1024))
    last_prep_name = db.Column('last_prep_name',db.String(1024))
    frequency = db.Column('frequency', db.BIGINT)
    approved_by = db.Column('approved_by', db.Integer)
    approved_dt = db.Column('approved_dt', db.DateTime(timezone=True))
    start_dt = db.Column('start_dt', db.DateTime(timezone=True))
    end_dt = db.Column('end_dt', db.DateTime(timezone=True))
    last_updated_by = db.Column('last_updated_by', db.Integer)
    last_updated_dt = db.Column('last_update_dt', db.DateTime(timezone=True), default=datetime.utcnow,onupdate=datetime.utcnow)


