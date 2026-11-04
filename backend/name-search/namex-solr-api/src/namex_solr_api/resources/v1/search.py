# TODO: add search endpoints replicating namex queries ? Maybe don't need this
"""Exposes all of the search endpoints in Flask-Blueprint style."""
import re
from dataclasses import replace
from http import HTTPStatus

from flask import Blueprint, current_app, jsonify, request
from flask.globals import request_ctx
from flask_cors import cross_origin

from namex_solr_api.exceptions import exception_response
from namex_solr_api.models import SearchHistory, User
from namex_solr_api.services import jwt, solr
from namex_solr_api.services.base_solr.utils import QueryParams
from namex_solr_api.services.namex_solr.doc_models import NameField, PCField
from namex_solr_api.services.namex_solr.utils import (
    analyze_stemmed_agro_stem_map,
    analyze_stemmed_agro_token_stems,
    apply_conflict_wildcard_boosts,
    apply_embedded_reserved_retrieve,
    apply_initials_group_exact_highlights,
    apply_leading_wildcard_rank,
    candidate_synonym_highlight_tokens,
    classify_conflict_bucket,
    hyphen_glued_tokens,
    keep_family_synonym_highlights,
    mark_wildcard_constant_score_boosts,
    namex_search,
    normalize_conflict_initials,
    normalize_nr_num,
    outer_wildcard_constant_score_terms,
    parse_conflict_wildcard,
    prep_query_str_namex,
    rank_conflict_docs,
    remove_designation_tokens,
    retrieve_synonym_families_by_term,
    visible_conflict_bucket,
)

bp = Blueprint("SEARCH", __name__, url_prefix="/search")


def _conflict_solr_search(params: QueryParams, is_strict: bool, max_highlighted_docs: int):
    if params.rows <= max_highlighted_docs:
        results = namex_search(params, solr, True, is_strict)
        return results, results.get("highlighting", {})

    results = namex_search(replace(params, highlighted_fields=[]), solr, True, is_strict)
    solr_highlighting: dict[str, dict[str, list[str]]] = {}
    highlight_rows = min(params.rows, max_highlighted_docs)
    if highlight_rows > 0:
        highlight_results = namex_search(
            replace(params, rows=highlight_rows),
            solr,
            True,
            is_strict,
        )
        solr_highlighting = highlight_results.get("highlighting", {})
    return results, solr_highlighting


