
import datetime

from . import db

def _to_string(string):
    if string is None:
        return ''

    return string

# The class that corresponds to the database link table between restricted words and restricted conditions audits.
class RestrictedLinkWordConditionAudit(db.Model):
    __tablename__ = 'restricted_link_word_condition_audit'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime)
    username = db.Column(db.String(100))
    action = db.Column(db.String(10))
    link_id = db.Column(db.Integer)
    cnd_id = db.Column(db.Integer)
    word_id = db.Column(db.Integer)

    def __init__(
            self, username: str, action: str, link_id: str,
            cnd_id: str, word_id: str ) -> None:
        self.timestamp = datetime.datetime.now()
        self.username = username
        self.action = action
        self.link_id = link_id
        self.cnd_id = cnd_id
        self.word_id = word_id




