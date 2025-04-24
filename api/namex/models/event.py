"""Events keep an audit trail of all changes submitted to the datastore"""

from sqlalchemy import and_, func

from . import db
from namex.exceptions import BusinessException
from marshmallow import Schema, fields, post_load
from datetime import datetime
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
    nrId = db.Column('nr_id', db.Integer, db.ForeignKey('requests.id'), index=True)
    userId = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=backref('user_events', uselist=False), foreign_keys=[userId])

    GET = 'get'
    PUT = 'put'
    PATCH = 'patch'
    POST = 'post'
    DELETE = 'DELETE'
    UPDATE_FROM_NRO = 'update_from_nro'
    NRO_UPDATE = 'nro_update'
    NR_DAY_JOB = 'nr_day_job'
    MARKED_ON_HOLD = 'marked_on_hold'
    SET_TO_DRAFT = 'set_to_draft'
    NAMEX_PAY = 'namex_pay'

    VALID_ACTIONS = [GET, PUT, PATCH, POST, DELETE]

    def json(self):
        return {
            'id': self.id,
            'eventDate': self.eventDate,
            'action': self.action,
            'stateCd': self.stateCd,
            'jsonData': self.eventJson,
            'requestId': self.nrId,
            'userId': self.userId,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_to_session(self):
        db.session.add(self)

    def delete_from_db(self):
        raise BusinessException()

    @classmethod
    def get_approved_names_counter(cls):
        auto_approved_names_counter = (
            db.session.query(func.count(Event.id).label('approvedNamesCounter'))
            .filter(Event.action == Event.PATCH + 'Payment Completed')
            .filter(Event.userId == EventUserId.SERVICE_ACCOUNT.value)
            .filter(Event.stateCd.in_(('APPROVED', 'CONDITIONAL')))
            .filter(func.date_trunc('day', Event.eventDate) == func.date_trunc('day', func.now()))
            .all()
        )
        return auto_approved_names_counter.pop()
