
from . import db

# The class that corresponds to the database table for restricted conditions.
class RestrictedConditionTmp(db.Model):
    __tablename__ = 'restricted_condition_tmp'

    cnd_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cnd_text = db.Column(db.VARCHAR(1000))
    allow_use = db.Column(db.VARCHAR(1))
    consent_required = db.Column(db.VARCHAR(1))
    consenting_body = db.Column(db.VARCHAR(195))
    instructions = db.Column(db.VARCHAR(1000))


