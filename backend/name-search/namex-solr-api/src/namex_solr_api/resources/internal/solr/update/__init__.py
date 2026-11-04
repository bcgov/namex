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
"""Exposes all of the update endpoints in Flask-Blueprint style."""
import re
from dataclasses import asdict
from http import HTTPStatus

from flask import Blueprint, g, jsonify, request
from flask_cors import cross_origin

from namex_solr_api.exceptions import exception_response
from namex_solr_api.models import SolrDoc, SolrDocEvent, User
from namex_solr_api.services import jwt
from namex_solr_api.services.namex_solr.doc_models import Name, PossibleConflict
from namex_solr_api.services.namex_solr.utils import normalize_nr_num

from .resync import bp as resync_bp
from .sync import bp as sync_bp
from .synonyms import bp as synonyms_bp

bp = Blueprint("UPDATE", __name__, url_prefix="/update")
bp.register_blueprint(resync_bp)
bp.register_blueprint(sync_bp)
bp.register_blueprint(synonyms_bp)


@bp.put("")
@cross_origin(origins="*")
@jwt.requires_roles([User.Role.system.value])
@jwt.requires_auth
def update_possible_conflict():
    """Add/Update possible conflict in solr."""
    try:
        request_json: dict = request.json
        # TODO: validate request
        # errors = RequestValidator.validate_solr_update_request(request_json)  # noqa: ERA001
        # if errors:
        #     return resource_utils.bad_request_response("Invalid payload.", errors)  # noqa: ERA001

        user = User.get_or_create_user_by_jwt(g.jwt_oidc_token_info)

        possible_conflict = _parse_conflict(request_json)
        # Commit Possible Conflict. Ensures other flows (i.e. resync) will use the current data
        solr_doc = SolrDoc(doc=asdict(possible_conflict), entity_id=possible_conflict.id, submitter_id=user.id)
        solr_doc.save()
        SolrDocEvent(event_type=SolrDocEvent.Type.UPDATE.value, solr_doc_id=solr_doc.id).save()
        # SOLR update will be triggered by job (does a frequent bulk update to solr)

        return jsonify({"message": "Update accepted."}), HTTPStatus.ACCEPTED

    except Exception as exception:
        return exception_response(exception)


def _parse_names(data: dict) -> list[Name]:
    """Parse the name data as a list of Name."""
    if data['type'] == 'CORP':
        return [Name(name=data['name'], name_state="CORP")]

    names: list[Name] = []
    for name_data in data['names']:
        names.append(Name(name=name_data['name'],
                          name_state=name_data['name_state'],
                          submit_count=name_data['submit_count'],
                          choice=name_data['choice']))
    return names


def _parse_conflict(data: dict) -> PossibleConflict:
    """Parse the data as a PossibleConflict."""
    nr_num = normalize_nr_num(data.get("nr_num"))
    return PossibleConflict(
        id=nr_num if data['type'] == 'NR' else data['corp_num'],
        names=_parse_names(data),
        state=data['state'],
        type=data['type'],
        sub_type=data.get("sub_type"),
        corp_num=data.get('corp_num'),
        jurisdiction=data.get('jurisdiction'),
        nr_num=nr_num,
        start_date=data.get('start_date'),
    )
