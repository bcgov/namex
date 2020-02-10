from . import db, ma


class Synonym(db.Model):
    __tablename__ = 'synonym'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column('category', db.String(100), default='NONE', nullable=False, index=True)
    synonymsText = db.Column('synonyms_text', db.String(1000), nullable=False, index=True)
    stemsText = db.Column('stems_text', db.String(1000))
    comment = db.Column('comment', db.String(1000))
    enabled = db.Column('enabled', db.Boolean, nullable=False, index=True)

    def json(self):
        return {
            "id": self.id,
            "category": self.category,
            "synonymsText": self.synonymsText,
            "stemsText": self.stemsText,
            "comment": self.comment,
            "enabled": self.enabled
        }

    @classmethod
    def find_by_category(cls, category):
        return cls.query.filter(category=category).filter(cls.enabled is True).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_to_session(self):
        db.session.add(self)


class SynonymSchema(ma.ModelSchema):
    class Meta:
        model = Synonym
