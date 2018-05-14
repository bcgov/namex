"""Events keep an audit trail of all changes submitted to the datastore

"""
from app import db
from datetime import datetime
import bz2


class Event(db.Model):
    __bind_key__ = None
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    eventDate = db.Column('event_dt', db.DateTime, default=datetime.utcnow)
    action = db.Column(db.String(1000))
    jsonZip = db.Column('json_zip', db.String(4096))

    # relationships
    nrId = db.Column('nr_id', db.Integer, db.ForeignKey('requests.id'))
    request = db.relationship('Request')
    userId = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    def __init__(self, action, jsonData):
        self.action = action
        self.jsonZip = bz2.compress(jsonData)

    def json(self):
        return {"eventDate": self.eventDate, "action": self.action, "jsonData": bz2.decompress(self.jsonZip),
                "requestId": self.nrId, "userId": self.userId}

