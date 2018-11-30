
import datetime

from . import db


def _to_string(string):
    if string is None:
        return ''

    return string

# The class that corresponds to the database table for restricted condition audits.
class RestrictedConditionAudit(db.Model):
    __tablename__ = 'restricted_condition_audit'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime)
    username = db.Column(db.String(100))
    action = db.Column(db.String(10))
    cnd_id = db.Column(db.Integer)
    cnd_text = db.Column(db.String(1000))
    consent_required = db.Column(db.VARCHAR(1))
    consenting_body = db.Column(db.VARCHAR(195))
    instructions = db.Column(db.VARCHAR(1000))
    allow_use = db.Column(db.VARCHAR(1))

    def __init__(
            self, username: str, action: str, cnd_id: int, cnd_text: str,
            consent_required: str, consenting_body: str, instructions: str, allow_use: str ) -> None:
        self.timestamp = datetime.datetime.now()
        self.username = username
        self.action = action
        self.cnd_id = cnd_id
        self.cnd_text = cnd_text
        self.consent_required = consent_required
        self.consenting_body = consenting_body
        self.instructions = instructions
        self.allow_use = allow_use




