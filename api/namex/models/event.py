"""Events keep an audit trail of all changes submitted to the datastore

"""
from sqlalchemy import and_, func

from . import db
from namex.exceptions import BusinessException
from marshmallow import Schema, fields, post_load
from datetime import datetime
from .request import Request
from sqlalchemy.orm import backref
from sqlalchemy import cast, Date
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, timedelta

from ..constants import EventAction, EventUserId, EventState, RequestState, RequestPriority


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    eventDate = db.Column('event_dt', db.DateTime(timezone=True), default=datetime.utcnow)
    action = db.Column(db.String(1000))
    jsonZip = db.Column('json_zip', db.Text)
    eventJson = db.Column('event_json', JSONB)

    # relationships
    stateCd = db.Column('state_cd', db.String(20), db.ForeignKey('states.cd'))
    state = db.relationship('State', backref=backref('state_events', uselist=False), foreign_keys=[stateCd])
    nrId = db.Column('nr_id', db.Integer, db.ForeignKey('requests.id'))
    request = db.relationship('Request', backref=backref('request_events', uselist=False), foreign_keys=[nrId])
    userId = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=backref('user_events', uselist=False), foreign_keys=[userId])

    GET = 'get'
    PUT = 'put'
    PATCH = 'patch'
    POST = 'post'
    DELETE = 'DELETE'
    UPDATE_FROM_NRO = 'update_from_nro'
    NRO_UPDATE = 'nro_update'
    MARKED_ON_HOLD = 'marked_on_hold'

    VALID_ACTIONS = [GET, PUT, PATCH, POST, DELETE]

    def json(self):
        return {"id": self.id, "eventDate": self.eventDate, "action": self.action, "stateCd": self.stateCd,
                "jsonData": self.eventJson,
                "requestId": self.nrId, "userId": self.userId}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_to_session(self):
        db.session.add(self)

    def delete_from_db(self):
        raise BusinessException()

    @classmethod
    def get_approved_names_counter(cls):
        auto_approved_names_counter = db.session.query(
            func.count(Event.id)).filter(Event.action == EventAction.PUT.value,
                                         Event.userId == EventUserId.SERVICE_ACCOUNT.value,
                                         Event.stateCd == EventState.APPROVED.value,
                                         func.date_trunc('day', Event.eventDate) == func.date_trunc('day', func.now())
                                         ).all()
        return auto_approved_names_counter

    @classmethod
    def get_avg_examination_time_secs(cls):
        avg_examination_time = db.session.query(
            func.percentile_cont(0.5).within_group((func.extract('epoch', Event.eventDate) -
                                                    func.extract('epoch', Request.submittedDate)))). \
            join(Request, and_(Event.nrId == Request.id)). \
            filter(Event.action == EventAction.PATCH.value,
                   Event.stateCd.in_(
                       [EventState.APPROVED.value, EventState.REJECTED.value,
                        EventState.CONDITIONAL.value, EventState.CANCELLED.value]),
                   Event.eventDate.cast(Date) == (func.now() - timedelta(days=1)).cast(Date)
                   ).all()

        return avg_examination_time
