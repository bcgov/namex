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
"""Exposes all of the resource endpoints mounted in Flask-Blueprint style."""
from .constants import EndpointVersionPath
from .v1 import corporations_bp, meta_bp, ops_bp
from .version_endpoint import VersionEndpoint


v1_endpoint = VersionEndpoint(  # pylint: disable=invalid-name
    name='API_V1',
    path=EndpointVersionPath.API_V1,
    bps=[meta_bp, corporations_bp, ops_bp])
