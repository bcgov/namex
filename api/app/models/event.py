"""Events keep an audit trail of all changes submitted to the datastore

"""
from . import db
from app.exceptions import BusinessException
from marshmallow import Schema, fields, post_load
from datetime import datetime
from .request import Request
from sqlalchemy.orm import backref
import bz2


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    eventDate = db.Column('event_dt', db.DateTime, default=datetime.utcnow)
    action = db.Column(db.String(1000))
    jsonZip = db.Column('json_zip', db.LargeBinary)

    # relationships
    stateCd = db.Column('state_cd', db.String(20),  db.ForeignKey('states.cd'))
    state = db.relationship('State', backref=backref('state_events', uselist=False), foreign_keys=[stateCd])
    nrId = db.Column('nr_id', db.Integer, db.ForeignKey('requests.id'))
    request = db.relationship('Request', backref=backref('request_events', uselist=False), foreign_keys=[nrId])
    userId = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=backref('user_events', uselist=False), foreign_keys=[userId])

    def __init__(self, action, jsonData):
        self.action = action
        self.jsonZip = bz2.compress(jsonData)

    def json(self):
        return {"eventDate": self.eventDate, "action": self.action, "jsonData": bz2.decompress(self.jsonZip),
                "requestId": self.nrId, "userId": self.userId }

    def save_to_db(self):
        db.session.add(self)

    def delete_from_db(self):
        raise BusinessException()
