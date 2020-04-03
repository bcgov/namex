"""Request is the main business class that is the real top level object in the system
"""
from . import db, ma
from flask import current_app
from namex.exceptions import BusinessException
from sqlalchemy import event
from sqlalchemy.orm import backref
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import and_, func
from marshmallow import Schema, fields, post_load, post_dump
from .nwpta import PartnerNameSystem
from .user import User, UserSchema
from .comment import Comment, CommentSchema
from .applicant import Applicant
from .name import Name, NameSchema
from .state import State, StateSchema
from datetime import datetime
import re

from namex.constants import ValidSources, request_type_mapping

# noinspection PyPep8Naming
from ..criteria.request.query_criteria import RequestConditionCriteria

class Request(db.Model):

    __tablename__ = 'requests'

    # Field names use a JSON / JavaScript naming pattern,
    # as opposed to the common python Snake_case

    # core fields
    id = db.Column(db.Integer, primary_key=True)
    submittedDate = db.Column('submitted_date', db.DateTime(timezone=True), default=datetime.utcnow, index=True)
    lastUpdate = db.Column('last_update', db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    nrNum = db.Column('nr_num', db.String(10), unique=True)
    requestTypeCd = db.Column('request_type_cd', db.String(10))
    priorityCd = db.Column('priority_cd', db.String(2))
    priorityDate = db.Column('priority_date', db.DateTime(timezone=True))
    expirationDate = db.Column('expiration_date', db.DateTime(timezone=True))
    consentFlag = db.Column('consent_flag', db.String(1))
    additionalInfo = db.Column('additional_info', db.String(150))
    natureBusinessInfo = db.Column('nature_business_info', db.String(1000))
    xproJurisdiction = db.Column('xpro_jurisdiction', db.String(40))
    corpNum = db.Column('corp_num', db.String(20), default=None)
    submitter_userid = db.Column('submitter_userid', db.Integer, db.ForeignKey('users.id'))
    # legacy sync tracking
    furnished = db.Column('furnished', db.String(1), default='N', index=True)

    # Flag to indicate this NR has been reset. Cleared upon submission, so it is only true after
    # reset before subsequent examination is complete.
    hasBeenReset = db.Column('has_been_reset', db.Boolean, default=False)

    # parent keys
    userId = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), index=True)

    # legacy fields
    requestId = db.Column('request_id', db.Integer)
    previousRequestId = db.Column('previous_request_id', db.Integer)
    submitCount = db.Column('submit_count', db.Integer)
    nroLastUpdate = db.Column('nro_last_update', db.DateTime(timezone=True))

    # Relationship State
    stateCd = db.Column('state_cd', db.String(40), db.ForeignKey('states.cd'), index=True)

    # previous state, used when editing NR in certain scenarios
    previousStateCd = db.Column('prev_state_cd', db.String(40), nullable=True)

    # Relationships - Users
    activeUser = db.relationship('User', backref=backref('active_user', uselist=False), foreign_keys=[userId])
    submitter = db.relationship('User', backref=backref('submitter', uselist=False), foreign_keys=[submitter_userid])
    # Relationships - Names
    names = db.relationship('Name', lazy='dynamic')
    # Relationships - Applicants
    applicants = db.relationship('Applicant', lazy='dynamic')
    # Relationships - Examiner Comments
    comments = db.relationship('Comment', lazy='dynamic', order_by="Comment.timestamp")
    # Relationships - Examiner Comments
    partnerNS = db.relationship('PartnerNameSystem', lazy='dynamic')

    # Name Request Additional Fields
    _request_action_cd = db.Column('request_action_cd', db.String(10))
    _entity_type_cd = db.Column('entity_type_cd', db.String(10))
    consent_dt = db.Column('consent_dt', db.DateTime(timezone=True))
    _payment_token = db.Column('payment_id', db.String(4096))
    _payment_completion_date = db.Column('payment_completion_date', db.DateTime(timezone=True))
    _source = db.Column('source', db.String(15), default=ValidSources.NRO)

    ##### end of table definitions
    REQUEST_FURNISHED = 'Y'

    # properties
    @hybrid_property
    def payment_token(self):
        """Property containing the payment token."""
        return self._payment_token

    @payment_token.setter
    def payment_token(self, token: int):
        if self.locked:
            self._raise_default_lock_exception()
        self._payment_token = token

    @hybrid_property
    def payment_completion_date(self):
        """Property containing the date the payment cleared."""
        return self._payment_completion_date

    @property
    def source(self):
        """Property containing the source app."""
        return self._source

    @property
    def request_action_cd(self):
        """Property containing the request action from name request."""
        return self._request_action_cd

    @request_action_cd.setter
    def request_action_cd(self, value: str):
        self._request_action_cd = value

    @property
    def entity_type_cd(self):
        """Property containing the entity type from name request"""
        return self._entity_type_cd

    @entity_type_cd.setter
    def entity_type_cd(self, value: str):
        self._entity_type_cd = value

    def __init__(self, *args, **kwargs):
        pass

    def json(self):

        # get previous NR number from legacy requestId and previousRequestId fields
        previousNr = None
        if self.previousRequestId:
            previousNr = self.query.filter_by(requestId=self.previousRequestId).first()
        try:
            # we just want the NR number, or null if it doesn't exist
            previousNr = previousNr.nrNum
        except:
            previousNr = None

        return {'id': self.id,
                'submittedDate': self.submittedDate,
                'lastUpdate': self.lastUpdate,
                'userId': '' if (self.activeUser is None) else self.activeUser.username,
                'submitter_userid': '' if (self.submitter is None) else self.submitter.username,
                'state': self.stateCd,
                'previousStateCd': self.previousStateCd,
                'nrNum': self.nrNum,
                'consentFlag': self.consentFlag,
                'consent_dt': self.consent_dt,
                'expirationDate': self.expirationDate,
                'requestTypeCd': self.requestTypeCd,
                'entity_type_cd':self.entity_type_cd,
                'request_action_cd': self.request_action_cd,
                'priorityCd': self.priorityCd,
                'priorityDate': self.priorityDate,
                'xproJurisdiction': self.xproJurisdiction,
                'additionalInfo': self.additionalInfo,
                'natureBusinessInfo': self.natureBusinessInfo,
                'furnished': self.furnished if (self.furnished is not None) else 'N',
                'hasBeenReset': self.hasBeenReset,
                'previousRequestId': self.previousRequestId,
                'previousNr': previousNr,
                'submitCount': self.submitCount,
                'corpNum': self.corpNum,
                'names': [name.as_dict() for name in self.names.all()],
                'applicants': '' if (
                        self.applicants.one_or_none() is None) else self.applicants.one_or_none().as_dict(),
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
        # TODO: Add listener onto the SQLALchemy event to block deletes
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
        existing_nr = Request.get_inprogress(userObj)

        if existing_nr:
            current_app.logger.info('Existing NR found, returning: {}'.format(existing_nr.nrNum))
            return existing_nr, False

        # this will error if there's nothing in the queue - likelihood ~ 0
        r = db.session.query(Request). \
            filter(Request.stateCd.in_([State.DRAFT])). \
            order_by(Request.priorityCd.desc(), Request.submittedDate.asc()). \
            with_for_update().first()
        # this row is now locked

        if not r:
            raise BusinessException(None, 404)

        # mark this as assigned to the user, masking it from others.
        r.stateCd = State.INPROGRESS
        r.userId = userObj.id

        db.session.add(r)
        db.session.commit()
        return r, True

    @classmethod
    def get_inprogress(cls, userObj):
        """Gets the Next NR# from the database
           where the STATUS == INPROGRESS
           and assigned to the user
           this assumes that a user can ONLY EVER have 1 Request in progress at a time.
        """
        existing_nr = db.session.query(Request). \
            filter(Request.userId == userObj.id, Request.stateCd == State.INPROGRESS). \
            one_or_none()

        return existing_nr

    @classmethod
    def find_name(cls, nr, choice):
        return cls.query.filter_by(nrNum=nr).names.filter_by(choice=choice).one_or_none()

    @classmethod
    def validNRFormat(cls, nr):
        '''NR should be of the format "NR 1234567"
        '''
        if len(nr) != 10 or nr[:2] != 'NR' or nr[2:3] != ' ':
            return False

        try:
            num = int(nr[3:])
        except:
            return False

        return True

    # START NEW NAME_REQUEST SERVICE METHODS, WE WILL REFACTOR THESE SHORTLY
    @classmethod
    def get_general_query(cls):
        filters = [
            Request.id == Name.nrId,
            Request.stateCd.in_([State.APPROVED, State.CONDITIONAL]),
            Request.requestTypeCd.in_(
                ['PA', 'CR', 'CP', 'FI', 'SO', 'UL', 'CUL', 'CCR', 'CFI', 'CCP', 'CSO', 'CCC', 'CC']),
            Name.state.in_(['APPROVED', 'CONDITION'])
        ]

        criteria = RequestConditionCriteria(
            fields=[Name.name],
            filters=filters
        )

        return criteria

    @classmethod
    def get_query_exact_match(cls, criteria, prep_name):
        criteria.filters.append(func.lower(Name.name) == func.lower(prep_name))

        results = Request.find_by_criteria(criteria)
        flattened = [item.strip() for sublist in results for item in sublist]

        return flattened

    @classmethod
    def get_query_distinctive_descriptive(cls, descriptive_element, criteria, distinctive=False):
        if not distinctive:
            # Reset filter index 5 which contains the descriptive in the previous round.
            # The filter index 4 contains distinctive value
            if len(criteria.filters) > 5:
                criteria.filters.pop()
            substitutions = ' ?| '.join(map(str, descriptive_element)) + ' ?'
            criteria.filters.append(func.lower(Name.name).op('~')(r'\s+\y{}\y'.format(substitutions)))
        else:
            substitutions = '|'.join(map(str, descriptive_element))
            criteria.filters.append(func.lower(Name.name).op('~')(r'^\s*\W*({})\y\W*\s+'.format(substitutions)))
            return criteria

        results = Request.find_by_criteria(criteria)
        flattened = [item.strip() for sublist in results for item in sublist]

        return flattened

    @classmethod
    def find_by_criteria(cls, criteria=None):
        RequestConditionCriteria.is_valid_criteria(criteria)

        query = cls.query.with_entities(*criteria.fields) \
            .filter(and_(*criteria.filters))

        # print(query.statement)
        return query.all()

#set the source from NRO, Societis Online, Name Request
@event.listens_for(Request, 'before_insert')
@event.listens_for(Request, 'before_update')
def set_source(mapper, connection, target):  # pylint: disable=unused-argument; SQLAlchemy callback signature
    """Set the source of the NR."""
    request = target
    soc_list = []
    soc_list = ['SO','ASO','CSO','RSO','CTSO','XSO','XCSO','XRSO','XASO','XCASO','CSSO']

    # comes from NRO/Societies Online
    if(re.match(r"NR [0-9]+", request.nrNum) and request.requestTypeCd not in soc_list):
        request._source = ValidSources.NRO.value  # pylint: disable=protected-access
    else:
        if (re.match(r"NR [A-Z]+", request.nrNum)):
             request._source = ValidSources.NAMEREQUEST.value   # pylint: disable=protected-access
        else:
            if(request.requestTypeCd in soc_list ):
             request._source = ValidSources.SO.value   # pylint: disable=protected-access


@event.listens_for(Request, 'before_insert')
@event.listens_for(Request, 'before_update')
def update_request_action_entity_type(mapper, connection, target): # pylint: disable=unused-argument; SQLAlchemy callback signature
    """Set the request_action when it is null because the NR is coming from NRO or NAMEX or Societies Online"""
    # needed to break apart  request_type
    request = target
    if (re.match(r"NR [0-9]+", request.nrNum) and request.requestTypeCd != None):
        # todo: handle assumed name as it is a name type and not currently a request action?
        # map the legacy request_type to the new Entity_type and Request_action
        new_value = request.requestTypeCd
        output = [item for item in request_type_mapping
                  if item[0] == new_value]

        request._entity_type_cd = output[0][1]
        request._request_action_cd = output[0][2]

@event.listens_for(Request, 'before_update')
def add_to_word_class_queue(mapper, connection, target):  # pylint: disable=unused-argument; SQLAlchemy callback signature
    """Set the cleaned_name when an examiner approves a BC corp class request_type when it is approved/conditionally approved in Namex"""
    # needed to reduce query time for conflict matching in Name Request
    request = target
    # TODO: put the name on the word classification queue to be picked up by the word classification service and update wod classification table
    # TODO: may have to review which entity types are included
    #if(request.stateCd  == 'APPROVED' and request.requestTypeCd in ['CR','CCR','CC','CCC','UL','CUL','BC'] and request.source != 'NAMEREQUEST' :
        #add it to the queue to add or update words
    #if(request_stateCd == 'HOLD' and request.requestTypeCd in ['CR','CCR','CC','CCC','UL','CUL','BC'] and request.source != 'NAMEREQUEST' and request.hasBeenReset=True):
        #add to the queue to decrement or remove words from word classification

class RequestsSchema(ma.ModelSchema):
    class Meta:
        model = Request
        additional = ['stateCd']

    names = ma.Nested(NameSchema, many=True)
    activeUser = ma.Nested(UserSchema, many=False, only='username')
    submitter = ma.Nested(UserSchema, many=False, only='username')
    comments = ma.Nested(CommentSchema, many=True, only=['comment', 'examiner', 'timestamp'])

    @post_dump
    def clean_missing(self, data):
        ret = data.copy()
        for key in filter(lambda key: data[key] is None, data):
            del ret[key]
        return ret


class RequestsHeaderSchema(ma.ModelSchema):
    class Meta:
        model = Request
        # sqla_session = db.scoped_session
        # additional = ['stateCd']
        fields = ('additionalInfo'
                  , 'consentFlag'
                  , 'corpNum'
                  , 'expirationDate'
                  , 'furnished'
                  , 'hasBeenReset'
                  , 'id'
                  , 'natureBusinessInfo'
                  , 'nrNum'
                  , 'nroLastUpdate'
                  , 'priorityCd'
                  , 'requestTypeCd'
                  , 'stateCd'
                  , 'previousStateCd'
                  , 'submitCount'
                  , 'submittedDate'
                  , 'xproJurisdiction'
                  )


class RequestsSearchSchema(ma.ModelSchema):
    class Meta:
        model = Request
        # sqla_session = db.scoped_session
        # additional = ['stateCd']
        fields = ('additionalInfo'
                  , 'comments'
                  , 'consentFlag'
                  , 'corpNum'
                  , 'expirationDate'
                  , 'furnished'
                  , 'lastUpdate'
                  , 'natureBusinessInfo'
                  , 'nrNum'
                  , 'nroLastUpdate'
                  , 'priorityCd'
                  , 'priorityDate'
                  , 'requestTypeCd'
                  , 'stateCd'
                  , 'submitCount'
                  , 'submittedDate'
                  , 'xproJurisdiction'
                  , 'names'
                  , 'activeUser'
                  )

    names = ma.Nested(NameSchema, many=True)
    activeUser = ma.Nested(UserSchema, many=False, only='username')
    comments = ma.Nested(CommentSchema, many=True, only=['comment', 'examiner', 'timestamp'])
