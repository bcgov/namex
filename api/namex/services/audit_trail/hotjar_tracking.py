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
from datetime import datetime

from flask import current_app

from namex.models import HotjarTracking as HotjarTrackingModel


class HotjarTracking(object):
    """Class of Hotjar Tracking."""

    @staticmethod
    def record(nr_model, hotjar_user):
        """Record a hotjar session."""
        try:
            hotjar = HotjarTracking.create(nr_model, hotjar_user)
            hotjar.save_to_db()
            return hotjar
        except Exception as err:  # pylint: disable=broad-except
            current_app.logger.error(err.with_traceback(None))

    @staticmethod
    def create(nr_model, hotjar_user):
        """Create a hotjar tracking object."""
        return HotjarTrackingModel(nrId=nr_model.id, hotjarUser=hotjar_user, lastUpdate=datetime.utcnow())
