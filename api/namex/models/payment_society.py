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
    requestState = db.Column('request_state', db.String(40), unique=True)
    paymentState = db.Column('payment_status', db.String(50), unique=True)
    paymentDate = db.Column('payment_date', db.DateTime(timezone=True), default=datetime.utcnow)
    paymentJson = db.Column('payment_json', JSONB)    
   
    def json(self):
        return {"id": self.id, 
                "nrNum": self.nrNum, 
                "corpNum": self.corpNum, 
                "requestState": self.requestState, 
                "paymentState": self.paymentState, 
                "paymentDate": self.paymentDate, 
                "paymentJson": self.paymentJson
                }      

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_to_session(self):
        db.session.add(self)