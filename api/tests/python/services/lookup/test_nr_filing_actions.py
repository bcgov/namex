# Copyright © c2021 Province of British Columbia
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
import logging

from flask import Flask

from namex.services.lookup import NameRequestFilingActions

def test_nr_filing_actions(caplog):
    """Assert that the nr_filing_actions is created and cached."""
    app = Flask(__name__)
    nr_type_cd = 'BC'
    nr_filing_actions_debug_msg = 'creating nr_filing_actions'

    caplog.clear()

    with app.app_context():
        with caplog.at_level(logging.DEBUG):

            nr_filing_actions = NameRequestFilingActions()
            nr_filing_actions.get_actions(nr_type_cd)
            assert  nr_filing_actions_debug_msg in [rec.message for rec in caplog.records]

            caplog.clear()
            nr_filing_actions.get_actions(nr_type_cd)
            assert  nr_filing_actions_debug_msg not in [rec.message for rec in caplog.records]
