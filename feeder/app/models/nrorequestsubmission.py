"""Request is the main business class that is the real top level object in the system
"""
from app import db


class NRORequestSubmission(db.Model):
    __bind_key__ = 'nro_db'
    __table_args__ = {"schema": "bc_registries_names"}
    __tablename__ = 'request_submission_info'

    nr_num = db.Column('nr_num', db.String(10), primary_key=True)
    request_id = db.Column('request_id', db.Integer)
    request_instance_id = db.Column('request_instance_id', db.Integer)
    request_type_cd = db.Column('request_type_cd', db.String(10))
    priority_cd = db.Column('priority_cd', db.String(2))
    tilma_ind = db.Column('tilma_ind', db.String(1))
    xpro_jurisdiction = db.Column('xpro_jurisdiction', db.String(40))
    nuans_expiration_date = db.Column('nuans_expiration_date', db.DateTime)
    additional_info = db.Column('additional_info', db.String(150))
    nature_business_info = db.Column('nature_business_info', db.String(1000))
    user_note = db.Column('user_note', db.String(1000))
    nuans_num = db.Column('nuans_num', db.String(20))
    tilma_transaction_id = db.Column('tilma_transaction_id', db.Integer)
    assumed_nuans_num = db.Column('assumed_nuans_num', db.String(20))
    assumed_nuans_name = db.Column('assumed_nuans_name', db.String(255))
    assumed_nuans_expiration_date = db.Column('assumed_nuans_expiration_date', db.DateTime)
    last_nuans_update_role = db.Column('last_nuans_update_role', db.String(10))
    admin_comment = db.Column('admin_comment', db.String(1000))
    applicant = db.Column(db.String(50))
    phone_number = db.Column('phone_number', db.String(30))
    contact = db.Column(db.String(150))
    ab_partner = db.Column('ab_partner', db.String(4000))
    sk_partner = db.Column('sk_partner', db.String(4000))

    # Relationship
    nro_names = db.relationship('NRONameSubmission', lazy='dynamic')

    def json(self):
        return {
                'nrNum': self.nr_num,
                'adminComment': self.admin_comment,
                'applicant': self.applicant,
                'phoneNumber': self.phone_number,
                'contact': self.contact,
                'abPartner': self.ab_partner,
                'names': [name.json() for name in self.nro_names.all()]
        }

    @classmethod
    def find_by_nr(cls, nr):
        return cls.query.filter_by(nr_num=nr).one()

    def all_names(self):
        return self.nro_names.all()
