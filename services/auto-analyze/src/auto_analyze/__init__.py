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
"""The service that analyizes an array of names."""
import asyncio
import json
import random

from quart import Quart, jsonify, request

from .analyzer import auto_analyze


app = Quart(__name__)


@app.route('/', methods=['POST'])
async def private_service():
    """Return the outcome of this private service call."""
    json_data = await request.get_json()

    result = await asyncio.gather(
        *[auto_analyze(name) for name in json_data.get('names')]
    )
    return jsonify(result=result)
