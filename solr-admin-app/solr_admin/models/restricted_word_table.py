
from . import db
from solr_admin.models.restricted_condition import RestrictedCondition2


# The class that corresponds to the database table for restricted words.
class RestrictedWordTable(db.Model):
    __tablename__ = 'restricted_word'

    word_id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.VARCHAR(60))
    cnd_id = db.Column(db.Integer)
