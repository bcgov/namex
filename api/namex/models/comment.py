from . import db, ma
from datetime import datetime
from sqlalchemy.orm import backref
from .user import User, UserSchema


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(4096))
    timestamp = db.Column('timestamp', db.DateTime(timezone=True), default=datetime.utcnow)

    # parent keys
    nrId = db.Column('nr_id', db.Integer, db.ForeignKey('requests.id'), index=True)
    examinerId = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), index=True)

    # Relationships - Users
    examiner = db.relationship('User', backref=backref('examiner_comments'), foreign_keys=[examinerId])

    # NRComments = db.relationship('Request', backref=backref("comments", uselist=False), foreign_keys=[nrId])

    def as_dict(self):
        return {
            'id': self.id,
            'examiner': 'unknown' if (self.examiner is None) else self.examiner.username,
            'comment': self.comment,
            'timestamp': self.timestamp.isoformat(),
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        pass


class CommentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Comment
        fields = ('comment', 'timestamp', 'examiner', 'id')

    examiner = ma.Nested(UserSchema, many=False, only=('username',))


class NameCommentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Comment
        fields = ('comment',)
