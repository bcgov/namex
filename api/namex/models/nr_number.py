from . import db, ma
from marshmallow import fields
from sqlalchemy.orm import backref
from sqlalchemy import event
from datetime import datetime

class NRNumber(db.Model):
    __tablename__ = 'nr_number'
    # core fields
    id = db.Column(db.Integer, primary_key=True)
    nrNum = db.Column('nr_num', db.String(10), unique=True)
    lastUpdate = db.Column('last_update', db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def find_last_nr_num(cls):
        return cls.query(cls.nrNum).filter(cls.source == 'NAMEREQUEST').one_or_none()

    @classmethod
    def get_next_nr_num(cls,last_nr_num):
        last_nr_header = last_nr_num[0:4]
        last_number = last_nr_num[4:10]
        if(last_number == '999999'):
            #next_nr_header = #next letter in the alphabet starting at a specific letter
            next_number = '000000'
        else:
            next_nr_header = last_nr_header

            next_number = str((int(last_number) + 1)).zfill(6)

        next_nrNum = next_nr_header + next_number

        return(next_nrNum)

        def as_dict(self):
            return {
                'id': self.id,
                'nrNum': self.nrNum
            }

        def save_to_db(self):
            db.session.add(self)
            db.session.commit()

        def delete_from_db(self):
            pass

class NRNumberSchema(ma.ModelSchema):
    class Meta:
        model = NRNumber
        fields = ('id', 'nrNum')