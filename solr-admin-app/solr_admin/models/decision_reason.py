
from . import db

# The class that corresponds to the database table for restricted words.
class DecisionReason(db.Model):
    __tablename__ = 'decision_reason2'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(1024))
    reason = db.Column(db.VARCHAR(1024))


