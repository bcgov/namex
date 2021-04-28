"""Name hold a name choice for a Request
"""
from . import db, ma
from sqlalchemy.orm import backref
from marshmallow import fields


class Applicant(db.Model):
    __tablename__ = 'applicants'

    partyId = db.Column('party_id', db.Integer, primary_key=True)
    lastName = db.Column('last_name', db.String(50))
    firstName = db.Column('first_name', db.String(50))
    middleName = db.Column('middle_name', db.String(50))
    phoneNumber = db.Column('phone_number', db.String(30))
    faxNumber = db.Column('fax_number', db.String(30))
    emailAddress = db.Column('email_address', db.String(75))
    contact = db.Column('contact', db.String(150))
    clientFirstName = db.Column('client_first_name', db.String(50))
    clientLastName = db.Column('client_last_name', db.String(50))
    declineNotificationInd = db.Column('decline_notification_ind', db.String(1))
    addrLine1 = db.Column('addr_line_1', db.String(200))
    addrLine2 = db.Column('addr_line_2', db.String(200))
    addrLine3 = db.Column('addr_line_3', db.String(200))
    city = db.Column('city', db.String(200))
    postalCd = db.Column('postal_cd', db.String(20))
    stateProvinceCd = db.Column('state_province_cd', db.String(2))
    countryTypeCd = db.Column('country_type_cd', db.String(2))

    nrId = db.Column('nr_id', db.Integer, db.ForeignKey('requests.id'), index=True)

    # Relationships - Requests
    # applicants = db.relationship("Requests", backref=backref("applicants", uselist=False), foreign_keys=[nrId])

    def as_dict(self):
        return {
            'partyId': self.partyId,
            'lastName': self.lastName,
            'firstName': self.firstName,
            'middleName': self.middleName,
            'phoneNumber': self.phoneNumber,
            'faxNumber': self.faxNumber,
            'emailAddress': self.emailAddress,
            'contact': self.contact,
            'clientFirstName': self.clientFirstName,
            'clientLastName': self.clientLastName,
            'declineNotificationInd': self.declineNotificationInd,
            'addrLine1': self.addrLine1,
            'addrLine2': self.addrLine2,
            'addrLine3': self.addrLine3,
            'city': self.city,
            'postalCd': self.postalCd,
            'stateProvinceCd': self.stateProvinceCd,
            'countryTypeCd': self.countryTypeCd
        }

    # @classmethod
    # def find_by_name(cls, name):
    #     return cls.query.filter_by(name=name).first()
    #
    def save_to_db(self):
        db.session.add(self)
        # db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        # db.session.commit()


class ApplicantSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Applicant
        fields = (
            'lastName',
            'firstName',
            'middleName',
            'phoneNumber',
            'faxNumber',
            'emailAddress',
            'contact',
            'clientFirstName',
            'clientLastName',
            'declineNotificationInd',
            'addrLine1',
            'addrLine2',
            'addrLine3',
            'city',
            'partyId',
            'postalCd',
            'stateProvinceCd',
            'countryTypeCd'
        )
    firstName = fields.String(allow_none=True)
    lastName = fields.String(allow_none=True)
    middleName = fields.String(allow_none=True)
    phoneNumber = fields.String(allow_none=True)
    faxNumber = fields.String(allow_none=True)
    emailAddress = fields.String(allow_none=True)
    contact = fields.String(allow_none=True)
    clientFirstName = fields.String(allow_none=True)
    clientLastName = fields.String(allow_none=True)
    declineNotificationInd = fields.Field(allow_none=True)
    addrLine1 = fields.String(allow_none=True)
    addrLine2 = fields.String(allow_none=True)
    addrLine3 = fields.String(allow_none=True)
    city = fields.String(allow_none=True)
    partyId = fields.Field(allow_none=True)
    postalCd = fields.String(allow_none=True)
    stateProvinceCd = fields.String(allow_none=True)
    countryTypeCd = fields.String(allow_none=True)
