"""Name hold a name choice for a Request
"""
from . import db, ma
from marshmallow import fields
from sqlalchemy.orm import backref
from sqlalchemy import event

class Name(db.Model):
    __tablename__ = 'names'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), index=True)
    state = db.Column(db.String(15), default='NE') # NE=Not Examined; R=Rejected; A=Accepted; C=Cond. Accepted
    choice = db.Column(db.Integer)
    designation = db.Column(db.String(50), default=None)
    consumptionDate = db.Column('consumption_date', db.DateTime(timezone=True))
    corpNum = db.Column('corp_num', db.String(10), default=None)
    remoteNameId = db.Column('remote_name_id', db.BigInteger)

    # decision info
    conflict1 = db.Column(db.String(250), default='') # optional conflict name
    conflict2 = db.Column(db.String(250), default='') # optional conflict name
    conflict3 = db.Column(db.String(250), default='') # optional conflict name
    conflict1_num = db.Column(db.String(250), default='') # optional conflict name - corp or NR number
    conflict2_num = db.Column(db.String(250), default='') # optional conflict name - corp or NR number
    conflict3_num = db.Column(db.String(250), default='') # optional conflict name - corp or NR number
    decision_text = db.Column(db.String(1000), default='')

    nrId = db.Column('nr_id', db.Integer, db.ForeignKey('requests.id'), index=True)
    commentId = db.Column('comment_id', db.Integer, db.ForeignKey('comments.id'))
    # nameRequest = db.relationship('Request')

    # if a comment is added during decision, link it to the name record to be sent back to NRO
    comment = db.relationship("Comment", backref=backref("related_name", uselist=False), foreign_keys=[commentId])


    # required for name request name analysis
    _name_type_cd = db.Column('name_type_cd', db.String(10))
    _clean_name = db.Column('clean_name', db.String(1024), index=True)

    NOT_EXAMINED = 'NE'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    CONDITION = 'CONDITION'
    # needed for name request reservation before completing the nr
    RESERVED = 'RESERVED'

    #Properties added for Name Request
    @property
    def name_type_cd(self):
        """Property containing the name type which is used by name Request."""
        return self._name_type_cd

    @name_type_cd.setter
    def name_type_cd(self, value: str):
        self._name_type_cd = value

    @property
    def clean_name(self):
        """Property containing the cleaned approved name used in analysis in Name Request"""
        return self._clean_name

    @clean_name.setter
    def clean_name(self, value: str):
        self._clean_name = value

    def as_dict(self):
        return {
            "name": self.name,
            "clean_name": self.clean_name,
            "name_type_cd": self.name_type_cd,
            "designation": self.designation,
            "choice": self.choice,
            "state": self.state,
            "conflict1": self.conflict1,
            "conflict2": self.conflict2,
            "conflict3": self.conflict3,
            "conflict1_num": self.conflict1_num,
            "conflict2_num": self.conflict2_num,
            "conflict3_num": self.conflict3_num,
            "decision_text": self.decision_text,
            "consumptionDate": self.consumptionDate,
            "corpNum": self.corpNum,
            "comment": None if self.comment is None else self.comment.as_dict(),
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        # force uppercase names
        self.name = self.name.upper()

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

@event.listens_for(Name, 'before_update')
def set_analysis_name(mapper, connection, target):  # pylint: disable=unused-argument; SQLAlchemy callback signature
    """Set the cleaned_name when an examiner approves a name (any name)"""
    name = target
    #if(name.state  == 'APPROVED'):
        #TODO: Run the regex service to set the clean name



class NameSchema(ma.ModelSchema):
    class Meta:
        model = Name
        fields = ('name', 'state', 'choice', 'designation', 'conflict1', 'conflict2',
                  'conflict3', 'conflict1_num', 'conflict2_num', 'conflict3_num', 'decision_text')
    name = fields.String(
        required=True,
        error_messages={'required': {'message': 'name is a required field'}}
    )




