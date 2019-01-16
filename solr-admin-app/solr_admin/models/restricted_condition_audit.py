
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
    username = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
    action = db.Column(db.String(10))
    cnd_id = db.Column(db.Integer)
    consenting_body = db.Column(db.VARCHAR(195))
    words = db.Column(db.VARCHAR(1000))
    cnd_text = db.Column(db.String(1000))
    instructions = db.Column(db.VARCHAR(1000))
    consent_required = db.Column(db.Boolean(), default=True)
    allow_use = db.Column(db.Boolean(), default=True)

    def __init__(
            self, username: str, action: str, cnd_id: int, cnd_text: str, words: str,
            consent_required: bool, consenting_body: str, instructions: str, allow_use: bool ) -> None:
        self.username = username
        self.timestamp = datetime.datetime.now()
        self.action = action
        self.cnd_id = cnd_id
        self.cnd_text = cnd_text
        self.words = words
        self.consent_required = consent_required
        self.consenting_body = consenting_body
        self.instructions = instructions
        self.allow_use = allow_use




