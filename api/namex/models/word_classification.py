""""word classification classifies all words in a name approved by an exmainer to be used for auto-approval

"""
from . import db, ma
from datetime import datetime, date
from sqlalchemy.orm import backref
from sqlalchemy import or_

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
    last_update_dt =  db.Column('last_update_dt', db.DateTime(timezone=True), default=datetime.utcnow,onupdate=datetime.utcnow)

    # relationships
    approver = db.relationship('User', backref=backref('user_word_approver', uselist=False), foreign_keys=[approved_by])
    updater = db.relationship('User',backref=backref('user_word_updater', uselist=False), foreign_keys=[last_updated_by])

    def json(self):
        return {"id": self.id, "classification": self.classification, "word": self.word,
                "lastNameUsed": self. last_name_used, "lastPrepName": self.last_prep_name,
                "frequency": self.frequency,"approvedDate": self.approved_dt,
                "approvedBy": self.approved_by, "startDate": self.start_dt,
                "lastUpdatedBy": self.last_updated_by, "lastUpdatedate": self.last_update_dt}

    @classmethod
    def find_word_classification(cls, word):
        return cls.query.filter(word=word)\
                   .filter(or_(cls.end_dt is None, datetime.date(cls.end_dt) > date.today()))\
                   .filter(datetime.date(cls.start_dt) <= date.today())\
                   .filter(cls.approved_dt) <= date.today().all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_to_session(self):
        db.session.add(self)


class WordClassificationSchema(ma.ModelSchema):
    class Meta:
        model = WordClassification
