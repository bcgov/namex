# Copyright © 2020 Province of British Columbia
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
"""This module holds all of the basic data about the auto analyzer uat testing."""
import os
from datetime import datetime
from http import HTTPStatus
from typing import List
from urllib.parse import quote_plus

import requests
from flask import Flask, current_app

from config import Config
from models import RequestName, UatJobResult, db
from utils import get_names_list_from_csv
from utils.logging import setup_logging


setup_logging(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logging.conf')
)


def create_app(config=Config) -> Flask:
    """Return a configured Flask App using the Factory method."""
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    return app


def get_prev_job_names(job_id: int) -> List:
    """Get names with given job id."""
    job = UatJobResult.get_by_id(job_id)
    name_objs = job.get_names()
    names = []
    for name_obj in name_objs:
        names.append(name_obj.name)
    return names


def clean_names_list(name_list: List) -> List:
    """Return list with names that wont fail in namex db query."""
    for name in name_list:
        if "'" in name:
            name_list.remove(name)
            name = name.replace("'", "''")
            name_list.append(name)
    return name_list


def get_names_from_namex(uat_job: UatJobResult, app: Flask, excl_names: List, priority_names: List, nrs: List) -> List:
    """Get names from namex."""
    existing_names = RequestName.get_all_names()
    sql = (
        """
        select requests.id, requests.nr_num, requests.request_type_cd, requests.state_cd, requests.submitted_date,
            names.choice, names.name, names.decision_text, names.conflict1_num, names.conflict1, names.conflict1_num,
            names.state
        from requests, names
        where requests.id=names.nr_id
            and requests.request_type_cd='CR'
        """
    )
    if excl_names:
        name_list = clean_names_list(excl_names)
        sql += f' and names.name not in {str(name_list)}'
    if nrs:
        sql += f' and requests.nr_num in {str(nrs)}'
    if priority_names:
        name_list = clean_names_list(priority_names)
        sql += f' and names.name in {str(name_list)}'
    else:
        if existing_names:
            name_list = clean_names_list(existing_names)
            sql += f' and names.name not in {str(name_list)}'

        if uat_job.uat_type == UatJobResult.UatTypes.REJECTION.value:
            sql += (
                """
                 and names.state='REJECTED'
                 and requests.state_cd in ('APPROVED', 'CONDITIONAL', 'REJECTED')
                """
            )
        else:  # uat_job.uat_type == uat_accuracy
            sql += "and requests.state_cd in ('DRAFT')"

    sql += (
        f"""
        order by requests.submitted_date desc nulls last
        limit {app.config['MAX_ROWS']}
        """
    )
    sql = sql.replace('[', '(').replace(']', ')').replace('"', "'")
    new_names = db.get_engine(app, 'namex').execute(sql)
    return new_names.fetchall()


def load_names_into_uat(names: list):
    """Load names into uat database."""
    for name in names:
        new_name = RequestName(
            choice=name['choice'],
            conflict1_num=name['conflict1_num'],
            conflict1=name['conflict1'],
            decision_text=name['decision_text'],
            name=name['name'],
            name_state=name['state'],
            nr_num=name['nr_num'],
            nr_request_type_cd=name['request_type_cd'],
            nr_state=name['state_cd'],
            nr_submitted_date=name['submitted_date'],
        )
        new_name.save()


def send_to_auto_analyzer(name: RequestName, app: Flask):
    """Return result of auto analyzer given the name."""
    payload = {
        'name': name.name,
        'location': 'BC',
        'entity_type_cd': name.nr_request_type_cd,
        'request_action_cd': 'NEW'
    }
    url_query = '&'.join(f'{key}={quote_plus(value)}' for (key, value) in payload.items())
    response = requests.get(
        f"{app.config['AUTO_ANALYSE_URL']}?{url_query}",
        timeout=10000
    )
    if response.status_code != HTTPStatus.OK:
        raise Exception(f'Error auto analyser returned {response.status_code}')
    return response


def set_uat_result(name: RequestName):
    """Set the uat result for the name based on the job type."""
    if name.name_state != 'NE':  # if they have state 'NE' result will be updated later
        if name.name_state == 'REJECTED' and name.auto_analyse_result != 'AVAILABLE':
            name.uat_result = RequestName.Results.PASS.value
        elif name.name_state == 'APPROVED' and name.auto_analyse_result == 'AVAILABLE':
            name.uat_result = RequestName.Results.PASS.value
        else:
            name.uat_result = RequestName.Results.FAIL.value