@bp.post("/possible-conflict-names")
@cross_origin(origins="*")
@jwt.requires_auth
def possible_conflict_names():  # noqa: PLR0912, PLR0915
    """Return a list of possible conflict name results from solr."""
    try:
        # NOTE: request_ctx.current_user is set by jwt.requires_auth
        user = User.get_or_create_user_by_jwt(request_ctx.current_user)
        request_json = request.json
        # TODO: validate request
        # if errors:
        #     return bad_request_response("Errors processing request.", errors)  # noqa: ERA001

        # set base query params
        query_json: dict = request_json.get("query", {})
        value = query_json.get("value")

        wildcard = parse_conflict_wildcard(value)
        value = wildcard.value
        normalized_nr_num = normalize_nr_num(query_json.get(PCField.NR_NUM.value, "")) or ""
        query = {
            "value": remove_designation_tokens(prep_query_str_namex(normalize_conflict_initials(value), "replace")),
            PCField.CORP_NUM_Q.value: prep_query_str_namex(query_json.get(PCField.CORP_NUM.value, "")),
            PCField.NR_NUM_Q.value: prep_query_str_namex(normalized_nr_num)
        }
        # set faceted category params
        categories_json: dict = request_json.get("categories", {})
        # TODO: verify these states
        conflict_states = ["ACTIVE", "APPROVED", "CONDITION", "ACT", "LIQ"]
        categories = {
            PCField.JURISDICTION: categories_json.get(PCField.JURISDICTION.value, None),
            PCField.STATE: categories_json.get(PCField.STATE.value, conflict_states)
        }
        # set nested child query params
        child_query = {
            NameField.NAME_Q_EXACT_PHRASE.value: prep_query_str_namex(query_json.get(NameField.NAME.value, ""), None, False)
        }
        # set nested child faceted category params
        # TODO: verify these states
        conflict_name_states = ["A", "C", "CORP"]
        child_categories = {
            NameField.NAME_STATE: categories_json.get(NameField.NAME_STATE.value, conflict_name_states)
        }

        strict = request_json.get("strict", False)
        start = request_json.get("start", solr.default_start)
        rows = request_json.get("rows", solr.default_rows)
        try:
            strict = bool(strict)
        except (TypeError, ValueError):
            strict = False
        try:
            start = int(start)
        except (TypeError, ValueError):
            start = solr.default_start
        try:
            rows = max(0, int(rows))
            if not strict:
                # TODO: return 400 if request is asking for too many rows - could mess up their paging
                # temporary setting for testing so that non strict doesn't overload the non strict search
                max_rows = current_app.config['SOLR_SVC_NAMEX_MAX_ROWS']
                rows = min(max_rows, rows)
        except (TypeError, ValueError):
            rows = solr.default_rows

        highlighted_fields = [NameField.NAME_Q_SINGLE, NameField.NAME_Q_STEM_HIGHLIGHT, NameField.NAME_Q_PHON_EN, NameField.NAME_Q_SYN]
        max_highlighted_docs = max(
            0,
            int(current_app.config["SOLR_SVC_NAMEX_MAX_HIGHLIGHTED_DOCS"]),
        )
        constant_score_terms = outer_wildcard_constant_score_terms(wildcard, query["value"])
        full_query_boosts = mark_wildcard_constant_score_boosts(
            apply_conflict_wildcard_boosts(
                solr.get_name_search_full_query_boost(value),
                wildcard.leading,
            ),
            constant_score_terms,
        )

        # the Solr analyzer call for stems of all the terms in the query
        stems_by_term = analyze_stemmed_agro_stem_map(solr, query["value"])

        params = QueryParams(
            query=query,
            rows=rows,
            start=start,
            categories=categories,
            child_query=child_query,
            child_categories=child_categories,
            fields=solr.resp_fields_nested,
            highlighted_fields=highlighted_fields,
            query_boost_fields={
                NameField.NAME_Q_AGRO: 2,
                NameField.NAME_Q_SINGLE: 2,
                NameField.NAME_Q_XTRA: 2,
                NameField.NAME_Q_SYN: 2
            },
            query_fields={
                NameField.NAME_Q: "child",
                NameField.NAME_Q_AGRO: "child",
                NameField.NAME_Q_STEM_HIGHLIGHT: "child",
                NameField.NAME_Q_SINGLE: "child",
                NameField.NAME_Q_XTRA: "child",
                NameField.NAME_Q_PHON_EN: "child",
            },
            query_fuzzy_fields={
                NameField.NAME_Q: {"short": 1, "long": 2},
                NameField.NAME_Q_AGRO: {"short": 1, "long": 2},
                NameField.NAME_Q_SINGLE: {"short": 0, "long": 2}
            },
            query_synonym_fields={
                NameField.NAME_Q_SYN: "child"
            },
            full_query_boosts=full_query_boosts,
            # TODO: add this as LD flag ? names ticket: #32885
            exclude_sub_types=["DBA", "FR", "GP", "LL", "LP"],
            constant_score_terms=constant_score_terms,
            stemmed_terms_map=stems_by_term,
        )

        params = apply_embedded_reserved_retrieve(params, solr, strict, start)
        results, solr_highlighting = _conflict_solr_search(params, strict, max_highlighted_docs)
        docs = []
        query_value = params.query.get("value", "")
        glued_tokens = hyphen_glued_tokens(value)
        query_terms_list = query_value.split()
        query_stems = (
            [stems_by_term.get(term, term) for term in query_terms_list]
            if stems_by_term
            else []
        )
        families_by_term = retrieve_synonym_families_by_term(
            query_value,
            solr.query_builder,
            NameField.NAME_Q_SYN,
            query_stems,
        )
        query_stems_by_term = {
            term: {stems_by_term[term]}
            for term in query_terms_list
            if stems_by_term.get(term)
        }
        # DB synonyms are stored as agro stems, so the family set is the stem set
        synonym_family = {
            token
            for part in families_by_term.values()
            for token in part
        }
        # doc names/highlights are surface forms while the family holds stems
        # one analyzer call bridges them for highlight filtering and bucket/rank family coverage
        result_docs = results.get("response", {}).get("docs") or []
        doc_token_stems = {}
        if synonym_family and result_docs:
            doc_tokens = set()
            for result in result_docs:
                doc_tokens.update(
                    candidate_synonym_highlight_tokens(
                        solr_highlighting.get(result[NameField.UNIQUE_KEY.value], {}).get(NameField.NAME_Q_SYN.value, []) or [],
                        result.get("name") or "",
                    )
                )
            doc_token_stems = analyze_stemmed_agro_token_stems(solr, sorted(doc_tokens))
        for result in result_docs:
            def split_highlights(highlights: list[str]):
                """Split list of strings into list of single terms, removing HTML tags"""
                resp = []
                for highlight in highlights:
                    clean = re.sub(r'<[^>]+>', '', highlight)
                    resp += [term for term in clean.upper().split(" ") if term]
                return resp

            highlight_raw = solr_highlighting.get(result[NameField.UNIQUE_KEY.value], {})
            exact_highlights = []
            stem_highlights = []
            phonetic_highlights = []
            synonym_highlights = []
            if exact_highlights_full_terms := highlight_raw.get(NameField.NAME_Q_SINGLE.value, []):
                exact_highlights_full_terms = split_highlights(exact_highlights_full_terms)
                for term in params.query["value"].split(" "):
                    if any(x for x in exact_highlights_full_terms if term.upper() in x):
                        exact_highlights.append(term.upper())
            exact_highlights = apply_initials_group_exact_highlights(
                exact_highlights,
                params.query["value"].split(),
                result.get("name") or "",
            )
            if stem_highlights := highlight_raw.get(NameField.NAME_Q_STEM_HIGHLIGHT.value, []):
                stem_highlights = [x for x in split_highlights(stem_highlights) if x not in (exact_highlights)]
            if phonetic_highlights := highlight_raw.get(NameField.NAME_Q_PHON_EN.value, []):
                other_highlights = exact_highlights + stem_highlights
                phonetic_highlights = [x.upper() for x in split_highlights(phonetic_highlights) if x.upper() not in other_highlights and x.strip()]
            other_highlights = exact_highlights + stem_highlights + phonetic_highlights
            synonym_candidates = candidate_synonym_highlight_tokens(
                highlight_raw.get(NameField.NAME_Q_SYN.value, []) or [],
                result.get("name") or "",
            )
            synonym_highlights = [
                token
                for token in keep_family_synonym_highlights(
                    synonym_candidates,
                    synonym_family,
                    None,
                    doc_token_stems,
                )
                if token not in other_highlights
            ]
            bucket = visible_conflict_bucket(
                classify_conflict_bucket(
                    query_value,
                    result.get("name") or "",
                    families_by_term,
                    None,
                    query_stems_by_term,
                    doc_token_stems,
                    glued_tokens,
                )
            )
            docs.append({
                **result,
                "name": result["name"].upper(),
                "bucket": bucket,
                "highlighting": {
                    "exact": list(set(exact_highlights)),
                    "stems": list(set(stem_highlights)),
                    "phonetic": list(set(phonetic_highlights)),
                    "synonyms": list(set(synonym_highlights))
                }
            })
        docs = rank_conflict_docs(
            docs,
            query_value,
            families_by_term,
            None,
            query_stems_by_term,
            doc_token_stems,
            glued_tokens,
        )
        if wildcard.leading and not wildcard.trailing and start == 0:
            docs = apply_leading_wildcard_rank(docs, value)
        # save search in the db
        SearchHistory(
            query=request_json,
            results=docs,
            submitter_id=user.id,
        ).save()

        response = {
            "searchResults": {
                "queryInfo": {
                    "categories": {
                        **categories,
                        **child_categories
                    },
                    "query": {
                        "value": query["value"],
                        PCField.CORP_NUM.value: query[PCField.CORP_NUM_Q.value],
                        PCField.NR_NUM.value: query[PCField.NR_NUM_Q.value],
                        NameField.NAME.value: child_query[NameField.NAME_Q_EXACT_PHRASE.value]
                    },
                    "rows": rows or solr.default_rows,
                    "start": start or solr.default_start,
                },
                "totalResults": len(docs),
                "results": docs
            },
        }
        return jsonify(response), HTTPStatus.OK

    except Exception as exception:
        return exception_response(exception)


