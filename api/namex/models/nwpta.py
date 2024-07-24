from . import db, ma
from marshmallow import fields


class PartnerNameSystem(db.Model):
    __tablename__ = 'partner_name_system'

    id = db.Column(db.Integer, primary_key=True)
    partnerNameTypeCd = db.Column('partner_name_type_cd', db.String(10))
    partnerNameNumber = db.Column('partner_name_number', db.String(20))
    partnerJurisdictionTypeCd = db.Column('partner_jurisdiction_type_cd', db.String(3))
    partnerNameDate = db.Column('partner_name_date', db.DateTime(timezone=True))
    partnerName = db.Column('partner_name', db.String(255))

    # "do it for me" (ie: NWPTA requested) indicator, set when data comes from Oracle so we have a
    # record of this, regardless of current state of data
    requested = db.Column('requested', db.Boolean(), default=False)

    # parent keys
    nrId = db.Column('nr_id', db.Integer, db.ForeignKey('requests.id'), index=True)

    def as_dict(self):
        return {
            'partnerNameTypeCd': self.partnerNameTypeCd,
            'partnerNameNumber': self.partnerNameNumber,
            'partnerJurisdictionTypeCd': self.partnerJurisdictionTypeCd,
            'partnerNameDate': self.partnerNameDate,
            'partnerName': self.partnerName,
            'requested': True if self.requested else False,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        pass


class PartnerNameSystemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PartnerNameSystem
        fields = (
            'partnerNameTypeCd',
            'partnerNameNumber',
            'partnerJurisdictionTypeCd',
            'partnerNameDate',
            'partnerName',
            'requested'
        )
    partnerName = fields.String(required=False, allow_none=True)
