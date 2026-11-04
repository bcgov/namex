
import datetime

from . import db


def _to_string(string):
    if string is None:
        return ''

    return string

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
            self, username: str, action: str, synonym_id: int, category: str, synonyms_text: str, comment: str,
            enabled: bool) -> None:
        self.username = username
        self.timestamp = datetime.datetime.now()
        self.action = action
        self.synonym_id = synonym_id
        self.category = _to_string(category)
        self.synonyms_text = synonyms_text
        self.comment = _to_string(comment)
        self.enabled = enabled
