# Copyright © 2025 Province of British Columbia
#
# Licensed under the BSD 3 Clause License, (the "License");
# you may not use this file except in compliance with the License.
# The template for the license can be found here
#    https://opensource.org/license/bsd-3-clause/
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""Manages dataclass for the solr possible conflict doc."""
from dataclasses import dataclass
from datetime import datetime

from namex_solr_api.common.base_enum import BaseEnum

from .name import Name


class PCField(BaseEnum):
    """Enum of the possible conflict fields available."""

    # unique key for all docs
    UNIQUE_KEY = "id"
    # stored fields
    CORP_NUM = "corp_num"
    JURISDICTION = "jurisdiction"
    NAMES = "names"
    NR_NUM = "nr_num"
    START_DATE = "start_date"
    # TODO: review current NR states: A, APPROVED, C, CONDITION (are a/approved and c/condition dupes?)
    # TODO: verify current CORP states: ACT, AMA, D1A, D1F, D1N, D2A, D2F, D2T, LIQ, LRS, NST
    # - Can we group these in ACT, LIQ ? Follows business search logic
    # - Will add nr states: 'CONSUMED', 'EXPIRED', 'REJECTED', 'DRAFT'
    STATE = "state"
    TYPE = "type"  # NR or CORP
    SUB_TYPE = "sub_type" # FR, BC, ULC, XPRO, ...
    # query fields
    CORP_NUM_Q = "corp_num_q"
    CORP_NUM_Q_EDGE = "corp_num_q_edge"
    NR_NUM_Q = "nr_num_q"
    NR_NUM_Q_EDGE = "nr_num_q_edge"

    # common built in across docs
    SCORE = "score"


@dataclass
class PossibleConflict:
    """Class representation for a solr possible conflict doc."""
    id: str  # The nr_num or corp_num depending on type
    names: list[Name]
    state: str  # APPROVED, CONDITION, CONSUMED, DRAFT, EXPIRED, REJECTED, ACT, LIQ
    type: str  # NR, CORP
    sub_type: str  # FR, BC, ULC, XPRO, ...
    corp_num: str | None = None
    jurisdiction: str | None = None
    nr_num: str | None = None
    start_date: datetime | None = None

    def __post_init__(self):
        """Update child 'parent_' fields."""
        for index, name in enumerate(self.names or []):
            # set parent_state, parent_type, parent_id
            if isinstance(name, dict):
                name['id'] = f'{self.id}-name-{index}'
                name['parent_id'] = self.id
                name['parent_jurisdiction'] = self.jurisdiction
                name['parent_start_date'] = self.start_date
                name['parent_state'] = self.state
                name['parent_type'] = self.type
                name['parent_sub_type'] = self.sub_type

            elif isinstance(name, Name):
                name.id = f'{self.id}-name-{index}'
                name.parent_id = self.id
                name.parent_jurisdiction = self.jurisdiction
                name.parent_start_date = self.start_date
                name.parent_state = self.state
                name.parent_type = self.type
                name.parent_sub_type = self.sub_type
