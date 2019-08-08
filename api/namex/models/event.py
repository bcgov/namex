"""Events keep an audit trail of all changes submitted to the datastore

"""
from . import db
from namex.exceptions import BusinessException
from marshmallow import Schema, fields, post_load
from datetime import datetime
from .request import Request
from sqlalchemy.orm import backref
from sqlalchemy.dialects.postgresql import JSONB



class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    eventDate = db.Column('event_dt', db.DateTime(timezone=True), default=datetime.utcnow)
    action = db.Column(db.String(1000))
    jsonZip = db.Column('json_zip', db.LargeBinary)
    eventJson =  db.Column('event_json', JSONB)

    # relationships
    stateCd = db.Column('state_cd', db.String(20),  db.ForeignKey('states.cd'))
    state = db.relationship('State', backref=backref('state_events', uselist=False), foreign_keys=[stateCd])
    nrId = db.Column('nr_id', db.Integer, db.ForeignKey('requests.id'))
    request = db.relationship('Request', backref=backref('request_events', uselist=False), foreign_keys=[nrId])
    userId = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=backref('user_events', uselist=False), foreign_keys=[userId])

    GET = 'get'
    PUT='put'
    PATCH='patch'
    POST='post'
    DELETE='DELETE'
    UPDATE_FROM_NRO = 'update_from_nro'
    NRO_UPDATE = 'nro_update'
    MARKED_ON_HOLD= 'marked_on_hold'

    VALID_ACTIONS=[GET, PUT, PATCH, POST, DELETE]

    def json(self):
        return {"eventDate": self.eventDate, "action": self.action, "jsonData": self.eventJson,
                "requestId": self.nrId, "userId": self.userId }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_to_session(self):
        db.session.add(self)

    def delete_from_db(self):
        raise BusinessException()
