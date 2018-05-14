"""Name hold a name choice for a Request
"""
from app import db


class Name(db.Model):
    __bind_key__ = None
    __tablename__ = 'names'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024))
    state = db.Column(db.String(15), default='DRAFT')
    choice = db.Column(db.Integer)
    consumptionDate = db.Column('consumption_date', db.DateTime)
    remoteNameId = db.Column('remote_name_id', db.BigInteger)

    nrId = db.Column('nr_id', db.Integer, db.ForeignKey('requests.id'))
    nameRequest = db.relationship('Request')

    def __init__(self):
        pass

    def json(self):
        return {"name": self.name, "choice": self.choice, "state": self.state, "consumptionDate": self.consumptionDate}
