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
"""This module contains all of the Entity Email specific processors.

Processors hold the business logic for how solr feeder is updated.
"""

import re

import requests
from flask import current_app
from namex.models import db, Name  # noqa: 1001
# noqa: 1005


def convert_to_solr_conformant_json(request_str):
    """Replace the 'add' keys append with a number with the key 'add'.

    This is needed as dict do not allow duplicates keys.  The solr api expects a json
    format that requires duplicate add keys so as a workaround this limitation, this is
    done after the payload_dict is converted to a json string.
    """
    request_str = re.sub(r"\"add\d+\":", "\"add\":", request_str)  # noqa:Q000
    return request_str


def post_to_solr_feeder(payload: dict):
    """Post to solr feeder api's feeds endpoint."""
    solr_feeder_api_url = current_app.config['SOLR_FEEDER_API_URL']
    resp = requests.post(
        f'{solr_feeder_api_url}/feeds',
        json=payload,
        headers={
            'Content-Type': 'application/json;charset=UTF-8'
        }
    )
    return resp


def convert_to_solr_conformant_datetime_str(dt_to_convert):
    """Convert datetime to a date format solr feeder api accepts."""
    return dt_to_convert.strftime('%Y-%m-%dT%H:%M:%SZ')


def find_name_by_name_states(nr_id, name_states):
    """Retrieve names associated with a NR that are in state provided by name_states input param."""
    names = db.session.query(Name) \
        .filter_by(nrId=nr_id) \
        .filter(Name.state.in_(name_states)) \
        .all()
    return names
