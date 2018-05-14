"""Request is the main business class that is the real top level object in the system
"""
from app import db
from datetime import datetime


# noinspection PyPep8Naming
class Request(db.Model):
    __bind_key__ = None
    __tablename__ = 'requests'

    # Field names use a JSON / JavaScript naming pattern,
    # as opposed to the common python Snake_case

    # core fields
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdate = db.Column('last_update', db.DateTime, default=datetime.utcnow)
    state = db.Column(db.String(40), default='DRAFT')
    nrNum = db.Column('nr_num', db.String(10), unique=True)
    adminComment = db.Column('admin_comment', db.String(1000))
    applicant = db.Column(db.String(50))
    phoneNumber = db.Column('phone_number', db.String(30))
    contact = db.Column(db.String(150))
    abPartner = db.Column('ab_partner', db.String(4000))
    skPartner = db.Column('sk_partner', db.String(4000))
    consentFlag = db.Column('consent_flag', db.String(1))
    examComment = db.Column('exam_comment', db.String(4000))
    expiryDate = db.Column('expiry_date', db.DateTime)

    # legacy fields
    requestId = db.Column('request_id', db.Integer)
    requestTypeCd = db.Column('request_type_cd', db.String(10))
    priorityCd = db.Column('priority_cd', db.String(2))
    # noinspection SpellCheckingInspection,SpellCheckingInspection
    tilmaInd = db.Column('tilma_ind', db.String(1))
    # noinspection SpellCheckingInspection,SpellCheckingInspection
    tilmaTransactionId = db.Column('tilma_transaction_id', db.Integer)
    # noinspection SpellCheckingInspection,SpellCheckingInspection
    xproJurisdiction = db.Column('xpro_jurisdiction', db.String(40))
    additionalInfo = db.Column('additional_info', db.String(150))
    natureBusinessInfo = db.Column('nature_business_info', db.String(1000))
    userNote = db.Column('user_note', db.String(1000))

    # nuans fields
    # noinspection SpellCheckingInspection,SpellCheckingInspection
    nuansNum = db.Column('nuans_num', db.String(20))
    # noinspection SpellCheckingInspection,SpellCheckingInspection
    nuansExpirationDate = db.Column('nuans_expiration_date', db.DateTime)
    # noinspection SpellCheckingInspection,SpellCheckingInspection
    assumedNuansNum = db.Column('assumed_nuans_num', db.String(20))
    # noinspection SpellCheckingInspection,SpellCheckingInspection
    assumedNuansName = db.Column('assumed_nuans_name', db.String(255))
    # noinspection SpellCheckingInspection,SpellCheckingInspection
    assumedNuansExpirationDate = db.Column('assumed_nuans_expiration_date', db.DateTime)
    # noinspection SpellCheckingInspection,SpellCheckingInspection
    lastNuansUpdateRole = db.Column('last_nuans_update_role', db.String(10))

    # Relationship
    names = db.relationship('Name', lazy='dynamic')

    userId = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    # ------ End of table definitions

    # Request States
    STATE_DRAFT = 'DRAFT'
    # noinspection SpellCheckingInspection,SpellCheckingInspection
    STATE_INPROGRESS = 'INPROGRESS'
    STATE_CANCELLED = 'CANCELLED'
    STATE_HOLD = 'HOLD'
    STATE_APPROVED = 'APPROVED'
    STATE_REJECTED = 'REJECTED'
    STATE_CONDITIONAL = 'CONDITIONAL'
    VALID_STATES = {STATE_DRAFT, STATE_INPROGRESS, STATE_CANCELLED, STATE_HOLD, STATE_APPROVED, STATE_REJECTED,
                    STATE_CONDITIONAL}

    def __init__(self):
        pass

    # noinspection PyPep8
    def json(self):
        # noinspection SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection
        return {'id': self.id,
                'timestamp': self.timestamp,
                'lastUpdate': self.lastUpdate,
                'userId': self.userId,
                'state': self.state,
                'nrNum': self.nrNum,
                'adminComment': self.adminComment,
                'applicant': self.applicant,
                'phoneNumber': self.phoneNumber,
                'contact': self.contact,
                'abPartner': self.abPartner,
                'skPartner': self.skPartner,
                'consentFlag': self.consentFlag,
                'examComment': self.examComment,
                'expiryDate': self.expiryDate,
                'requestId': self.requestId,
                'requestTypeCd': self.requestTypeCd,
                'priorityCd': self.priorityCd,
                'tilmaInd': self.tilmaInd,
                'tilmaTransactionId': self.tilmaTransactionId,
                'xproJurisdiction': self.xproJurisdiction,
                'additionalInfo': self.additionalInfo,
                'natureBusinessInfo': self.natureBusinessInfo,
                'userNote': self.userNote,
                'nuansNum': self.nuansNum,
                'nuansExpirationDate': self.nuansExpirationDate,
                'assumedNuansNum': self.assumedNuansNum,
                'assumedNuansName': self.assumedNuansName,
                'assumedNuansExpirationDate': self.assumedNuansExpirationDate,
                'lastNuansUpdateRole': self.lastNuansUpdateRole,
                'names': [name.json() for name in self.names.all()]}
