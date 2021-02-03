"""Payments for a Request."""
from sqlalchemy import event

from namex.models import State, db


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    _payment_token = db.Column('payment_id', db.String(4096))
    _payment_completion_date = db.Column('payment_completion_date', db.DateTime(timezone=True))
    _payment_status_code = db.Column('payment_status_code', db.String(50))
    payment_note = db.Column('payment_note', db.String(100))
    payment_action = db.Column('payment_action', db.String(50))
    furnished = db.Column('furnished',db.Boolean, default=False)


    nrId = db.Column('nr_id', db.Integer, db.ForeignKey('requests.id'), index=True)

    # properties
    @property
    def payment_token(self):
        """Property containing the payment token."""
        return self._payment_token

    @payment_token.setter
    def payment_token(self, token: str):
        self._payment_token = token

    @property
    def payment_completion_date(self):
        """Property containing the date the payment cleared."""
        return self._payment_completion_date

    @payment_completion_date.setter
    def payment_completion_date(self, date):
        """Property containing the date the payment cleared."""
        self._payment_completion_date = date

    @property
    def payment_status_code(self):
        """Property containing the payment token."""
        return self._payment_status_code

    @payment_status_code.setter
    def payment_status_code(self, str):
        self._payment_status_code = str

    @classmethod
    def find_by_payment_token(cls, token):
        return cls.query.filter_by(payment_id=token).one_or_none()


    def as_dict(self):
        return {
            'id': self.id,
            'nr_id': self.nrId,
            'payment_token': self.payment_token,
            'payment_note': self.payment_note,
            'payment_completion_date': self.payment_completion_date,
            'payment_status_code': self.payment_status_code,
            'payment_action': self.payment_action,
            'receipt_sent': self.furnished
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        pass

@event.listens_for(Payment, 'after_insert')
@event.listens_for(Payment, 'before_update')
def update_nr_state(mapper, connection, target):
    """Set the state of the NR based on payment_status_code."""
    from namex.models import Request

    payment = target
    nr = Request.find_by_id(payment.nrId)
    if nr:
        # could not make this update properly via the model so used raw sql
        if payment.payment_status_code != 'REFUND_REQUESTED':
            if payment.payment_status_code == 'COMPLETED' and nr.stateCd == 'PENDING_PAYMENT':
                connection.execute(
                    f"""
                    UPDATE requests
                    SET state_cd='{State.DRAFT}'
                    WHERE id={nr.id}
                    """
                )

