
from . import db


# The class that corresponds to the database table for synonyms.
class Synonym(db.Model):
    __tablename__ = "synonym"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(100))
    synonyms_text = db.Column(db.String(1000), unique=True, nullable=False)
    comment = db.Column(db.String(1000))
    enabled = db.Column(db.Boolean(), default=True)
