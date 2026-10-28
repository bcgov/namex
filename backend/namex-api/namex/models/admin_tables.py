import datetime

from . import db


def _to_string(string):
    if string is None:
        return ''

    return string


"""
@deprecated
"""

"""
class VirtualWordCondition(db.Model):
    __tablename__ = 'virtual_word_condition'

    id = Column(db.Integer, primary_key=True, autoincrement=True)

    rc_consenting_body = Column(db.VARCHAR(195))
    rc_words = Column(db.VARCHAR(1000))
    rc_condition_text = Column(db.VARCHAR(1000))
    rc_instructions = Column(db.VARCHAR(1000))
    rc_consent_required = db.Column(db.Boolean(), default=False)
    rc_allow_use = db.Column(db.Boolean(), default=True)
"""


# The class that corresponds to the database table for decision reasons audits.
class DecisionReasonAudit(db.Model):
    __tablename__ = 'decision_reason_audit'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100))
    timestamp = db.Column('timestamp', db.DateTime(timezone=True))
    action = db.Column(db.String(10))
    dr_id = db.Column(db.Integer)
    name = db.Column(db.VARCHAR(1024))
    reason = db.Column(db.VARCHAR(1024))

    def __init__(self, username: str, action: str, id: str, name: str, reason: str) -> None:
        self.username = username
        self.timestamp = datetime.datetime.now()
        self.action = action
        self.dr_id = id
        self.name = name
        self.reason = reason


# The class that corresponds to the database table for restricted condition audits.
class RestrictedConditionAudit(db.Model):
    __tablename__ = 'restricted_condition_audit'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100))
    timestamp = db.Column('timestamp', db.DateTime(timezone=True))
    action = db.Column(db.String(10))
    cnd_id = db.Column(db.Integer)
    consenting_body = db.Column(db.VARCHAR(195))
    words = db.Column(db.VARCHAR(1000))
    cnd_text = db.Column(db.String(1000))
    instructions = db.Column(db.VARCHAR(1000))
    consent_required = db.Column(db.Boolean(), default=True)
    allow_use = db.Column(db.Boolean(), default=True)

    def __init__(
        self,
        username: str,
        action: str,
        cnd_id: int,
        cnd_text: str,
        words: str,
        consent_required: bool,
        consenting_body: str,
        instructions: str,
        allow_use: bool,
    ) -> None:
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


# The class that corresponds to the database table for synonym audits.
class SynonymAudit(db.Model):
    __tablename__ = 'synonym_audit'
    __bind_key__ = 'synonyms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
    action = db.Column(db.String(10))
    synonym_id = db.Column(db.Integer)
    category = db.Column(db.String(100))
    synonyms_text = db.Column(db.String(1000))
    comment = db.Column(db.String(1000))
    enabled = db.Column(db.Boolean())

    def __init__(
        self,
        username: str,
        action: str,
        synonym_id: int,
        category: str,
        synonyms_text: str,
        comment: str,
        enabled: bool,
    ) -> None:
        self.username = username
        self.timestamp = datetime.datetime.now()
        self.action = action
        self.synonym_id = synonym_id
        self.category = _to_string(category)
        self.synonyms_text = synonyms_text
        self.comment = _to_string(comment)
        self.enabled = enabled
