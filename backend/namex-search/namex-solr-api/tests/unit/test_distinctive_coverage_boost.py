"""Regression contract for the distinctive-coverage ranking boost.

Raises names that cover every remaining distinctive term (exact / fuzzy /
phonetic). Synonym-only coverage (ltd ≈ holdings) is not part of the clause.
"""

from __future__ import annotations

import inspect

import pytest

from namex_solr_api.config import Config
from namex_solr_api.resources.v1 import search
from namex_solr_api.services.namex_solr import NamexSolr
from namex_solr_api.services.namex_solr.utils.formatting_helpers import (
    DISTINCTIVE_COVERAGE_BOOST_WEIGHT,
    INITIALS_GROUP_BOOST_WEIGHT,
    build_distinctive_coverage_boosts,
    conflict_match_prep_terms,
)
from namex_solr_api.services.namex_solr.utils.namex_search_helper import (
    format_full_query_boost,
    namex_search,
)


def match_prep(raw: str) -> list[str]:
    return conflict_match_prep_terms(raw, Config.DEFAULT_DESIGNATIONS)


def distinctive_items(raw: str) -> list[dict]:
    return [
        item
        for item in NamexSolr.get_name_search_full_query_boost(raw)
        if item.get("term_clauses")
    ]


MIN_DISTINCTIVE_TERMS = 2

EMITS_CLAUSE = [
    "katherine holdings",
    "kathy enterprises",
    "KATHERINE HOLDINGS LTD",
    "pacific west construction",
]

NO_CLAUSE = [
    "katherine",
    "kathy",
    "be kind",
    "KIND",
    "J.R.M.",
    "J R M INVESTMENTS",
    "VAN INVESTMENTS",
]


@pytest.mark.parametrize("raw", EMITS_CLAUSE)
def test_two_plus_distinctive_terms_emit_boost(raw):
    items = build_distinctive_coverage_boosts(match_prep(raw))
    assert len(items) == 1
    assert items[0]["boost"] == DISTINCTIVE_COVERAGE_BOOST_WEIGHT
    assert len(items[0]["term_clauses"]) >= MIN_DISTINCTIVE_TERMS
    joined = " ".join(items[0]["term_clauses"])
    assert "name_q_phon_en:" in joined
    assert "name_q_synonym" not in joined


@pytest.mark.parametrize("raw", NO_CLAUSE)
def test_single_or_short_terms_emit_nothing(raw):
    assert build_distinctive_coverage_boosts(match_prep(raw)) == []


def test_katherine_holdings_uses_long_fuzzy():
    items = build_distinctive_coverage_boosts(match_prep("katherine holdings"))
    clauses = items[0]["term_clauses"]
    assert any("name_q:katherine~2" in clause for clause in clauses)
    assert any("name_q:holdings~2" in clause for clause in clauses)
    assert all("name_q_synonym" not in clause for clause in clauses)


def test_kathy_enterprises_uses_short_fuzzy():
    items = build_distinctive_coverage_boosts(match_prep("kathy enterprises"))
    clauses = items[0]["term_clauses"]
    assert any("name_q:kathy~1" in clause for clause in clauses)
    assert any("name_q_phon_en:kathy" in clause for clause in clauses)
    assert all("name_q:kathy~2" not in clause for clause in clauses)


def test_ltd_is_not_a_required_distinctive_term():
    items = build_distinctive_coverage_boosts(match_prep("katherine holdings ltd"))
    joined = " ".join(items[0]["term_clauses"])
    assert "katherine" in joined
    assert "holdings" in joined
    assert "ltd" not in joined


def test_render_term_clauses_is_and_of_ors():
    info = {
        "term_clauses": [
            "(name_q:katherine OR name_q_phon_en:katherine OR name_q:katherine~2)",
            "(name_q:holdings OR name_q_phon_en:holdings OR name_q:holdings~2)",
        ],
        "boost": DISTINCTIVE_COVERAGE_BOOST_WEIGHT,
    }
    rendered = format_full_query_boost(info)
    assert rendered.startswith("((")
    assert rendered.endswith(")^80)")
    assert " AND " in rendered
    assert "name_q_synonym" not in rendered


def test_render_keeps_phrase_and_initials_shapes():
    from namex_solr_api.services.namex_solr.doc_models import NameField

    phrase = {"field": NameField.NAME_Q_EXACT, "value": "be kind", "boost": "3"}
    initials = {
        "field": NameField.NAME_Q,
        "values": ["jrm", "investments"],
        "boost": INITIALS_GROUP_BOOST_WEIGHT,
    }
    assert format_full_query_boost(phrase) == '(name_q_exact:"be kind"^3)'
    assert format_full_query_boost(initials) == "((name_q:jrm AND name_q:investments)^80)"


@pytest.mark.parametrize("raw", EMITS_CLAUSE)
def test_builder_appends_distinctive_clause(raw, app):
    app.config["DESIGNATIONS"] = list(Config.DEFAULT_DESIGNATIONS)
    items = distinctive_items(raw)
    assert len(items) == 1
    assert items[0]["boost"] == DISTINCTIVE_COVERAGE_BOOST_WEIGHT


@pytest.mark.parametrize("raw", NO_CLAUSE)
def test_builder_does_not_append_distinctive_clause(raw, app):
    app.config["DESIGNATIONS"] = list(Config.DEFAULT_DESIGNATIONS)
    assert distinctive_items(raw) == []


def test_builder_keeps_classic_and_initials_beside_distinctive(app):
    app.config["DESIGNATIONS"] = list(Config.DEFAULT_DESIGNATIONS)
    boosts = NamexSolr.get_name_search_full_query_boost("J.R.M. INVESTMENTS")
    classic = [item for item in boosts if "value" in item]
    initials = [item for item in boosts if item.get("values")]
    distinctive = [item for item in boosts if item.get("term_clauses")]
    assert classic
    assert initials
    assert distinctive == []


def test_conflict_call_site_still_passes_raw_value():
    source = inspect.getsource(search.possible_conflict_names)
    assert "get_name_search_full_query_boost(value)" in source


def test_nrs_still_has_empty_boosts():
    source = inspect.getsource(search.nrs)
    assert "full_query_boosts=[]" in source
    assert "build_distinctive_coverage_boosts" not in source


def test_helper_still_or_appends_formatted_boosts():
    helper = inspect.getsource(namex_search)
    assert "OR {format_full_query_boost(info)}" in helper
    boost_builder = inspect.getsource(NamexSolr.get_name_search_full_query_boost)
    assert "build_distinctive_coverage_boosts" in boost_builder
    assert "build_initials_group_boosts" in boost_builder
