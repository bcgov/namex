"""Request is the main business class that is the real top level object in the system
"""
from app import db, ma
from app.exceptions import BusinessException
from sqlalchemy import Sequence
from sqlalchemy.orm import backref
from marshmallow import Schema, fields, post_load
from .nwpta import PartnerNameSystem
from .user import User
from .comment import Comment
from .applicant import Applicant
from .name import Name, NameSchema
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
    submittedDate = db.Column('submitted_date', db.DateTime, default=datetime.utcnow)
    lastUpdate = db.Column('last_update', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    state = db.Column(db.String(40), default='DRAFT')
    nrNum = db.Column('nr_num', db.String(10), unique=True)
    requestTypeCd = db.Column('request_type_cd', db.String(10))
    priorityCd = db.Column('priority_cd', db.String(2))
    expirationDate = db.Column('expiration_date', db.DateTime)
    consentFlag = db.Column('consent_flag', db.String(1))
    additionalInfo = db.Column('additional_info', db.String(150))
    natureBusinessInfo = db.Column('nature_business_info', db.String(1000))
    xproJurisdiction = db.Column('xpro_jurisdiction', db.String(40))
    submitter_userid = db.Column('submitter_userid', db.Integer, db.ForeignKey('users.id'))
    #legacy sync tracking
    furnished = db.Column('furnished', db.String(1), default='N')

    # parent keys
    userId = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))

    # legacy fields
    requestId = db.Column('request_id', db.Integer)
    previousRequestId = db.Column('previous_request_id', db.Integer)
    submitCount = db.Column('submit_count', db.Integer)

    # Relationships - Users
    active_user = db.relationship('User', backref=backref('active_user', uselist=False), foreign_keys=[userId])
    submitter = db.relationship('User', backref=backref('submitter', uselist=False), foreign_keys=[submitter_userid])
    # Relationships - Names
    names = db.relationship('Name', lazy='dynamic')
    # Relationships - Applicants
    applicants = db.relationship('Applicant', lazy='dynamic')
    # Relationships - Examiner Comments
    comments = db.relationship('Comment', lazy='dynamic')
    # Relationships - Examiner Comments
    partnerNS = db.relationship('PartnerNameSystem', lazy='dynamic')

    ##### end of table definitions
    REQUEST_FURNISHED = 'Y'

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
    COMPLETED_STATE = { STATE_APPROVED, STATE_REJECTED, STATE_CONDITIONAL }


    def __init__(self, *args, **kwargs):
        pass

    def json(self):

        return {'id' : self.id,
                'submittedDate' : self.submittedDate,
                'lastUpdate' : self.lastUpdate,
                'userId' : '' if (self.active_user is None) else self.active_user.username,
                'submitter_userid' : '' if (self.submitter is None) else self.submitter.username,
                'state' : self.state,
                'nrNum' : self.nrNum,
                'consentFlag' : self.consentFlag,
                'expirationDate' : self.expirationDate,
                'requestTypeCd' : self.requestTypeCd,
                'priorityCd' : self.priorityCd,
                'xproJurisdiction' : self.xproJurisdiction,
                'additionalInfo' : self.additionalInfo,
                'natureBusinessInfo' : self.natureBusinessInfo,
                'furnished': self.furnished if (self.furnished is not None) else 'N',
                'names': [name.as_dict() for name in self.names.all()],
                'applicants': [applicant.as_dict() for applicant in self.applicants.all()],
                'comments': [comment.as_dict() for comment in self.comments.all()],
                'nwpta': [partner_name.as_dict() for partner_name in self.partnerNS.all()]
                }

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
            order_by(Request.submittedDate.asc()).\
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
