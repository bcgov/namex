from . import db


# The class that corresponds to the database table for restricted words.
class RestrictedWordCondition(db.Model):
    __tablename__ = 'restricted_word_condition'

    cnd_id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, primary_key=True)
