
from . import db


# The class that corresponds to the database view between restricted words and restricted conditions.
class RestrictedView(db.Model):
    __tablename__ = 'restricted_view'

    word_phrase = db.Column(db.VARCHAR(60))
    cnd_text = db.Column(db.VARCHAR(1000))
    consent_required = db.Column(db.VARCHAR(1))
    consenting_body = db.Column(db.VARCHAR(195))
    instructions = db.Column(db.VARCHAR(1000))
    allow_use = db.Column(db.VARCHAR(1))
    word_id = db.Column(db.Integer,primary_key=True)
    cnd_id = db.Column(db.Integer,primary_key=True)


