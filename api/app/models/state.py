from . import db, ma
from marshmallow import fields

class State(db.Model):
    __tablename__ = 'states'

    cd = db.Column(db.String(20), primary_key=True)
    description = db.Column(db.String(200))

    # Request States
    DRAFT = 'DRAFT'
    INPROGRESS = 'INPROGRESS'
    CANCELLED = 'CANCELLED'
    HOLD = 'HOLD'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    CONDITIONAL = 'CONDITIONAL'
    EXPIRED = 'EXPIRED'
    VALID_STATES = [DRAFT, INPROGRESS, CANCELLED, HOLD, APPROVED, REJECTED, CONDITIONAL, EXPIRED]
    RELEASE_STATES = [DRAFT, CANCELLED, HOLD, APPROVED, REJECTED, CONDITIONAL, EXPIRED]
    COMPLETED_STATE = [APPROVED, REJECTED, CONDITIONAL]

    def as_dict(self):
        return {
            'code': self.cd,
            'description': self.description
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        pass


class StateSchema(ma.ModelSchema):
    class Meta:
        model = State
        fields = ('cd', 'description')
