from api import db, ma


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
    VALID_STATES = {DRAFT, INPROGRESS, CANCELLED, HOLD, APPROVED, REJECTED, CONDITIONAL}
    RELEASE_STATES = {DRAFT, CANCELLED, HOLD, APPROVED, REJECTED, CONDITIONAL}
    COMPLETED_STATE = {APPROVED, REJECTED, CONDITIONAL}

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
