
import datetime

from . import db

def _to_string(string):
    if string is None:
        return ''

    return string

# The class that corresponds to the database table for restricted word audits.
class RestrictedWordAudit(db.Model):
    __tablename__ = 'restricted_word_audit'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime)
    word_id = db.Column(db.Integer)
    word_phrase = db.Column(db.VARCHAR(60))
    username = db.Column(db.String(100))
    action = db.Column(db.String(10))


    def __init__(
            self, username: str, action: str, word_id: int, word_phrase: str
        ) -> None:
        self.timestamp = datetime.datetime.now()
        self.word_id = word_id
        self.word_phrase = word_phrase
        self.username = username
        self.action = action








