from . import db, ma
from flask import current_app
from marshmallow import Schema, fields, post_load
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000), index=True)
    firstname = db.Column(db.String(1000))
    lastname = db.Column(db.String(1000))
    sub = db.Column(db.String(36), unique=True)
    iss = db.Column(db.String(1024))
    creationDate = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    APPROVER='names_approver'
    EDITOR='names_editor'
    VIEWONLY='names_viewer'
    SYSTEM='system'

    def __init__(self, username, firstname, lastname, sub, iss ):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.sub = sub
        self.iss = iss

    def json(self):
        return {"username": self.username, "firstname": self.firstname, "lastname": self.lastname,
                "sub": self.sub, "iss": self.iss }

    @classmethod
    def find_by_jwtToken(cls, token):
        return cls.query.filter_by(sub=token['sub']).one_or_none()

    @classmethod
    def create_from_jwtToken(cls, token):
        if token:
            # TODO: schema doesn't parse from token need to figure that out ... LATER!
            # s = KeycloakUserSchema()
            # u = s.load(data=token, partial=True)
            user = User(
                # username = token.get('username', None),
                username = token.get('preferred_username', None),
                firstname = token.get('given_name', None),
                lastname = token.get('family_name', None),
                iss = token['iss'],
                sub = token['sub']
            )
            current_app.logger.debug('Creating user from JWT:{}; User:{}'.format(token, user))
            db.session.add(user)
            db.session.commit()
            return user
        return None

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).order_by(User.creationDate.desc()).first()

    @classmethod
    def find_by_sub(cls, sub):
        return cls.query.filter_by(sub=sub).one_or_none()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        pass
        return
        # need to intercept the ORM and stop Users from being deleted
        # db.session.delete(self)
        # db.session.commit()

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

    # id = fields.Int(dump_only=False)
    # username = fields.String()
    # firstname = fields.String()
    # lastname = fields.String()
    # sub = fields.String()
    # iss = fields.String()
    # creationDate = fields.DateTime()

    #     We use make_object to create a new User from validated data
    # @post_load
    # def make_object(self, data):
    #     if not data:
    #         return None
    #     return User(username=data['username'],
    #                 firstname=data['firstname'],
    #                 lastname=data['lastname'],
    #                 sub=data['sub'],
    #                 iss=data['iss'])


# class KeycloakUserSchema(Schema):
#     id = fields.Int(dump_only=True)
#     username = fields.String(attribute="username")
#     firstname = fields.String(attribute="given_name")
#     lastname = fields.String(attribute="family_name")
#     sub = fields.String(attribute="sub")
#     iss = fields.String(attribute="iss")
#     creationDate = fields.DateTime(dump_only=True)
#
