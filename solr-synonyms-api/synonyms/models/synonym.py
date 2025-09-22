from flask import current_app
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import and_

from synonyms.criteria.synonym.query_criteria import SynonymQueryCriteria

from . import db

"""
- Models NEVER implement business logic, ONLY generic queries belong in here.
- Methods like find, find_one, or find_by_criteria belong in models.
- Methods like get_synonym_list or get_en_designation_end_all_list belong in a Service!
    - They belong in a Service because getting eg. a list of designations or synonyms is a USE case of the model,
      but getting a list of designations is not necessarily something that is inherent to the model; rather, that is
      what a particular user of the model wants to query for.
"""


# The class that corresponds to the database table for synonyms.
class Synonym(db.Model):
    __tablename__ = "synonym"
    # TODO: What's the deal with this bind key?
    # __bind_key__ = 'synonyms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(100))
    synonyms_text = db.Column(db.String(1000), unique=True, nullable=False)
    stems_text = db.Column(db.String(1000), nullable=False)
    comment = db.Column(db.String(1000))
    enabled = db.Column(db.Boolean(), default=True)

    def json(self):
        return {"id": self.id, "category": self.category, "synonymsText": self.synonyms_text,
                "stemsText": self.stems_text, "comment": self.comment, "enabled": self.enabled}

    """
    Find a term by column.
    """
    @classmethod
    def find(cls, term, col):
        current_app.logger.debug("finding {} for {}".format(col, term))
        synonyms_list = []
        term = term.lower()
        if col == "synonyms_text":
            rows = cls.query.filter(Synonym.synonyms_text.ilike("%" + term + "%")).all()
            for row in rows:
                synonyms = [synonym.strip().lower() for synonym in row.synonyms_text.split(",")]
                if term in synonyms:
                    synonyms_list.append(row)
        # col == stems_text
        else:
            rows = cls.query.filter(Synonym.stems_text.ilike("%" + term + "%")).all()
            for row in rows:
                synonyms = [synonym.strip().lower() for synonym in row.stems_text.split(",")]
                if term in synonyms:
                    synonyms_list.append(row)

        return synonyms_list

    r"""
    Query the model collection using an array of filters
    @:param filters An array of query filters eg. 
                    [
                      func.lower(model.category).op('~')(r'\y{}\y'.format('sub')),
                      func.lower(model.category).op('~')(r'\y{}\y'.format('prefix(es)?'))
                    ]
    """
    @classmethod
    def find_by_criteria(cls, criteria=None):
        SynonymQueryCriteria.is_valid_criteria(criteria)

        query = cls.query.with_entities(*criteria.fields) \
            .filter(and_(*criteria.filters))

        return query.all()


class SynonymSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Synonym
