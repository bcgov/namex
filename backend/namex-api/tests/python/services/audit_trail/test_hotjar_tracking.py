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
from namex.constants import ValidSources
from namex.models import Name as NameDAO
from namex.models import Request as RequestDAO
from namex.models import State
from namex.services.audit_trail.hotjar_tracking import HotjarTracking


def create_base_nr():
    """Create a base NR object."""
    nr_model = RequestDAO()
    nr_model.nrNum = 'NR 0000002'
    nr_model.stateCd = State.PENDING_PAYMENT
    nr_model.requestId = 1460775
    nr_model._source = ValidSources.NAMEREQUEST.value
    name1 = NameDAO()
    name1.choice = 1
    name1.name = 'TEST NAME ONE'
    nr_model.names = [name1]
    nr_model.additionalInfo = 'test'
    nr_model.requestTypeCd = 'CR'
    nr_model.request_action_cd = 'NEW'
    nr_model.save_to_db()
    return nr_model


def test_hotjar_tracking_record(app):
    """Test hotjar tracking record function."""
    hotjar_user = 'testhotjar'
    nr_model = create_base_nr()

    hotjar = HotjarTracking.record(nr_model, hotjar_user)
    assert hotjar is not None
    assert hotjar.hotjarUser == hotjar_user


def test_hotjar_tracking_create(app):
    """Test hotjar tracking create function."""
    hotjar_user = 'testhotjar'
    nr_model = create_base_nr()

    hotjar_model = HotjarTracking.create(nr_model, hotjar_user)
    assert hotjar_model is not None
    assert hotjar_model.hotjarUser == hotjar_user
