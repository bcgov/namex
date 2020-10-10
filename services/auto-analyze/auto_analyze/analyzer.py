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
"""Analyzes a single name."""
import asyncio
import random


async def auto_analyze(name: str) -> bool:
    """Return either True/False if the name passes auto analysis.

    For fun it approves all names of even length.
    """
    print(f'> {name}')
    rand = int(random.uniform(1, 5))
    await asyncio.sleep(rand)
    print(f'< {name} {rand}')

    if len(name) % 2:
        return False
    return True
