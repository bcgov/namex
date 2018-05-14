"""Models for the business objects in the application
   This is picked up by the DB management system to maintain tables, etc.
"""
from .name import Name, NameSchema
from .request import Request, RequestsSchema
from .user import User
from .event import Event
