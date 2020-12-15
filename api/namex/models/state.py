from . import db, ma


class State(db.Model):
    __tablename__ = 'states'

    cd = db.Column(db.String(20), primary_key=True)
    description = db.Column(db.String(200))

    # Request States
    DRAFT = 'DRAFT'
    INPROGRESS = 'INPROGRESS'
    CANCELLED = 'CANCELLED'
    REFUND_REQUESTED = 'REFUND_REQUESTED'
    HOLD = 'HOLD'
    RESERVED = 'RESERVED'
    COND_RESERVE = 'COND-RESERVE'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    CONDITIONAL = 'CONDITIONAL'
    EXPIRED = 'EXPIRED'
    COMPLETED = 'COMPLETED'
    NRO_UPDATING = 'NRO_UPDATING'
    HISTORICAL = 'HISTORICAL'
    VALID_STATES = [DRAFT, INPROGRESS, CANCELLED, REFUND_REQUESTED, HOLD, APPROVED, REJECTED, CONDITIONAL, EXPIRED, RESERVED, COND_RESERVE]
    RELEASE_STATES = [DRAFT, INPROGRESS, CANCELLED, HOLD, APPROVED, REJECTED, CONDITIONAL, EXPIRED]
    COMPLETED_STATE = [APPROVED, REJECTED, CONDITIONAL]
    CANCELLABLE_STATES = [DRAFT, INPROGRESS, HOLD, APPROVED, REJECTED, CONDITIONAL, RESERVED, COND_RESERVE]
    ALL_STATES = VALID_STATES + RELEASE_STATES + COMPLETED_STATE + [COMPLETED, HISTORICAL, NRO_UPDATING]

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
