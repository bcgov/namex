
from . import db

# The class that corresponds to the database table for restricted words.
class RestrictedWord(db.Model):
    __tablename__ = 'restricted_word'

    word_id = db.Column(db.Integer, primary_key=True)
    word_phrase = db.Column(db.VARCHAR(60))


