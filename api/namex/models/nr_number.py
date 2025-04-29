from datetime import datetime

from . import db, ma


class NRNumber(db.Model):
    __tablename__ = 'nr_number'
    # core fields
    id = db.Column(db.Integer, primary_key=True)
    nrNum = db.Column('nr_num', db.String(10), unique=True)
    lastUpdate = db.Column('last_update', db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def get_next_nr_num(cls, last_nr):
        last_nr_header = last_nr[0:4]
        last_number = last_nr[4:10]
        if last_number == '999999':
            # next_nr_header = #next letter in the alphabet starting at a specific letter
            next_number = '000000'
        else:
            next_nr_header = last_nr_header
            next_number = str((int(last_number) + 1)).zfill(6)

        next_nr_num = next_nr_header + next_number

        return next_nr_num

    def json(self):
        return {'id': self.id, 'nrNum': self.nrNum}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class NRNumberSchema(ma.SQLAlchemySchema):
    class Meta:
        model = NRNumber
