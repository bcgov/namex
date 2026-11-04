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
"""Test suite for the name analyzer API."""
import pytest


@pytest.mark.asyncio
async def test_auto_analyzer_api(app):
    """Assert that the API can successfully recieve and process the name array."""
    data = {'names': ['person', 'man', 'woman', 'camera', 'tv', 'genius']}
    client = app.test_client()
    response = await client.post('/', json=data)
    assert response.status_code == 200
