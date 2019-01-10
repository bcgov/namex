"""The tables used to track data sent back to the legacy NRO system
   By convention, we add all data items to core models held here
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
class NRONamesSyncJobStatus(db.Model):
    __tablename__ = 'nro_names_sync_job_status'

    code = db.Column('cd', db.String(10), primary_key=True)
    description = db.Column('desc', db.String(1000))

    def __init__(self):
        pass


class NRONamesSyncJob(db.Model):
    __tablename__ = 'nro_names_sync_job'

    # core fields
    id = db.Column('id', db.Integer, primary_key=True)
    statusCd = db.Column('status_cd', db.String(10), db.ForeignKey('nro_names_sync_job_status.cd'))
    startTime = db.Column('start_time', db.DateTime(timezone=True), default=None)
    endTime = db.Column('end_time', db.DateTime(timezone=True), default=None)


class NRONamesSyncJobDetail(db.Model):
    __tablename__ = 'nro_names_sync_job_detail'

    # core fields
    id = db.Column('id', db.Integer, primary_key=True)
    jobId = db.Column('job_id', db.Integer, db.ForeignKey('nro_names_sync_job.id'))
    nrNum = db.Column('nr_num', db.String(10))
    time = db.Column('time', db.DateTime(timezone=True), default=None)
    success = db.Column('success', db.Boolean, default=True)
    errorMsg = db.Column('error_msg', db.String(1000), default=None)
