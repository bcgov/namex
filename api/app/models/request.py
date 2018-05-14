"""Request is the main business class that is the real top level object in the system
"""
from app import db, ma
from app.exceptions import BusinessException
from sqlalchemy import Sequence
from marshmallow import Schema, fields, post_load
from app.models import Name, NameSchema
from datetime import datetime
import logging

# create sequence if not exists nr_seq;
# noinspection PyPep8Naming
class Request(db.Model):
    __tablename__ = 'requests'

    # Field names use a JSON / JavaScript naming pattern,
    # as opposed to the common python Snake_case

    # core fields
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdate = db.Column('last_update', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
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
    tilmaInd = db.Column('tilma_ind', db.String(1))
    tilmaTransactionId = db.Column('tilma_transaction_id', db.Integer)
    xproJurisdiction = db.Column('xpro_jurisdiction', db.String(40))
    additionalInfo = db.Column('additional_info', db.String(150))
    natureBusinessInfo = db.Column('nature_business_info', db.String(1000))
    userNote = db.Column('user_note', db.String(1000))

    #nuans fields
    nuansNum = db.Column('nuans_num', db.String(20))
    nuansExpirationDate = db.Column('nuans_expiration_date', db.DateTime)
    assumedNuansNum = db.Column('assumed_nuans_num', db.String(20))
    assumedNuansName = db.Column('assumed_nuans_name', db.String(255))
    assumedNuansExpirationDate = db.Column('assumed_nuans_expiration_date', db.DateTime)
    lastNuansUpdateRole = db.Column('last_nuans_update_role', db.String(10))

    #legacy sync tracking
    nroUpdated = db.Column('nro_updated', db.String(1), default='N')

    # Relationship
    names = db.relationship('Name', lazy='dynamic')

    userId = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    # user = db.relationship('User')

    ##### end of table definitions

    # Request States
    STATE_DRAFT = 'DRAFT'
    STATE_INPROGRESS ='INPROGRESS'
    STATE_CANCELLED = 'CANCELLED'
    STATE_HOLD = 'HOLD'
    STATE_APPROVED = 'APPROVED'
    STATE_REJECTED = 'REJECTED'
    STATE_CONDITIONAL = 'CONDITIONAL'
    VALID_STATES = { STATE_DRAFT, STATE_INPROGRESS, STATE_CANCELLED, STATE_HOLD, STATE_APPROVED, STATE_REJECTED, STATE_CONDITIONAL }
    RELEASE_STATES = { STATE_DRAFT, STATE_CANCELLED, STATE_HOLD, STATE_APPROVED, STATE_REJECTED, STATE_CONDITIONAL }


    def __init__(self, timestamp, lastUpdate, state, nrNum, userId, adminComment, applicant, phoneNumber, contact, abPartner, skPartner, consentFlag, examComment, expiryDate, requestId, requestTypeCd, priorityCd, tilmaInd, tilmaTransactionId, xproJurisdiction, additionalInfo, natureBusinessInfo, userNote, nuansNum, nuansExpirationDate, assumedNuansNum, assumedNuansName, assumedNuansExpirationDate, lastNuansUpdateRole):
        self.timestamp = timestamp
        self.lastUpdate = lastUpdate
        self.state = state
        self.nrNum = nrNum
        self.adminComment = adminComment
        self.applicant = applicant
        self.phoneNumber = phoneNumber
        self.contact = contact
        self.abPartner = abPartner
        self.skPartner = skPartner
        self.consentFlag = consentFlag
        self.examComment = examComment
        self.expiryDate = expiryDate
        self.requestId = requestId
        self.requestTypeCd = requestTypeCd
        self.priorityCd = priorityCd
        self.tilmaInd = tilmaInd
        self.tilmaTransactionId = tilmaTransactionId
        self.xproJurisdiction = xproJurisdiction
        self.additionalInfo = additionalInfo
        self.natureBusinessInfo = natureBusinessInfo
        self.userNote = userNote
        self.nuansNum = nuansNum
        self.nuansExpirationDate = nuansExpirationDate
        self.assumedNuansNum = assumedNuansNum
        self.assumedNuansName = assumedNuansName
        self.assumedNuansExpirationDate = assumedNuansExpirationDate
        self.lastNuansUpdateRole = lastNuansUpdateRole
        self.userId = userId

    def json(self):
        return {'id' : self.id,
                'timestamp' : self.timestamp,
                'lastUpdate' : self.lastUpdate,
                'userId' : self.userId,
                'state' : self.state,
                'nrNum' : self.nrNum,
                'adminComment' : self.adminComment,
                'applicant' : self.applicant,
                'phoneNumber' : self.phoneNumber,
                'contact' : self.contact,
                'abPartner' : self.abPartner,
                'skPartner' : self.skPartner,
                'consentFlag' : self.consentFlag,
                'examComment' : self.examComment,
                'expiryDate' : self.expiryDate,
                'requestId' : self.requestId,
                'requestTypeCd' : self.requestTypeCd,
                'priorityCd' : self.priorityCd,
                'tilmaInd' : self.tilmaInd,
                'tilmaTransactionId' : self.tilmaTransactionId,
                'xproJurisdiction' : self.xproJurisdiction,
                'additionalInfo' : self.additionalInfo,
                'natureBusinessInfo' : self.natureBusinessInfo,
                'userNote' : self.userNote,
                'nuansNum' : self.nuansNum,
                'nuansExpirationDate' : self.nuansExpirationDate,
                'assumedNuansNum' : self.assumedNuansNum,
                'assumedNuansName' : self.assumedNuansName,
                'assumedNuansExpirationDate' : self.assumedNuansExpirationDate,
                'lastNuansUpdateRole' : self.lastNuansUpdateRole,
                'names': [name.json() for name in self.names.all()]}

    @classmethod
    def find_by_nr(cls, nr):
        return cls.query.filter_by(nrNum=nr).one_or_none()

    def save_to_db(self):
        # if self.id is None:
            # NR is not the primary key, but has to be a unique value.
            # seq = Sequence('nr_seq')
            # next_nr = db.engine.execute(seq)
            # self.nr = 'NR{0:0>8}'.format(next_nr)

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        #TODO: Add listener onto the SQLALchemy event to block deletes
        raise BusinessException({"code": "cannot_delete_nr",
                                 "description":
                                     "NRs cannot be deleted, maybe try cancelling instead"},
                                403)

    @classmethod
    def get_queued_oldest(cls, userObj):
        """Gets the Next NR# from the database
           It sets the STATUS == INPROGRESS
           and then returns the NR or
           error out with a SQLAlchemy Error type
        """
        existing_nr = db.session.query(Request).\
            filter(Request.userId == userObj.id, Request.state == Request.STATE_INPROGRESS).\
            order_by(Request.timestamp.asc()).\
            one_or_none()

        if existing_nr:
            return existing_nr.nrNum

        r = db.session.query(Request).\
                filter(Request.state.in_([Request.STATE_DRAFT])).\
                order_by(Request.timestamp.asc()).\
                with_for_update().first()
        # this row is now locked

        # mark this as assigned to the user, masking it from others.
        r.state= Request.STATE_INPROGRESS
        r.userId = userObj.id

        db.session.add(r)
        db.session.commit()
        # db.session.close()
        return r.nrNum

    @classmethod
    def get_inprogress(cls, userObj):
        """Gets the Next NR# from the database
           where the STATUS == INPROGRESS
           and assigned to the user
        """
        existing_nr = db.session.query(Request).\
            filter(Request.userId == userObj.id, Request.state == Request.STATE_INPROGRESS).\
            order_by(Request.timestamp.asc()).\
            one_or_none()

        return existing_nr


class RequestsSchema(ma.ModelSchema):
    class Meta:
        model = Request

    names = ma.Nested(NameSchema, many=True)
