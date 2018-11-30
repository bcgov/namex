
from . import db


# The class that corresponds to the database link table between restricted words and restricted conditions.
class RestrictedLinkWordCondition(db.Model):
    __tablename__ = 'restricted_link_word_condition'

    link_id = db.Column(db.Integer, primary_key=True)
    cnd_id = db.Column(db.Integer)
    word_id = db.Column(db.Integer)

    # keep the unique constraint so that they can be used as a primary key if need be
    __table_args__ = (
        db.UniqueConstraint("cnd_id", "word_id"),
    )