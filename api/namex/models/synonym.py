from . import db, ma

# The class that corresponds to the database table for synonyms.
class Synonym(db.Model):
    __tablename__ = 'synonym'
    __bind_key__ = 'synonyms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(100))
    synonyms_text = db.Column(db.String(1000), unique=True, nullable=False)
    stems_text = db.Column(db.String(1000),nullable=False)
    comment = db.Column(db.String(1000))
    enabled = db.Column(db.Boolean(), default=True)

    def json(self):
        return {"id": self.id, "category": self.category, "synonymsText": self.synonyms_text,
                "stemsText": self.stems_text, "comment":self.comment, "enabled": self.enabled}

    @classmethod
    def find(cls, term, col):
        print('finding {} for {}'.format(col, term))
        synonyms_list = []
        term = term.lower()
        if col == 'synonyms_text':
            rows = cls.query.filter(Synonym.synonyms_text.ilike('%' + term + '%')).all()
            for row in rows:
                synonyms = [synonym.strip().lower() for synonym in row.synonyms_text.split(',')]
                if term in synonyms:
                    synonyms_list.append(row)
        # col == stems_text
        else:
            rows = cls.query.filter(Synonym.stems_text.ilike('%' + term + '%')).all()
            for row in rows:
                synonyms = [synonym.strip().lower() for synonym in row.stems_text.split(',')]
                if term in synonyms:
                    synonyms_list.append(row)

        return synonyms_list


class SynonymSchema(ma.ModelSchema):
    class Meta:
        model = Synonym