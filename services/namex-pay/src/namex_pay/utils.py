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
"""This module holds general utility functions and helpers for the main package.

Supply version and commit hash info.

When deployed in OKD, it adds the last commit hash onto the version info.
"""
import os
from namex_pay.version import __version__
import time as _time
from datetime import (  # pylint: disable=unused-import # noqa: F401, I001, I005
     datetime as _datetime,  # pylint: disable=unused-import # noqa: F401, I001, I005
     timezone,  # pylint: disable=unused-import # noqa: F401, I001, I005
     timedelta
)  # noqa: F401, I001, I005
# pylint: disable=unused-import # noqa: F401, I001, I003, I005


class datetime(_datetime):  # pylint: disable=invalid-name; # noqa: N801; ha datetime is invalid??
    """Alternative to the built-in datetime that has a timezone on the UTC call."""

    @classmethod
    def utcnow(cls):
        """Construct a UTC non-naive datetime, meaning it includes timezone from time.time()."""
        time_stamp = _time.time()
        return super().utcfromtimestamp(time_stamp).replace(tzinfo=timezone.utc)


def _get_build_openshift_commit_hash():
    return os.getenv('VCS_REF', None)


def get_run_version():
    """Return a formatted version string for this service."""
    commit_hash = _get_build_openshift_commit_hash()
    if commit_hash:
        return f'{__version__}-{commit_hash}'
    return __version__
