
from . import db


# The class that corresponds to the database table for synonyms.
class Synonym(db.Model):
    __tablename__ = 'synonym'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(100))
    synonyms_text = db.Column(db.String(1000), unique=True, nullable=False)
    comment = db.Column(db.String(1000))
    enabled = db.Column(db.Boolean(), default=True)

    @classmethod
    def find(cls, term):
        rows = cls.query.filter(Synonym.synonyms_text.ilike('%' + term + '%')).all()

        # We're matching in a comma-separated list of terms, which means that a search for "art" will match "martial".
        # Split synonyms into their components and then match exactly on those.
        synonyms_list = []
        for row in rows:
            synonyms = [synonym.strip() for synonym in row.synonyms_text.split(',')]
            if term in synonyms:
                synonyms_list.append(row)

        return synonyms_list
