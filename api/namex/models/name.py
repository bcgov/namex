"""Name hold a name choice for a Request
"""
from . import db, ma
from marshmallow import fields

class Name(db.Model):
    __tablename__ = 'names'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024))
    state = db.Column(db.String(15), default='DRAFT') # NE=Not Examined; R=Rejected; A=Accepted; C=Cond. Accepted
    choice = db.Column(db.Integer)
    designation = db.Column(db.String(50), default='DRAFT')
    consumptionDate = db.Column('consumption_date', db.DateTime)
    remoteNameId = db.Column('remote_name_id', db.BigInteger)

    # decision info
    conflict1 = db.Column(db.String(250), default='') # optional conflict name
    conflict2 = db.Column(db.String(250), default='') # optional conflict name
    conflict3 = db.Column(db.String(250), default='') # optional conflict name
    conflict1_num = db.Column(db.String(250), default='') # optional conflict name - corp or NR number
    conflict2_num = db.Column(db.String(250), default='') # optional conflict name - corp or NR number
    conflict3_num = db.Column(db.String(250), default='') # optional conflict name - corp or NR number
    decision_text = db.Column(db.String(1000), default='')

    nrId = db.Column('nr_id', db.Integer, db.ForeignKey('requests.id'))
    # nameRequest = db.relationship('Request')

    NOT_EXAMINED = 'NE'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    CONDITION = 'CONDITION'

    def as_dict(self):
        return {
            "name": self.name,
            "choice": self.choice,
            "state": self.state,
            "consumptionDate": self.consumptionDate,
            "conflict1": self.conflict1,
            "conflict2": self.conflict2,
            "conflict3": self.conflict3,
            "conflict1_num": self.conflict1_num,
            "conflict2_num": self.conflict2_num,
            "conflict3_num": self.conflict3_num,
            "decision_text": self.decision_text,
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class NameSchema(ma.ModelSchema):
    class Meta:
        model = Name
        fields = ('name', 'state', 'choice', 'designation', 'consumptionDate', 'conflict1', 'conflict2', 'conflict3',
                  'conflict1_num', 'conflict2_num', 'conflict3_num', 'decision_text')
    name = fields.String(
        required=True,
        error_messages={'required': {'message': 'name is a required field'}}
    )
    # additional = ("name", "email", "created_at")
