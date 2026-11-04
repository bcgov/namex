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
"""API endpoint for updating/adding synonyms in solr."""
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from namex_solr_api.exceptions import bad_request_response, exception_response
from namex_solr_api.models import SolrSynonymList, User
from namex_solr_api.services import jwt, solr
from namex_solr_api.services.namex_solr.utils import (
    analyze_stemmed_agro_token_map,
    get_synonyms,
    stem_synonym_payload,
)

bp = Blueprint("SYNONYMS", __name__, url_prefix="/synonyms")


@bp.put("")
@cross_origin(origins="*")
@jwt.requires_roles([User.Role.system.value])
def update_synonyms():
    """Add/trigger update to synonyms lists."""
    # NOTE: changes will not be reflected until the next daily reindex is finished
    try:
        if not (synonyms := request.json) or not isinstance(synonyms, dict):
            return bad_request_response("Invalid payload")

        errors = [key for key in synonyms if key not in [SolrSynonymList.Type.ALL]]
        if errors:
            return bad_request_response(f"Invalid synonym type(s): {','.join(errors)}")

        # update db synonym lists
        synonyms_terms: dict[SolrSynonymList.Type, list[str]] = {}
        synonyms_updated: dict[SolrSynonymList.Type, dict[str, list[str]]] = {}
        skipped_terms: list[str] = []
        for synonym_type, synonym_lists in synonyms.items():
            # i.e. syn_type = ALL  # noqa: ERA001
            syn_type = SolrSynonymList.Type(synonym_type)

            # Stem every key/member with the same analyzer as name_q_stem_agro so
            # stored keys match the (post synonym graph) stems in the solr index.
            # Raises if analysis is unavailable - unstemmed data must never be
            # persisted, so the whole request errors before any db write.
            vocabulary = [
                token
                for key, members in (synonym_lists or {}).items()
                for phrase in [key, *(members or [])]
                for token in (phrase or "").lower().split()
            ]
            stem_map = analyze_stemmed_agro_token_map(solr, vocabulary)
            stemmed_lists, skipped = stem_synonym_payload(synonym_lists, stem_map)
            skipped_terms += skipped

            # i.e. { ALL: ['bc', 'british columbia', 'ab', 'alberta'] }
            synonyms_terms[syn_type] = SolrSynonymList.create_or_replace_all(synonyms=stemmed_lists, synonym_type=syn_type)

            if request.args.get("prune") == "true":
                # delete all synonyms under the type which were not referenced in this update
                SolrSynonymList.delete_all(syn_type, synonyms_terms[syn_type])

            # i.e [<SolrSynonymList synonym='bc', ...>, <SolrSynonymList synonym='ab', ...>, ...]
            terms_synonym_lists = SolrSynonymList.find_all_by_synonyms(synonyms_terms[syn_type], syn_type)

            # i.e. { ALL: { 'bc': ['british columbia'], 'ab': ['alberta'], ... }}
            synonyms_updated = {syn_type: { x.synonym: x.synonym_list for x in terms_synonym_lists}}

        # update solr synonym file
        if SolrSynonymList.Type.ALL in synonyms_updated:
            solr.create_or_update_synonyms(SolrSynonymList.Type.ALL, synonyms_updated[SolrSynonymList.Type.ALL])
            # Reload the solr core so it will register any changes for new updates/imports. It will throw an error if there is some issue with the synonym lists.
            # NOTE: Any existing docs will not pickup the new synonym changes until the next reindex
            solr.reload_core()

        response = {"message": "Update successful"}
        if skipped_terms:
            # stemmed form exceeded the synonym column limit
            response["skipped"] = skipped_terms
        return jsonify(response), HTTPStatus.OK

    except Exception as exception:
        return exception_response(exception)

@bp.get("/resync-all")
@cross_origin(origins="*")
@jwt.requires_roles([User.Role.system.value])
def resync_synonyms():
    """Add/trigger update to synonyms lists."""
    try:
        synonyms = get_synonyms()
        if SolrSynonymList.Type.ALL in synonyms:
            solr.create_or_update_synonyms(SolrSynonymList.Type.ALL, synonyms[SolrSynonymList.Type.ALL])

        # reload the solr core (so it will register any changes)
        solr.reload_core()

        return jsonify({"message": "Resync all synonyms successful"}), HTTPStatus.OK

    except Exception as exception:
        return exception_response(exception)
