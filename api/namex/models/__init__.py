"""Models for the business objects in the application
   This is picked up by the DB management system to maintain tables, etc.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from flask_marshmallow import Marshmallow

ma = Marshmallow()

from marshmallow.exceptions import ValidationError

from .applicant import Applicant, ApplicantSchema
from .comment import Comment, CommentSchema, NameCommentSchema
from .state import State, StateSchema
from .event import Event
from .nwpta import PartnerNameSystem, PartnerNameSystemSchema
from .name import Name, NameSchema
from .request import Request, RequestsSchema, RequestsHeaderSchema, RequestsSearchSchema
from .user import User, UserSchema

from .decision_reason import DecisionReason
from .admin_tables import DecisionReasonAudit, RestrictedConditionAudit
from .word_classification import WordClassification, WordClassificationSchema
from .virtual_word_condition import VirtualWordCondition
from .nr_number import NRNumber
from .nr_number_exclude import NRNumberExclude
from .nr_number_lifespan import NRNumberLifespan
from .payment import Payment
from .hotjar_tracking import HotjarTracking
