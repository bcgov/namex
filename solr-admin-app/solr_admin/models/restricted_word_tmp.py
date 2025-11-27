
from . import db


# The class that corresponds to the database table for restricted words.
class RestrictedWordTmp(db.Model):
    __tablename__ = 'restricted_word_tmp'

    word_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word_phrase = db.Column(db.VARCHAR(60))