def uat_accuracy_update(app: Flask, excluded_names: List, prioritized_names: List) -> int:
    """Update previously unexamined names with examined state and check result."""
    # get all names without a uat result
    name_objs = RequestName.get_unverified()
    if not name_objs:
        return 0
    names = []
    nrs = []
    for name in name_objs:
        if prioritized_names:
            if name.name in prioritized_names:
                names.append(str(name.name))
                nrs.append(name.nr_num)
        else:
            names.append(str(name.name))
            nrs.append(name.nr_num)
    namex_names = get_names_from_namex(None, app, excluded_names, names, nrs)
    # check if any of these have been examined in namex
    if not namex_names:
        return 0
    count = 0
    for name in name_objs:
        namex_name = None
        for n in namex_names:
            if name.name == n['name']:
                namex_name = n
                break
        if namex_name and namex_name['state'] != 'NE':
            # update the uat_result
            name.name_state = namex_name['state']
            name.nr_state = namex_name['state_cd']
            name.conflict1_num = namex_name['conflict1_num'],
            name.conflict1 = namex_name['conflict1'],
            name.decision_text = namex_name['decision_text'],
            set_uat_result(name)
            name.save()
            # update the job if all names finished
            uat_job = UatJobResult.get_by_id(name.uat_job_id)
            if not uat_job.get_unfinished_names():
                uat_job.uat_finished = True
                uat_job.save()
        count += 1
        if count == app.config['MAX_ROWS']:
            break
    return count


def run_auto_analyse_uat(uat_job: UatJobResult, app: Flask) -> int:
    """Run names through the auto analyser and save the results."""
    names_list = RequestName.get_untested()

    count = 0
    for name in names_list:
        try:
            app.logger.debug(f'testing {name.name}...')
            result = send_to_auto_analyzer(name, app)
            result_json = result.json()
            name.auto_analyse_request_time = int(result.elapsed.total_seconds())
            name.uat_job_id = uat_job.id
            name.auto_analyse_response = result_json
            name.auto_analyse_result = result_json['status']
            if result_json['issues']:
                name.auto_analyse_issue_text = result_json['issues'][0]['line1']
                name.auto_analyse_issue_type = result_json['issues'][0]['issue_type']
                if result_json['issues'][0]['conflicts']:
                    name.auto_analyse_conflicts = result_json['issues'][0]['conflicts'][0]['name']
            set_uat_result(name)
            name.save()
            app.logger.debug(f'{name.name} auto analyse time: {name.auto_analyse_request_time}')

            count += 1
            if count == app.config['MAX_ROWS']:
                break
        except Exception as err:
            name.uat_result = RequestName.Results.ERROR.value
            name.uat_job_id = uat_job.id
            name.save()
            app.logger.error(err)
            app.logger.debug('skipping this name due to error.')
            continue

    return count


if __name__ == '__main__':
    try:
        app = create_app(Config)
        uat_type = app.config['UAT_TYPE']
        app.logger.debug(f'Running {uat_type}...')

        # delete any previously queued untested names (refresh the queue of names to test)
        for name in RequestName.get_untested():
            db.session.delete(name)

        if app.config['CSV_FILE'] and app.config['PREV_JOB_ID']:
            app.logger.error(
                'CSV_FILE and PREV_JOB_ID set in config. This is not handled, please only set one of these values.')
            app.logger.debug('CSV_FILE will take precedence (PREV_JOB_ID will be ignored).')

        excluded_names = \
            get_names_list_from_csv(app.config['EXCLUDED_NAMES']) if app.config['EXCLUDED_NAMES'] else []
        prioritized_names = get_names_list_from_csv(app.config['CSV_FILE']) if app.config['CSV_FILE'] else None
        if not prioritized_names:
            prioritized_names = \
                get_prev_job_names(int(app.config['PREV_JOB_ID'])) if app.config['PREV_JOB_ID'] else None

        if uat_type == 'uat_accuracy_update':
            count = uat_accuracy_update(app, excluded_names, prioritized_names)
        else:
            if uat_type not in [x.value for x in UatJobResult.UatTypes.__members__.values()]:
                raise Exception(f'invalid UAT_TYPE: {uat_type}. Please change it in the config.')
            uat_job = UatJobResult(uat_type=uat_type)
            uat_job.save()

            app.logger.debug('fetching new names...')
            new_names = get_names_from_namex(uat_job, app, excluded_names, prioritized_names, None)
            app.logger.debug('loading new names...')
            if new_names:
                load_names_into_uat(new_names)

                app.logger.debug('running uat...')
                count = run_auto_analyse_uat(uat_job, app)
                uat_job.uat_end_date = datetime.utcnow()

                # accuracy type will complete later in different job (after names have been completed)
                if uat_job.uat_type == UatJobResult.UatTypes.REJECTION.value:
                    uat_job.uat_finished = True
                uat_job.save()
            else:
                count = 0
        db.session.commit()
        app.logger.debug(f'Job completed. Processed {count} names.')

    except Exception as err:
        app.logger.error(err)
        app.logger.debug('Error occurred, rolling back uat db...')
        db.session.rollback()
        app.logger.debug('Rollback successful.')
