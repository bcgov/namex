"""NameX solr search functions."""
import re
from dataclasses import replace

from namex_solr_api.services.base_solr.utils import QueryParams
from namex_solr_api.services.namex_solr import NamexSolr
from namex_solr_api.services.namex_solr.doc_models import NameField, PCField

from .add_category_filters import add_category_filters
from .analysis_helpers import analyze_stemmed_agro_tokens
from .formatting_helpers import (
    reserved_coverage_params,
    reserved_glued_concat_query,
    reserved_prefix_params,
    should_run_reserved_coverage,
)


def format_full_query_boost(info: dict) -> str:
    """Render one full-query boost clause.

    Accepts three shapes: term_clauses (AND of pre-built clauses), values
    (AND of field:token), or value with an optional fuzzy width.
    """
    boost = info["boost"]
    score_op = "^=" if info.get("constant_score") else "^"
    if term_clauses := info.get("term_clauses"):
        inner = " AND ".join(term_clauses)
        return f"(({inner}){score_op}{boost})"
    field = info["field"].value
    if values := info.get("values"):
        inner = " AND ".join(f"{field}:{token}" for token in values)
        return f"(({inner}){score_op}{boost})"
    clause = f'{field}:"{info["value"]}"'
    if fuzzy := info.get("fuzzy"):
        clause += f"~{fuzzy}"
    return f"({clause}{score_op}{boost})"


def build_namex_query_payload(
    params: QueryParams,
    solr: NamexSolr,
    is_name_search: bool,
    is_strict: bool,
    clause_bridge: str | None = None,
) -> dict[str, list[str]]:
    if clause_bridge is None:
        clause_bridge = "AND" if is_strict else "OR"
    value = params.query.get("value", "")
    if (stem_map := params.stemmed_terms_map) is not None:
        # one upstream analyzer call serves every lane (lane values are term subsets)
        stemmed_terms = [stem_map.get(term, term) for term in value.split()]
    else:
        stemmed_terms = analyze_stemmed_agro_tokens(solr, value)
    return solr.query_builder.build_base_query(
        query=params.query,
        fields=params.query_fields,
        boost_fields=params.query_boost_fields,
        fuzzy_fields=params.query_fuzzy_fields,
        synonym_fields=params.query_synonym_fields,
        is_child_search=is_name_search,
        clause_bridge=clause_bridge,
        stemmed_terms=stemmed_terms,
        synonym_as_raw=True,
        constant_score_terms=frozenset(params.constant_score_terms or []),
    )


def query_with_full_boosts(
    params: QueryParams, solr: NamexSolr, is_name_search: bool, is_strict: bool
) -> str:
    payload = build_namex_query_payload(params, solr, is_name_search, is_strict)
    for info in params.full_query_boosts:
        payload["query"] += f" OR {format_full_query_boost(info)}"
    return payload["query"]


def join_embedded_conflict_query(or_query: str, reserved_queries: list[str]) -> str | None:
    if not or_query or not reserved_queries:
        return None
    return " OR ".join(f"({part})" for part in [or_query, *reserved_queries])


def embed_reserved_retrieve_query(params: QueryParams, solr: NamexSolr, is_strict: bool, start: int) -> str | None:
    if not should_run_reserved_coverage(is_strict, start, params.query.get("value", "")):
        return None
    reserved = []
    if prefix_params := reserved_prefix_params(params):
        reserved.append(query_with_full_boosts(prefix_params, solr, True, True))
    if coverage_params := reserved_coverage_params(params):
        reserved.append(query_with_full_boosts(coverage_params, solr, True, True))
    if concat_query := reserved_glued_concat_query(params.query.get("value", ""), solr=solr):
        reserved.append(concat_query)
    return join_embedded_conflict_query(query_with_full_boosts(params, solr, True, False), reserved)


def apply_embedded_reserved_retrieve(params: QueryParams, solr: NamexSolr, is_strict: bool, start: int) -> QueryParams:
    if fat_query := embed_reserved_retrieve_query(params, solr, is_strict, start):
        return replace(params, override_query=fat_query)
    return params


def namex_search(params: QueryParams, solr: NamexSolr, is_name_search: bool, is_strict: bool = True):
    """Return the list of possible conflicts from Solr that match the query."""
    initial_queries = build_namex_query_payload(
        params,
        solr,
        is_name_search,
        is_strict,
        clause_bridge="AND" if is_strict else "OR",
    )
    for info in params.full_query_boosts:
        initial_queries["query"] += f" OR {format_full_query_boost(info)}"
    built_query = initial_queries["query"]
    if override_query := getattr(params, "override_query", None):
        initial_queries["query"] = override_query

    highlight_query = built_query if params.highlighted_fields else None

    # add defaults
    parent_field = NameField.PARENT_TYPE.value if is_name_search else PCField.TYPE.value
    solr_payload = {
        **initial_queries,
        "queries": {
            "parents": f"{parent_field}:*",
            "parentFilters": " AND ".join(initial_queries["filter"]),
        },
        "fields": params.fields
    }
    if params.highlighted_fields:
        solr_payload = {
            **solr_payload,
            **namex_search_highlighting(params, highlight_query)
        }
    # base doc faceted filters
    add_category_filters(solr_payload=solr_payload,
                         categories=params.categories,
                         is_child=False,
                         is_child_search=is_name_search,
                         solr=solr)
    # child filter queries
    if child_query := solr.query_builder.build_child_query(params.child_query, is_name_search, True):
        solr_payload["filter"].append(child_query)

    # exclude firms
    if len(params.exclude_sub_types) > 0:
        exclude_sub_types = f"({') OR ('.join(params.exclude_sub_types)})"
        solr_payload["filter"].append(f"-sub_type:({exclude_sub_types})")
        solr_payload["filter"].append(f"-parent_sub_type:({exclude_sub_types})")

    # child doc faceted filter queries
    add_category_filters(solr_payload=solr_payload,
                         categories=params.child_categories,
                         is_child=True,
                         is_child_search=is_name_search,
                         solr=solr)

    resp: dict[str, dict[str, dict[str, list[str]]]] = solr.query(solr_payload, params.start, params.rows)
    parsed_highlighting = {}
    if solr_highlighting := resp.get('highlighting'):
        for result_id, result in solr_highlighting.items():
            parsed_highlighting[result_id] = {}
            for field_enum in params.highlighted_fields:
                if field_highlights := result.get(field_enum.value):
                    parsed_highlighting[result_id][field_enum.value] = []
                    for highlight in field_highlights:
                        parsed_highlighting[result_id][field_enum.value] += namex_search_parse_highlighting(highlight)
    resp['highlighting'] = parsed_highlighting
    return resp


def namex_search_highlighting(params: QueryParams, highlight_query: str | None = None):
    """Return the the highlighting params for the query."""
    hl_params = {
        "hl": "on",
        "hl.method": "unified",
        "hl.requireFieldMatch": "true",
        "hl.tag.pre": "|||",
        "hl.tag.post": "|||",
        "hl.fl": ",".join([x.value for x in params.highlighted_fields]),
    }
    if highlight_query:
        hl_params["hl.q"] = highlight_query
    return {"params": hl_params}


def namex_search_parse_highlighting(highlighted_value: str) -> list[str]:
    """Return the parsed list of highlighted terms."""
    highlighted_rgx = r'\|\|\|([^\|]*)\|\|\|'
    return re.findall(highlighted_rgx, highlighted_value)
