
import datetime

from . import db


def _to_string(string):
    if string is None:
        return ''

    return string

# The class that corresponds to the database table for decision reasons audits.
class DecisionReasonAudit(db.Model):
    __tablename__ = 'decision_reason_audit'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100))
<<<<<<< HEAD
<<<<<<< HEAD
    timestamp = db.Column(db.DateTime)
=======
    timestamp = db.Column('timestamp', db.DateTime(timezone=True))
>>>>>>> f72389dbba58d781274777c0e9a40a538a58806f
=======
    timestamp = db.Column('timestamp', db.DateTime(timezone=True))
>>>>>>> eaa64fc879dc34071e45a2ca9ab67747a387106d
    action = db.Column(db.String(10))
    dr_id = db.Column(db.Integer)
    name = db.Column(db.VARCHAR(1024))
    reason = db.Column(db.VARCHAR(1024))

    def __init__(
            self, username: str, action: str, id: str,
            name: str, reason: str ) -> None:
        self.username = username
        self.timestamp = datetime.datetime.now()
        self.action = action
        self.dr_id = id
        self.name = name
        self.reason = reason



