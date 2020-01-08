""""word classification classifies all words in a name approved by an exmainer to be used for auto-approval

"""
from . import db, ma
from datetime import datetime
from sqlalchemy.orm import backref


class WordClassification(db.Model):
    __tablename__ = 'word_classification'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classification = db.Column('word_classification',db.String(4),default='NONE',nullable=False,index=True)
    word = db.Column('word', db.String(1024), nullable=False, index=True)
    lastNameUsed = db.Column('last_name_used',db.String(1024))
    lastPrepName = db.Column('last_prep_name',db.String(1024))
    frequency = db.Column('frequency', db.BIGINT)
    approvedBy = db.Column('approved_by', db.Integer, db.ForeignKey('users.id'))
    approvedDate = db.Column('approved_dt', db.DateTime(timezone=True), default=datetime.utcnow)
    startDate = db.Column('start_dt', db.DateTime(timezone=True), default=datetime.utcnow)
    endDate = db.Column('end_dt', db.DateTime(timezone=True), default=datetime.utcnow)
    lastUpdatedBy = db.Column('last_updated_by', db.Integer, db.ForeignKey('users.id'))
    lastUpdateDate =  db.Column('approved_dt', db.DateTime(timezone=True), default=datetime.utcnow)

    # relationships
    approver = db.relationship('User', backref=backref('user_word_approver', uselist=False), foreign_keys=[approvedBy])
    updater = db.relationship('User',backref=backref('user_word_updater', uselist=False), foreign_keys=[lastUpdatedBy])

    def json(self):
        return {"id": self.id, "classification": self.classification, "word": self.word,
                "lastNameUsed": self.lastNameUsed, "lastPrepName": self.lastPrepName,"frequency": self.frequency}

    @classmethod
    def find_word_classification(cls, word):
        return cls.query.filter(word=word).filter(cls.endDate is None).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_to_session(self):
        db.session.add(self)

    def delete_from_db(self):
        raise BusinessException()

class WordClassificationSchema(ma.ModelSchema):
        class Meta:
            model = WordClassification