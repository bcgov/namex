"""Payments for a Request
"""
from . import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    _payment_token = db.Column('payment_id', db.String(4096))
    _payment_completion_date = db.Column('payment_completion_date', db.DateTime(timezone=True))
    _payment_status_code = db.Column('payment_status_code', db.String(50))

    nrId = db.Column('nr_id', db.Integer, db.ForeignKey('requests.id'), index=True)

    #properties
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
        return self._payment_date

    @payment_completion_date.setter
    def payment_date(self, date):
        """Property containing the date the payment cleared."""
        self._payment_date = date


    def as_dict(self):
        return {
            'id': self.id,
            'payment_token' : self.payment_token,
            'payment_completion_date' : self.payment_completion_date
        }


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        pass




