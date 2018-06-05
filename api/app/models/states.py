from app import db, ma
from datetime import datetime
from sqlalchemy.orm import backref
from app.models.user import User


class State(db.Model):
    __tablename__ = 'states'

    cd = db.Column(db.String(20), primary_key=True)
    description = db.Column(db.String(200))

    # Request States
    STATE_DRAFT = 'DRAFT'
    STATE_INPROGRESS ='INPROGRESS'
    STATE_CANCELLED = 'CANCELLED'
    STATE_HOLD = 'HOLD'
    STATE_APPROVED = 'APPROVED'
    STATE_REJECTED = 'REJECTED'
    STATE_CONDITIONAL = 'CONDITIONAL'
    VALID_STATES = { STATE_DRAFT, STATE_INPROGRESS, STATE_CANCELLED, STATE_HOLD, STATE_APPROVED, STATE_REJECTED, STATE_CONDITIONAL }
    RELEASE_STATES = { STATE_DRAFT, STATE_CANCELLED, STATE_HOLD, STATE_APPROVED, STATE_REJECTED, STATE_CONDITIONAL }
    COMPLETED_STATE = { STATE_APPROVED, STATE_REJECTED, STATE_CONDITIONAL }

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
