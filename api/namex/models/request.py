"""Request is the main business class that is the real top level object in the system
"""
import sqlalchemy
# TODO: Only trace if LOCAL_DEV_MODE / DEBUG conf exists
# import traceback

from . import db, ma
from flask import current_app
# TODO: Only trace if LOCAL_DEV_MODE / DEBUG conf exists
# from flask_sqlalchemy import get_debug_queries
from namex.exceptions import BusinessException
from sqlalchemy import event
from sqlalchemy.orm import backref
from sqlalchemy.dialects import postgresql
from sqlalchemy import and_, func, Date
from marshmallow import Schema, fields, post_load, post_dump
from .nwpta import PartnerNameSystem
from .user import User, UserSchema
from .comment import Comment, CommentSchema
from .applicant import Applicant
from .name import Name, NameSchema
from .payment import Payment
from .event import Event
from .state import State, StateSchema
from datetime import datetime, timedelta
import re

from namex.constants import ValidSources, NameState, \
    EntityTypes, LegacyEntityTypes, \
    request_type_mapping, RequestPriority, EventAction, EventState, EventUserId, DesignationPositionCodes

# noinspection PyPep8Naming
from ..criteria.request.query_criteria import RequestConditionCriteria
from ..services.statistics import UnitTime


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
    # Relationships - Events
    events = db.relationship('Event', lazy='dynamic')
    # Relationships - Applicants
    applicants = db.relationship('Applicant', lazy='dynamic')
    # Relationships - Examiner Comments
    comments = db.relationship('Comment', lazy='dynamic', order_by="Comment.timestamp")
    # Relationships - Examiner Comments
    partnerNS = db.relationship('PartnerNameSystem', lazy='dynamic')

    # Relationships - Payments
    payments = db.relationship('Payment', lazy='dynamic')

    # Name Request Additional Fields
    _request_action_cd = db.Column('request_action_cd', db.String(10))
    _entity_type_cd = db.Column('entity_type_cd', db.String(10))
    consent_dt = db.Column('consent_dt', db.DateTime(timezone=True))
    _source = db.Column('source', db.String(15), default=ValidSources.NRO)
    tradeMark = db.Column('trade_mark', db.String(100))

    # Check-In / Check-Out (for INPROGRESS)
    # A UUID granted to the user that checks out the Name Request
    checkedOutBy = db.Column('checked_out_by', db.String(64), index=True)
    checkedOutDt = db.Column('checked_out_dt', db.DateTime(timezone=True), index=True)

    # MRAS fields
    homeJurisNum = db.Column('home_juris_num', db.String(40))

    # End of table definitions
    REQUEST_FURNISHED = 'Y'

    # properties
    @property
    def has_consumed_name(self):
        names = self.names.all()

        def is_not_consumed(name):
            no_corp_num = name.corpNum is None
            no_consumption_date = name.consumptionDate is None

            return no_corp_num and no_consumption_date

        results = [is_not_consumed(n) is False for n in names]
        return True in results

    @property
    def is_expired(self):
        todays_date = datetime.utcnow().date()
        expiry_date = self.expirationDate.date() if self.expirationDate else None
        if expiry_date:
            return todays_date > expiry_date
        return False

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

        return {
            'id': self.id,
            'submittedDate': self.submittedDate,
            'lastUpdate': self.lastUpdate,
            'userId': '' if (self.activeUser is None) else self.activeUser.username,
            'submitter_userid': '' if (self.submitter is None) else self.submitter.username,
            # TODO: Lucas added stateCd not sure why when we're mapping to json we're sending back 'state' and not 'stateCd'
            'stateCd': self.stateCd,
            'state': self.stateCd,
            'previousStateCd': self.previousStateCd,
            'nrNum': self.nrNum,
            'consentFlag': self.consentFlag,
            'consent_dt': self.consent_dt,
            'expirationDate': self.expirationDate,
            'requestTypeCd': self.requestTypeCd,
            'entity_type_cd': self.entity_type_cd,
            'request_action_cd': self.request_action_cd,
            'source': self.source,
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
            'tradeMark': self.tradeMark,
            'homeJurisNum': self.homeJurisNum,
            'names': [name.as_dict() for name in self.names.all()],
            'applicants': '' if (self.applicants.one_or_none() is None) else self.applicants.one_or_none().as_dict(),
            'comments': [comment.as_dict() for comment in self.comments.all()],
            'nwpta': [partner_name.as_dict() for partner_name in self.partnerNS.all()],
            'checkedOutBy': self.checkedOutBy,
            'checkedOutDt': self.checkedOutDt
        }

    @classmethod
    def find_by_id(cls, internal_id: int):
        """Find NR by the internal id."""
        return cls.query.filter_by(id=internal_id).one_or_none()

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
        raise BusinessException({
            "code": "cannot_delete_nr",
            "description":
                "NRs cannot be deleted, maybe try cancelling instead"
        }, 403)

    @classmethod
    def get_queued_oldest(cls, userObj):
        """
        Gets the Next NR# from the database
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
            filter(
            Request.stateCd.in_([State.DRAFT]),
            Request.nrNum.notlike('NR L%')). \
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
    def get_oldest_draft(cls):
        """Get the oldest NR in DRAFT state."""
        return db.session.query(Request). \
            filter(
                Request.stateCd.in_([State.DRAFT]),
                Request.nrNum.notlike('NR L%')). \
            order_by(Request.submittedDate.asc()). \
            first()

    @classmethod
    def get_inprogress(cls, userObj):
        """
        Gets the Next NR# from the database where the STATUS == INPROGRESS and assigned to the user
        this assumes that a user can ONLY EVER have 1 Request in progress at a time.
        """
        existing_nr = db.session.query(Request). \
            filter(
            Request.userId == userObj.id,
            Request.stateCd == State.INPROGRESS,
            Request.nrNum.notlike('NR L%')). \
            one_or_none()

        return existing_nr

    @classmethod
    def find_name_by_choice(cls, nr_id, choice):
        names = cls.query.filter_by(id=nr_id).first().names
        return names.filter_by(choice=choice).one_or_none()

    @classmethod
    def validNRFormat(cls, nr):
        """NR should be of the format 'NR 1234567'"""
        if len(nr) != 10 or nr[:2] != 'NR' or nr[2:3] != ' ':
            return False

        try:
            num = int(nr[3:])
        except:
            return False

        return True

    # START NEW NAME_REQUEST SERVICE METHODS, WE WILL REFACTOR THESE SHORTLY
    @classmethod
    def get_general_query(cls, change_filter=False, queue=False):
        criteria = []
        basic_filter = [
            cls.id == Name.nrId,
            cls.requestTypeCd.in_([
                                      EntityTypes.PRIVATE_ACT.value,
                                      EntityTypes.CORPORATION.value,
                                      LegacyEntityTypes.CORPORATION.CCR.value,
                                      LegacyEntityTypes.CORPORATION.CT.value,
                                      LegacyEntityTypes.CORPORATION.RCR.value,
                                      EntityTypes.COOPERATIVE.value,
                                      LegacyEntityTypes.COOPERATIVE.CCP.value,
                                      LegacyEntityTypes.COOPERATIVE.CTC.value,
                                      LegacyEntityTypes.COOPERATIVE.RCP.value,
                                      EntityTypes.FINANCIAL_INSTITUTION.value,
                                      LegacyEntityTypes.FINANCIAL_INSTITUTION.CFI.value,
                                      LegacyEntityTypes.FINANCIAL_INSTITUTION.RFI.value,
                                      EntityTypes.SOCIETY.value,
                                      LegacyEntityTypes.SOCIETY.ASO.value,
                                      LegacyEntityTypes.SOCIETY.CSO.value,
                                      LegacyEntityTypes.SOCIETY.CSSO.value,
                                      LegacyEntityTypes.SOCIETY.CTSO.value,
                                      LegacyEntityTypes.SOCIETY.RSO.value,
                                      EntityTypes.UNLIMITED_LIABILITY_COMPANY.value,
                                      LegacyEntityTypes.UNLIMITED_LIABILITY_COMPANY.UC.value,
                                      LegacyEntityTypes.UNLIMITED_LIABILITY_COMPANY.CUL.value,
                                      LegacyEntityTypes.UNLIMITED_LIABILITY_COMPANY.ULCT.value,
                                      LegacyEntityTypes.UNLIMITED_LIABILITY_COMPANY.RUL.value,
                                      EntityTypes.XPRO_SOCIETY.value,
                                      LegacyEntityTypes.XPRO_SOCIETY.XASO.value,
                                      LegacyEntityTypes.XPRO_SOCIETY.XCASO.value,
                                      LegacyEntityTypes.XPRO_SOCIETY.XCSO.value,
                                      LegacyEntityTypes.XPRO_SOCIETY.XRSO.value,
                                      EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value,
                                      LegacyEntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.CC.value,
                                      LegacyEntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.CCV.value,
                                      LegacyEntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.CCCT.value,
                                      LegacyEntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.RCC.value,
                                      EntityTypes.PARISH.value,
                                      EntityTypes.XPRO_CORPORATION.value,
                                      LegacyEntityTypes.XPRO_CORPORATION.XCCR.value,
                                      LegacyEntityTypes.XPRO_CORPORATION.XRCR.value,
                                      LegacyEntityTypes.XPRO_CORPORATION.AS.value,
                                      EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value,
                                      LegacyEntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.UA.value,
                                      LegacyEntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.XCUL.value,
                                      LegacyEntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.XRUL.value,
                                      EntityTypes.XPRO_COOPERATIVE.value,
                                      LegacyEntityTypes.XPRO_COOPERATIVE.XCCP.value,
                                      LegacyEntityTypes.XPRO_COOPERATIVE.XRCP.value,
                                      EntityTypes.BENEFIT_COMPANY.value
                                  ] if not change_filter else [
                EntityTypes.PRIVATE_ACT.value,
                EntityTypes.CORPORATION.value,
                LegacyEntityTypes.CORPORATION.CCR.value,
                LegacyEntityTypes.CORPORATION.RCR.value,
                EntityTypes.COOPERATIVE.value,
                LegacyEntityTypes.COOPERATIVE.CCP.value,
                LegacyEntityTypes.COOPERATIVE.RCP.value,
                EntityTypes.FINANCIAL_INSTITUTION.value,
                LegacyEntityTypes.FINANCIAL_INSTITUTION.CFI.value,
                LegacyEntityTypes.FINANCIAL_INSTITUTION.RFI.value,
                LegacyEntityTypes.SOCIETY.ASO.value,
                LegacyEntityTypes.SOCIETY.CSO.value,
                LegacyEntityTypes.SOCIETY.RSO.value,
                EntityTypes.UNLIMITED_LIABILITY_COMPANY.value,
                LegacyEntityTypes.UNLIMITED_LIABILITY_COMPANY.UC.value,
                LegacyEntityTypes.UNLIMITED_LIABILITY_COMPANY.CUL.value,
                LegacyEntityTypes.UNLIMITED_LIABILITY_COMPANY.RUL.value,
                EntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.value,
                LegacyEntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.CC.value,
                LegacyEntityTypes.COMMUNITY_CONTRIBUTION_COMPANY.RCC.value,
                EntityTypes.PARISH.value,
                EntityTypes.BENEFIT_COMPANY.value
            ]),
        ]

        queue_request_state_filter = [
            cls.stateCd.in_(
                [State.DRAFT, State.HOLD, State.INPROGRESS])
        ]

        corp_request_state_filter = [
            cls.stateCd.in_(
                [State.APPROVED, State.CONDITIONAL, State.COND_RESERVE, State.RESERVED]),
        ]

        name_state_filter = [
            Name.state.in_(
                [NameState.APPROVED.value, NameState.CONDITION.value, NameState.RESERVED.value,
                 NameState.COND_RESERVE.value])
        ]

        not_consumed_filter = [
            cls.expirationDate > func.current_Date(),
            Name.corpNum.is_(None),
            Name.consumptionDate.is_(None)
        ]

        consumed_filter = [
            Name.corpNum.isnot(None),
        ]

        if queue:
            criteria.append(RequestConditionCriteria(
                fields=[Name.name, sqlalchemy.null().label('consumptionDate'), cls.submittedDate,
                        sqlalchemy.null().label('corpNum'), cls.nrNum],
                filters=[basic_filter, queue_request_state_filter]
            ))
        else:
            criteria.append(RequestConditionCriteria(
                fields=[Name.name, Name.consumptionDate, sqlalchemy.null().label('submittedDate'),
                        Name.corpNum,
                        sqlalchemy.null().label('nrNum')],
                filters=[basic_filter, corp_request_state_filter, name_state_filter, consumed_filter]
            ))
            criteria.append(RequestConditionCriteria(
                fields=[Name.name, sqlalchemy.null().label('consumptionDate'), cls.submittedDate,
                        sqlalchemy.null().label('corpNum'), cls.nrNum],
                filters=[basic_filter, corp_request_state_filter, name_state_filter, not_consumed_filter]
            ))

        return criteria

    @classmethod
    def get_waiting_time(cls, unit):
        unit_time = 86400 if unit == UnitTime.DAY.value else 60 * 60 if unit == UnitTime.HR.value else 60
        median_waiting_time = db.session.query(
            func.percentile_cont(0.5).within_group((func.extract('epoch', Event.eventDate) -
                                                    func.extract('epoch', Request.submittedDate)) / unit_time).label(
                'examinationTime')). \
            join(Request, and_(Event.nrId == Request.id)). \
            filter(Event.action == EventAction.PATCH.value,
                   Event.stateCd.in_(
                       [EventState.APPROVED.value, EventState.REJECTED.value,
                        EventState.CONDITIONAL.value, EventState.CANCELLED.value]),
                   Event.userId != EventUserId.SERVICE_ACCOUNT.value,
                   Event.eventDate.cast(Date) >= (func.now() - timedelta(days=1)).cast(Date)
                   )

        return median_waiting_time

    @classmethod
    def get_waiting_time_priority_queue(cls, unit):
        median_waiting_time = cls.get_waiting_time(unit)
        priority_waiting_time = median_waiting_time.filter(Request.priorityCd == RequestPriority.Y.value).all()

        return priority_waiting_time.pop()

    @classmethod
    def get_waiting_time_regular_queue(cls, unit):
        median_waiting_time = cls.get_waiting_time(unit)
        regular_waiting_time = median_waiting_time.filter(Request.priorityCd != RequestPriority.Y.value).all()

        return regular_waiting_time.pop()

    @classmethod
    def get_query_exact_match(cls, criteria, list_name, list_dist, list_desc, end_designation_list,
                              any_designation_list, stop_words):
        name = []
        for word in list_name:
            if word in list_dist:
                name.extend(Request.set_special_characters_distinctive([word]))
            elif word in list_desc:
                name.extend(Request.set_special_characters_descriptive([word]))
            else:
                raise Exception(
                    'Invalid classification for the word {0}. Cannot be included in exact match query.'.format(word))

        criteria = cls.get_designations_in_name(criteria, name, any_designation_list, end_designation_list, stop_words)

        return criteria

    @classmethod
    def get_designations_in_name(cls, criteria, special_characters_name, any_designation_list, end_designation_list,
                                 stop_words_list):
        name_with_designation = cls.include_designations_in_name(special_characters_name, any_designation_list,
                                                                 end_designation_list,
                                                                 stop_words_list)
        for e in criteria:
            e.filters.insert(len(e.filters),
                             [func.lower(Name.name).op('~')(r'{0}'.format(name_with_designation))])

        return criteria

    @classmethod
    def get_any_designation_in_name(cls, criteria, special_characters_name, any_list_designation, stop_words_list):
        name_any_designation = cls.include_any_designation_in_name(special_characters_name, any_list_designation,
                                                                   stop_words_list)
        for e in criteria:
            e.filters.insert(len(e.filters),
                             [func.lower(Name.name).op('~')(r'{0}'.format(name_any_designation))])

        return criteria

    @classmethod
    def get_name_criteria(cls, dist_list, desc_list, list_name):
        name_criteria = ''
        if dist_list:
            substitutions = cls.get_distinctive(dist_list, list_name)
            name_criteria = cls.format_criteria(name_criteria, substitutions, r'^((\w+\s\w+\s+)|\w+\s+)?\y(', r')+\y.*?')
        if desc_list:
            synonyms = cls.get_descriptive(desc_list, list_name)
            name_criteria = cls.format_criteria(name_criteria, synonyms, r'\y(', ')+')

        return name_criteria

    @classmethod
    def insert_name_criteria(cls, criteria, name_criteria):
        for e in criteria:
            e.filters.insert(len(e.filters), [func.lower(Name.name).op('~')(name_criteria)])

        return criteria

    @classmethod
    def format_criteria(cls, criteria, substitutions, prefix, suffix):
        if substitutions:
            substitutions = substitutions[:-1] if substitutions[-1] == '|' else substitutions
            dist_criteria = prefix + substitutions + suffix
            criteria += dist_criteria
        return criteria

    def find_by_criteria_array(cls, criteria_arr=None, queue=False):
        queries = []
        for criteria in criteria_arr:
            RequestConditionCriteria.is_valid_criteria(criteria)
            filters_all = []
            for filter_group in criteria.filters:
                for element in filter_group:
                    filters_all.append(element)
            queries.append(cls.query.with_entities(*criteria.fields).filter(and_(*filters_all)))

        if queue:
            query_all = queries[0]
        else:
            query_all = queries[0].union(queries[1])

        print(query_all.statement)
        return query_all.all()

    @classmethod
    def find_by_criteria(cls, criteria=None, limit=10):
        RequestConditionCriteria.is_valid_criteria(criteria)

        query = cls.query
        if len(criteria.fields) > 0:
            query = query.with_entities(*criteria.fields)

        query = query.filter(and_(*criteria.filters))
        query = query.limit(limit)

        # Dump the query
        # TODO: Make a util for this!
        # TODO: Only log if LOCAL_DEV_MODE / DEBUG conf exists
        # query_str = '\n' + str(query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        # current_app.logger.debug(query_str)

        return query.all()

    @classmethod
    def set_special_characters_distinctive(cls, list_d):
        list_special_characters = []
        for element in list_d:
            list_special_characters.append(
                r'\W*'.join(element[i:i + 1] + element[i:i + 1] + r'?' for i in range(0, len(element), 1)) + r'(?:es|[a-z])?')

        return list_special_characters

    @classmethod
    def set_special_characters_descriptive(cls, list_d):
        list_special_characters = []
        for element in list_d:
            list_special_characters.append(r'\W*'.join(element[i:i + 1] for i in range(0, len(element), 1)))

        return list_special_characters

    @classmethod
    def get_distinctive(cls, dist_list, list_name):
        substitutions = ''
        for i, word in enumerate(list_name):
            for j, dist_sublist in enumerate(dist_list):
                if word in dist_sublist:
                    special_characters_dist = Request.set_special_characters_distinctive(dist_sublist)
                    substitutions += '(' + '|'.join(map(str, special_characters_dist)) + ')|'
                    dist_list.pop(j)
                    break
        return substitutions

    @classmethod
    def get_descriptive(cls, desc_list, list_name):
        synonyms = ''
        for i, word in enumerate(list_name):
            for j, desc_sublist in enumerate(desc_list):
                if word.replace(" ", "") in desc_sublist:
                    special_characters_descriptive = Request.set_special_characters_descriptive(desc_sublist)
                    synonyms += ' ?|'.join(map(str, special_characters_descriptive)) + ' ?|'
                    desc_list.pop(j)
                    break

        return synonyms

    @classmethod
    def include_designations_in_name(cls, special_characters_name, any_designation_list, end_designation_list,
                                     stop_words_list):
        any_designation_alternators = '|'.join(map(re.escape, any_designation_list))
        end_designation_alternators = '|'.join(map(re.escape, end_designation_list))
        stop_words_alternators = '|'.join(map(re.escape, stop_words_list))

        name = r'\W*({0})?\W*({1})?\W*'.format(any_designation_alternators, stop_words_alternators).join(
            map(str, special_characters_name))

        full_name = r'^\d*\W*({0})?\W*({1})?\W*'.format(any_designation_alternators, stop_words_alternators) + name + \
                    r'\W*({0})?\W*({1})?$'.format(any_designation_alternators, end_designation_alternators)
        return full_name


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
        fields = (
            'additionalInfo',
            'consentFlag',
            'consent_dt',
            'corpNum',
            'expirationDate',
            'furnished',
            'hasBeenReset',
            'id',
            'natureBusinessInfo',
            'nrNum',
            'nroLastUpdate',
            'priorityCd',
            'requestTypeCd',
            'stateCd',
            'previousStateCd',
            'submitCount',
            'submittedDate',
            'xproJurisdiction',
        )


class RequestsSearchSchema(ma.ModelSchema):
    class Meta:
        model = Request
        # sqla_session = db.scoped_session
        # additional = ['stateCd']
        fields = (
            'additionalInfo',
            'comments',
            'consentFlag',
            'consent_dt',
            'corpNum',
            'expirationDate',
            'furnished',
            'lastUpdate',
            'natureBusinessInfo',
            'nrNum',
            'nroLastUpdate',
            'priorityCd',
            'priorityDate',
            'requestTypeCd',
            'stateCd',
            'submitCount',
            'submittedDate',
            'xproJurisdiction',
            'names',
            'activeUser'
        )

    names = ma.Nested(NameSchema, many=True)
    activeUser = ma.Nested(UserSchema, many=False, only='username')
    comments = ma.Nested(CommentSchema, many=True, only=['comment', 'examiner', 'timestamp'])
