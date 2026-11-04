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
"""Manages dataclass for the solr name doc."""
from dataclasses import dataclass

from namex_solr_api.common.base_enum import BaseEnum


class NameField(BaseEnum):
    """Enum of the name fields available."""

    # unique key for all docs
    UNIQUE_KEY = "id"
    # stored fields
    CHOICE = "choice"
    NAME = "name"
    NAME_STATE = "name_state"
    SUBMIT_COUNT = "submit_count"
    PARENT_ID = "parent_id"
    PARENT_JURISDICTION = "parent_jurisdiction"
    PARENT_START_DATE = "parent_start_date"
    PARENT_STATE = "parent_state"
    PARENT_TYPE = "parent_type"
    PARENT_SUB_TYPE = "parent_sub_type"
    # query fields
    NAME_Q = "name_q"  # minimal stem
    NAME_Q_EXACT = "name_q_exact"  # edge ngram
    NAME_Q_EXACT_PHRASE = "name_q_exact_phrase"  # keyword tokenizer (no stemming, no ngram)
    NAME_Q_SINGLE = "name_q_single_term"  # ngram
    NAME_Q_AGRO = "name_q_stem_agro"  # aggressive stem
    NAME_Q_STEM_HIGHLIGHT = "name_q_stem_highlight"  # aggressive stem used for highlight info
    NAME_Q_SYN = "name_q_synonym"  # synonym
    NAME_Q_XTRA = "name_q_xtra"  # classic tokenizer on query (others using whitespace - effects periods, dashes etc.)
    NAME_Q_PHON_EN = "name_q_phon_en"  # DoubleMetaphone phonetic

    # common built in across docs
    SCORE = "score"


@dataclass
class Name:
    """Class representation for a solr name doc."""
    name: str
    # TODO: review existing states (A, C, R, APPROVED, CONDITION) -- are A/APPROVED the same? Are C/CONDITION the same?
    # adding new states for corp name: 'CORP', and nr name: 'NE'
    name_state: str
    choice: int | None = None
    id: str | None = None  # set by parent
    submit_count: int | None = None
    parent_id: str | None = None  # corp num or nr num
    parent_jurisdiction: str | None = None
    parent_start_date: str | None = None
    parent_state: str | None = None
    parent_type: str | None = None
    parent_sub_type: str  = '-'
