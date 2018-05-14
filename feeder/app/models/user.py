from app import db
from datetime import datetime


# noinspection SpellCheckingInspection
class User(db.Model):
    __bind_key__ = None
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000), unique=True)
    firstname = db.Column(db.String(1000))
    lastname = db.Column(db.String(1000))
    sub = db.Column(db.String(36), default='DRAFT')
    iss = db.Column(db.String(1024))
    creationDate = db.Column(db.DateTime, default=datetime.utcnow)

    requests = db.relationship('Request', lazy='dynamic')

    def __init__(self, username, firstname, lastname, sub, iss):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.sub = sub
        self.iss = iss

    def json(self):
        return {"username": self.username, "firstname": self.firstname, "lastname": self.lastname,
                "sub": self.sub, "iss": self.iss}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).one()
