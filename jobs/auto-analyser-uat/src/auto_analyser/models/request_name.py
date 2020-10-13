# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This module holds all of the basic data about a Request Name.

The RequestName class is held in this module
"""
from datetime import datetime
from enum import Enum
from typing import List

from sqlalchemy.dialects.postgresql import JSONB

from .db import db


class RequestName(db.Model):
    """This class manages names imported from namex that will be tested against the auto analyser."""

    class Results(Enum):
        """Render an Enum of the uat results."""

        PASS = 'PASSED'
        FAIL = 'FAILED'
        ERROR = 'ERROR'

    __tablename__ = 'request_names'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    choice = db.Column('choice', db.Integer)
    conflict1_num = db.Column('conflict1_num', db.VARCHAR(20))
    conflict1 = db.Column('conflict1', db.VARCHAR(1024))
    decision_text = db.Column('decision_text', db.VARCHAR(1024))
    name = db.Column('name', db.VARCHAR(1024))
    name_state = db.Column('name_state', db.VARCHAR(20))

    nr_num = db.Column('nr_num', db.VARCHAR(10))
    nr_request_type_cd = db.Column('nr_request_type_cd', db.VARCHAR(10))
    nr_state = db.Column('nr_state', db.VARCHAR(20))
    nr_submitted_date = db.Column('nr_submitted_date', db.DateTime(timezone=True), default=datetime.utcnow)

    auto_analyse_issue_text = db.Column('auto_analyse_issue_text', db.VARCHAR(2048))
    auto_analyse_conflict1 = db.Column('auto_analyse_conflict1', db.VARCHAR(1024))
    auto_analyse_issue_type = db.Column('auto_analyse_issue_type', db.VARCHAR(20))
    auto_analyse_response = db.Column('auto_analyse_response', JSONB)
    auto_analyse_result = db.Column('auto_analyse_result', db.VARCHAR(20))

    auto_analyse_date = db.Column('auto_analyse_date', db.DateTime(timezone=True))
    auto_analyse_request_time = db.Column('auto_analyse_request_time', db.Integer)
    uat_result = db.Column('uat_result', db.String(20), default=None)

    uat_job_id = db.Column('uat_job_id', db.Integer, db.ForeignKey('uat_job_results.id'))

    def save(self):
        """Save uat job instance to the db."""
        db.session.add(self)

    @classmethod
    def get_all_names(cls, uat_result: str = None) -> List:
        """Get all names in the db (optional: based on result)."""
        names = []
        if uat_result:
            db_result = db.session.query(RequestName.name). \
                filter(RequestName.uat_result == uat_result).all()
        else:
            db_result = db.session.query(RequestName.name).all()
        if db_result:
            for name in db_result:
                names.append(name[0])
        return names

    @classmethod
    def get_untested(cls) -> List:
        """Get all request names that haven't been tested by a uat job."""
        return db.session.query(RequestName). \
            filter(
                RequestName.uat_job_id == None  # pylint: disable=singleton-comparison # noqa: E711;
            ).all()

    @classmethod
    def get_unverified(cls) -> List:
        """Get all request names that haven't been tested by a uat job."""
        return db.session.query(RequestName). \
            filter(
                RequestName.auto_analyse_result != RequestName.Results.ERROR.value,
                RequestName.uat_result == None  # pylint: disable=singleton-comparison # noqa: E711;
            ).all()
