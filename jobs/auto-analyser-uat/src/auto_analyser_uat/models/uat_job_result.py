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
"""This module holds all of the basic data about uat job runs.

The UatJobResult class is held in this module
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List

from .db import db
from .request_name import RequestName


class UatJobResult(db.Model):
    """This class manages overall information for uat jobs."""

    class UatTypes(Enum):
        """Render an Enum of the UAT job types."""

        ACCURACY = 'uat_accuracy'
        REJECTION = 'uat_rejection'

    __tablename__ = 'uat_job_results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    results_sent = db.Column('results_sent', db.Boolean, unique=False, default=False)
    uat_end_date = db.Column('uat_end_date', db.DateTime(timezone=True))
    uat_start_date = db.Column('uat_start_date', db.DateTime(timezone=True), default=datetime.utcnow)
    uat_finished = db.Column('uat_finished', db.Boolean, unique=False, default=False)
    uat_type = db.Column('uat_type', db.String(20), default=UatTypes.REJECTION)

    request_names = db.relationship('RequestName', lazy='dynamic', cascade='all, delete, delete-orphan')

    def get_accuracy(self, name_state: str = None) -> float:
        """Get the overall approval/rejection accuracy for job run (optional: based on name_state)."""
        if name_state:
            passed = self.get_names(name_state=name_state, result=RequestName.Results.PASS.value)
            total = self.get_names(name_state=name_state)
        else:
            passed = self.get_names(result=RequestName.Results.PASS.value)
            total = self.get_names()
        return float(len(passed))/float(len(total))

    def get_names(self, name_state: str = None, result: str = None) -> List:
        """Get names associated with the job (optional: based on result)."""
        if name_state:
            if result:
                names = db.session.query(RequestName). \
                    filter(
                        RequestName.name_state == name_state,
                        RequestName.uat_result == result,
                        RequestName.uat_job_id == self.id).all()
            else:
                names = db.session.query(RequestName). \
                    filter(
                        RequestName.name_state == name_state,
                        RequestName.uat_job_id == self.id).all()
        elif result:
            names = db.session.query(RequestName). \
                filter(
                    RequestName.uat_result == result,
                    RequestName.uat_job_id == self.id).all()
        else:
            names = db.session.query(RequestName). \
                filter(RequestName.uat_job_id == self.id).all()

        return names

    def get_request_time_avg(self) -> float:
        """Get the average request time for the auto analyze end point during the job run."""
        names = db.session.query(RequestName). \
            filter(
                RequestName.uat_job_id == self.id).all()
        total_time = 0
        for name in names:
            time = name.auto_analyse_request_time
            if time:
                total_time += time
        return float(total_time)/float(len(names))

    def get_unfinished_names(self) -> List:
        """Get all names with unfinished uat."""
        return db.session.query(RequestName). \
            filter(
                RequestName.uat_job_id == self.id,
                RequestName.uat_result == None  # pylint: disable=singleton-comparison # noqa: E711;
            ).all()

    def save(self):
        """Save uat job instance to the db."""
        db.session.add(self)

    @classmethod
    def get_by_id(cls, job_id: int) -> UatJobResult:
        """Get the uat job by it's id."""
        return db.session.query(UatJobResult). \
            filter(UatJobResult.id == job_id).one_or_none()

    @classmethod
    def get_jobs_with_unsent_results(cls, uat_type: str = None) -> List:
        """Get all jobs with results that haven't been sent out (optional: with the given uat_type)."""
        if uat_type:
            return db.session.query(UatJobResult). \
                filter(
                    UatJobResult.uat_type == uat_type,
                    UatJobResult.results_sent == False,  # pylint: disable=singleton-comparison # noqa: E712;
                    UatJobResult.uat_finished == True   # pylint: disable=singleton-comparison # noqa: E712;
                ).all()
        return db.session.query(UatJobResult). \
            filter(
                UatJobResult.results_sent == False,  # pylint: disable=singleton-comparison # noqa: E712;
                UatJobResult.uat_finished == True   # pylint: disable=singleton-comparison # noqa: E712;
            ).all()

    @classmethod
    def get_jobs(cls, uat_type: str = None, finished: bool = True) -> List:
        """Get all finished uat jobs (optional: with the given uat_type)."""
        if uat_type:
            return db.session.query(UatJobResult). \
                filter(
                    UatJobResult.uat_type == uat_type,
                    UatJobResult.uat_finished == finished   # pylint: disable=singleton-comparison # noqa: E712;
                ).all()
        return db.session.query(UatJobResult). \
            filter(
                UatJobResult.uat_finished == finished   # pylint: disable=singleton-comparison # noqa: E712;
            ).all()
