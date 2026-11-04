"""List of decision/rejection reasons for front end UI."""

from . import db, ma


class DecisionReason(db.Model):
    __tablename__ = 'decision_reason'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024))
    reason = db.Column(db.String(1024))

    def json(self):
        return {'id': self.id, 'name': self.name, 'reason': self.reason}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class DecisionReasonSchema(ma.SQLAlchemySchema):
    class Meta:
        model = DecisionReason
        # fields = ('choice', 'name', 'state')
