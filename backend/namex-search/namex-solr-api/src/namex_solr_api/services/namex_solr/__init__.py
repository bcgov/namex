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
"""This module wraps the solr classes/fields for using namex solr."""
from dataclasses import asdict

from flask import Flask

from namex_solr_api.models import SolrSynonymList
from namex_solr_api.services.base_solr import Solr
from namex_solr_api.services.base_solr.utils import QueryBuilder, prep_query_str

from .doc_models.name import Name, NameField
from .doc_models.possible_conflict import PCField, PossibleConflict


class NamexSolr(Solr):
    """Extends the solr wrapper class for namex specific functionality."""

    def __init__(self, config_prefix: str, app: Flask = None) -> None:
        super().__init__(config_prefix, app)
        self.query_builder = QueryBuilder(
            identifier_field_values=[],
            unique_parent_field=PCField.TYPE,
            synonym_field_map={NameField.NAME_Q_SYN: SolrSynonymList.Type.ALL})

        # fields
        self.resp_fields = [
            PCField.CORP_NUM.value,
            PCField.JURISDICTION.value,
            PCField.NR_NUM.value,
            PCField.START_DATE.value,
            PCField.STATE.value,
            PCField.TYPE.value,
            PCField.SUB_TYPE.value,
            PCField.NAMES.value,
            "[child]",
            NameField.CHOICE.value,
            NameField.NAME.value,
            NameField.NAME_STATE.value,
            NameField.SUBMIT_COUNT.value
        ]
        self.resp_fields_nested = [
            NameField.CHOICE.value,
            NameField.NAME.value,
            NameField.NAME_STATE.value,
            NameField.SUBMIT_COUNT.value,
            NameField.PARENT_ID.value,
            NameField.PARENT_JURISDICTION.value,
            NameField.PARENT_START_DATE.value,
            NameField.PARENT_STATE.value,
            NameField.PARENT_TYPE.value,
            NameField.PARENT_SUB_TYPE.value,
            NameField.UNIQUE_KEY.value,
        ]

    def create_or_replace_docs(self,
                               docs: list[PossibleConflict] | None = None,
                               raw_docs: list[dict] | None = None,
                               timeout=25,
                               additive=True):
        """Create or replace solr docs in the core."""
        update_list = raw_docs if raw_docs else [asdict(doc) for doc in docs]

        if not additive and not raw_docs:
            for pc_dict in update_list:
                # names
                if names := pc_dict.get(PCField.NAMES.value, None):
                    pc_dict[PCField.NAMES.value] = {"set": names}

        url = self.update_url if len(update_list) < 1000 else self.bulk_update_url  # noqa: PLR2004
        return self.call_solr("POST", url, json_data=update_list, timeout=timeout)

    @staticmethod
    def get_name_search_full_query_boost(query_value: str):
        """Return the list of full query boost information intended for business search.

        Phrase boosts use the raw query; token-derived boosts use conflict
        match-prep terms.
        """
        from namex_solr_api.services.namex_solr.utils.formatting_helpers import (
            build_distinctive_coverage_boosts,
            build_hyphen_glued_boosts,
            build_initials_exact_boosts,
            build_initials_group_boosts,
            conflict_match_prep_terms,
        )

        full_query_boosts = [
            {
                "field": NameField.NAME_Q_EXACT,
                "value": prep_query_str(query_value),
                "boost": "3",
            },
            {
                "field": NameField.NAME_Q_SINGLE,
                "value": prep_query_str(query_value),
                "boost": "2",
            },
            {
                "field": NameField.NAME_Q,
                "value": prep_query_str(query_value),
                "boost": "5",
                "fuzzy": "5"
            },
            {
                "field": NameField.NAME_Q_AGRO,
                "value": prep_query_str(query_value),
                "boost": "3",
                "fuzzy": "10"
            }
        ]
        # add more boost clauses if a dash is in the query
        if "-" in query_value:
            full_query_boosts += [
                {
                    "field": NameField.NAME_Q,
                    "value": prep_query_str(query_value, "remove"),
                    "boost": "3",
                    "fuzzy": "5"
                },
                {
                    "field": NameField.NAME_Q,
                    "value": prep_query_str(query_value, "pad"),
                    "boost": "7",
                    "fuzzy": "5"
                },
                {
                    "field": NameField.NAME_Q,
                    "value": prep_query_str(query_value, "tighten"),
                    "boost": "7",
                    "fuzzy": "5"
                },
                {
                    "field": NameField.NAME_Q,
                    "value": prep_query_str(query_value, "tighten-remove"),
                    "boost": "3",
                    "fuzzy": "5"
                }
            ]
        match_terms = conflict_match_prep_terms(query_value)
        full_query_boosts += build_initials_group_boosts(match_terms)
        full_query_boosts += build_initials_exact_boosts(match_terms)
        full_query_boosts += build_hyphen_glued_boosts(query_value)
        full_query_boosts += build_distinctive_coverage_boosts(match_terms)
        return full_query_boosts
