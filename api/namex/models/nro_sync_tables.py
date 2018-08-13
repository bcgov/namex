"""Request is the main business class that is the real top level object in the system
"""
from . import db, ma
from flask import current_app
from namex.exceptions import BusinessException
from sqlalchemy import Sequence
from sqlalchemy.orm import backref
from marshmallow import Schema, fields, post_load, post_dump
from .nwpta import PartnerNameSystem
from .user import User, UserSchema
from .comment import Comment, CommentSchema
from .applicant import Applicant
from .name import Name, NameSchema
from .state import State, StateSchema
from datetime import datetime


# noinspection PyPep8Naming
class NRONamesSyncJob(db.Model):
    __tablename__ = 'nro_names_sync_job'

    # core fields
    id = db.Column('id', db.Integer, primary_key=True)
    statusCd = db.Column('status_cd', db.String(10))
    startTime = db.Column('start_time', db.DateTime, default=None)
    endTime = db.Column('end_time', db.DateTime, default=None)


    def __init__(self, *args, **kwargs):
        pass


class NRONamesSyncJobDetail(db.Model):
    __tablename__ = 'nro_names_sync_job_detail'

    # core fields
    id = db.Column('id', db.Integer, primary_key=True)
    jobId = db.Column('job_id', db.Integer)
    nrNum = db.Column('nr_num', db.String(10))
    time = db.Column('time', db.DateTime, default=None)


    def __init__(self, *args, **kwargs):
        pass

