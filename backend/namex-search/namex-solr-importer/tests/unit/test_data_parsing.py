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
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
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
"""Unit tests for importer data parsing."""

from namex_solr_importer.utils.data_parsing import parse_conflict


def test_parse_conflict_normalizes_nr_num_for_nr_docs():
    """Importer NR docs should use canonical no-space nr for id and nr_num."""
    possible_conflict = parse_conflict(
        {
            "nr_num": "NR 6059079",
            "state": "APPROVED",
            "sub_type": "BC",
            "jurisdiction": "BC",
            "start_date": None,
            "names": [
                {
                    "name": "TEST NAME",
                    "name_state": "A",
                    "submit_count": 1,
                    "choice": 1,
                }
            ],
        },
        "NR",
    )

    assert possible_conflict.id == "NR6059079"
    assert possible_conflict.nr_num == "NR6059079"


def test_parse_conflict_corp_id_unchanged():
    """Importer CORP docs should still use corp_num as id."""
    possible_conflict = parse_conflict(
        {
            "corp_num": "BC1234567",
            "state": "ACTIVE",
            "sub_type": "BC",
            "jurisdiction": "BC",
            "start_date": None,
            "name": "TEST CORP",
        },
        "CORP",
    )

    assert possible_conflict.id == "BC1234567"
    assert possible_conflict.nr_num is None
