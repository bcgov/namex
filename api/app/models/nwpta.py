from app import db, ma
from datetime import datetime
from sqlalchemy.orm import backref

class PartnerNameSystem(db.Model):
    __tablename__ = 'partner_name_system'

    id = db.Column(db.Integer, primary_key=True)
    partnerNameTypeCd = db.Column('partner_name_type_cd', db.String(2))
    partnerNameNumber = db.Column('partner_name_number', db.String(20))
    partnerJurisdictionTypeCd = db.Column('partner_jurisdiction_type_cd', db.String(3))
    partnerNameDate = db.Column('partner_name_date', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    partnerName = db.Column('partner_name', db.String(255))

    # parent keys
    nrId = db.Column('nr_id', db.Integer, db.ForeignKey('requests.id'))

    def as_dict(self):
        return {
            'partnerNameTypeCd': self.partnerNameTypeCd,
            'partnerNameNumber': self.partnerNameNumber,
            'partnerJurisdictionTypeCd': self.partnerJurisdictionTypeCd,
            'partnerNameDate': self.partnerNameDate,
            'partnerName': self.partnerName
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        pass
