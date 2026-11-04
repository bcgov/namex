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
"""Exposes all of the non internal synonyms endpoints in Flask-Blueprint style."""
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from namex_solr_api.exceptions import bad_request_response, exception_response
from namex_solr_api.models import SolrSynonymList
from namex_solr_api.services import jwt, solr
from namex_solr_api.services.namex_solr.utils import analyze_stemmed_agro_token_map, stem_phrase

bp = Blueprint("SYNONYMS", __name__, url_prefix="/synonyms")


@bp.post("")
@cross_origin(origins="*")
@jwt.requires_auth
def synonym_lists():
    """Return the synonym lists for the given terms."""
    try:
        terms: list = request.json.get("terms", [])
        if not isinstance(terms, list) or len(terms) == 0:
            return bad_request_response("Expected required value 'terms' to be a list of strings.")

        # Stored synonym keys are agro stems
        # - stem the incoming surface terms so we keep sending plain words
        # - Lookup degrades to the raw terms if analysis fails
        try:
            stem_map = analyze_stemmed_agro_token_map(
                solr, [token for term in terms for token in str(term).lower().split()]
            )
        except Exception:
            stem_map = {}
        stems_by_term = {str(term): stem_phrase(str(term), stem_map) or str(term).lower() for term in terms}

        terms_synonym_lists = SolrSynonymList.find_all_by_synonyms(
            list(set(stems_by_term.values())), SolrSynonymList.Type.ALL
        )
        lists_by_stem = {x.synonym: x.synonym_list for x in terms_synonym_lists}
        # respond keyed by the caller's original terms
        response = {
            term: lists_by_stem[stem]
            for term, stem in stems_by_term.items()
            if stem in lists_by_stem
        }
        return jsonify(response), HTTPStatus.OK

    except Exception as exception:
        return exception_response(exception)
