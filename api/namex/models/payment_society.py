"""Payment_societies keep data for society from home legancy app
"""
from . import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

class PaymentSociety(db.Model):
    __tablename__ = 'payment_societies'

    id = db.Column(db.Integer, primary_key=True)
    nrNum = db.Column('nr_num', db.String(10), unique=True)
    corpNum = db.Column('corp_num', db.String(20), unique=True)
    paymentCompletionDate = db.Column('payment_completion_date', db.DateTime(timezone=True), default=datetime.utcnow)
    paymentStatusCode = db.Column('payment_status_code', db.String(30), unique=True)
    paymentFeeCode = db.Column('payment_fee_code', db.String(30), unique=True)
    paymentType = db.Column('payment_type', db.String(30), unique=True)
    paymentAmount = db.Column('payment_amount', db.Numeric(19, 2), unique=True)
    paymentJson = db.Column('payment_json', JSONB)
    paymentAction = db.Column('payment_action', db.String(30), unique=True)

    def json(self):
        return {"id": self.id, 
                "nrNum": self.nrNum
                }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_to_session(self):
        db.session.add(self)