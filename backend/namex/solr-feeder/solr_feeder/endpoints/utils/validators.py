# Copyright © 2023 Province of British Columbia
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
"""Manages validators for endpoints."""


def feeds_validate(payload: dict) -> str:
    """Validate the feeder endpoint payload."""
    solr_core = payload.get('solr_core')
    if not solr_core:
        return 'Required parameter "solr_core" not defined'

    if solr_core not in ('names', 'possible.conflicts', 'search'):
        return 'Parameter "solr_core" only has valid values of "names", "possible.conflicts" or "search"'

    if solr_core == 'search':
        if not payload.get('identifier'):
            return 'Required parameter "identifier" not defined'
        if not payload.get('legalType'):
            return 'Required parameter "legalType" not defined'
    else:
        if 'request' not in payload:
            return 'Required parameter "request" not defined'

    return None
