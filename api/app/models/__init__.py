"""Models for the business objects in the application
   This is picked up by the DB management system to maintain tables, etc.
"""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask_marshmallow import Marshmallow
ma = Marshmallow()


from .applicant import Applicant, ApplicantSchema
from .comment import Comment, CommentSchema
from .event import Event
from .nwpta import PartnerNameSystem, PartnerNameSystemSchema
from .name import Name, NameSchema
from .request import Request, RequestsSchema, RequestsHeaderSchema
from .user import User, UserSchema
from .state import State, StateSchema
from .decision_reason import DecisionReason