@bp.post("/nrs")
@cross_origin(origins="*")
@jwt.requires_auth
def nrs():
    """Return a list of Name Request results from solr."""
    try:
        request_json = request.json
        # TODO: validate request
        # if errors:
        #     return bad_request_response("Errors processing request.", errors)  # noqa: ERA001

        # set base query params
        query_json: dict = request_json.get("query", {})
        value = query_json.get("value")
        normalized_nr_num = normalize_nr_num(query_json.get(PCField.NR_NUM.value, "")) or ""
        query = {
            "value": prep_query_str_namex(value),
            PCField.CORP_NUM_Q.value: prep_query_str_namex(query_json.get(PCField.CORP_NUM.value, "")),
            PCField.NR_NUM_Q.value: prep_query_str_namex(normalized_nr_num)
        }
        # set faceted category params
        categories_json: dict = request_json.get("categories", {})
        categories = {
            PCField.JURISDICTION: categories_json.get(PCField.JURISDICTION.value, None),
            PCField.STATE: categories_json.get(PCField.STATE.value, None),
            PCField.TYPE: ["NR"]
        }
        # set nested child query params
        child_query = {
            NameField.NAME_Q_SINGLE.value: prep_query_str_namex(query_json.get(NameField.NAME.value, ""))
        }
        # set nested child faceted category params
        child_categories = {
            NameField.NAME_STATE: categories_json.get(NameField.NAME_STATE.value, None)
        }

        start = request_json.get("start", solr.default_start)
        rows = request_json.get("rows", solr.default_rows)
        strict = request_json.get("strict", True)
        try:
            strict = bool(strict)
        except (TypeError, ValueError):
            strict = True

        params = QueryParams(
            query=query,
            rows=rows,
            start=start,
            categories=categories,
            child_query=child_query,
            child_categories=child_categories,
            fields=solr.resp_fields,
            highlighted_fields=[],
            query_boost_fields={
                NameField.NAME_Q: 2,
                NameField.NAME_Q_AGRO: 2,
                NameField.NAME_Q_SINGLE: 2,
                NameField.NAME_Q_XTRA: 2
            },
            query_fields={
                PCField.NR_NUM_Q: "parent",
                PCField.NR_NUM_Q_EDGE: "parent",
                NameField.NAME_Q: "child",
                NameField.NAME_Q_AGRO: "child",
                NameField.NAME_Q_SINGLE: "child",
                NameField.NAME_Q_XTRA: "child",
            },
            query_fuzzy_fields={
                NameField.NAME_Q: {"short": 1, "long": 2},
                NameField.NAME_Q_AGRO: {"short": 1, "long": 2},
                NameField.NAME_Q_SINGLE: {"short": 1, "long": 2}
            },
            query_synonym_fields={
                NameField.NAME_Q_SYN: "child"
            },
            # NOTE: add items to this to improve ordering as needed
            full_query_boosts=[],
            exclude_sub_types=[]
        )

        results = namex_search(params, solr, False, strict)
        docs = results.get("response", {}).get("docs")

        response = {
            "searchResults": {
                "queryInfo": {
                    "categories": {
                        **categories,
                        **child_categories
                    },
                    "query": {
                        "value": query["value"],
                        PCField.CORP_NUM.value: query[PCField.CORP_NUM_Q.value],
                        PCField.NR_NUM.value: query[PCField.NR_NUM_Q.value],
                        NameField.NAME.value: child_query[NameField.NAME_Q_SINGLE.value]
                    },
                    "rows": rows or solr.default_rows,
                    "start": start or solr.default_start,
                },
                "totalResults": results.get("response", {}).get("numFound"),
                "results": docs,
            },
        }
        return jsonify(response), HTTPStatus.OK

    except Exception as exception:
        return exception_response(exception)
