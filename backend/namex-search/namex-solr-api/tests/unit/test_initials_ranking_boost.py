"""Regression contract for the targeted initials ranking boost.

Conflict match-prep uses DEFAULT_DESIGNATIONS. AND/BE/THE/OR are not
stripped to glue initials.
"""

from __future__ import annotations

import inspect

import pytest

from namex_solr_api.config import Config
from namex_solr_api.resources.v1 import search
from namex_solr_api.services.namex_solr import NamexSolr
from namex_solr_api.services.namex_solr.doc_models import NameField
from namex_solr_api.services.namex_solr.utils.formatting_helpers import (
    INITIALS_GROUP_BOOST_WEIGHT,
    build_initials_group_boosts,
    conflict_match_prep_terms,
)
from namex_solr_api.services.namex_solr.utils.namex_search_helper import (
    format_full_query_boost,
    namex_search,
)


def match_prep(raw: str) -> list[str]:
    return conflict_match_prep_terms(raw, Config.DEFAULT_DESIGNATIONS)


def initials_items(raw: str) -> list[dict]:
    return [item for item in NamexSolr.get_name_search_full_query_boost(raw) if item.get("values")]


def group_values(items: list[dict]) -> list[list[str]]:
    return [item["values"] for item in items]


LOCKED_CLAUSES = [
    ("J.R.M. INVESTMENTS", ["jrm", "investments"]),
    ("J R M INVESTMENTS", ["jrm", "investments"]),
    ("INVESTMENTS J R M", ["jrm", "investments"]),
    ("PACIFIC J R M INVESTMENTS", ["jrm", "pacific", "investments"]),
    ("H&H INVESTMENTS", ["hh", "investments"]),
    ("J R M SMITH H H INVESTMENTS", ["jrm", "hh", "smith", "investments"]),
    ("J.R.M. INVESTMENTS LTD", ["jrm", "investments"]),
    ("J.R.M. INVESTMENTS INC", ["jrm", "investments"]),
]

NO_INITIALS_BOOST = [
    "J AND R AND M INVESTMENTS",
    "J.R.M.",
    "JRM INVESTMENTS",
    "VAN INVESTMENTS",
    "NEW WEST HOLDINGS",
    "SUN LIFE",
    "BE KIND",
]


@pytest.mark.parametrize(("raw", "expected"), LOCKED_CLAUSES)
def test_generator_locked_queries_emit_and_boost(raw, expected):
    items = build_initials_group_boosts(match_prep(raw))
    assert group_values(items) == [expected]
    assert items[0]["field"] == NameField.NAME_Q
    assert items[0]["boost"] == INITIALS_GROUP_BOOST_WEIGHT


@pytest.mark.parametrize("raw", NO_INITIALS_BOOST)
def test_generator_locked_queries_emit_nothing(raw):
    assert build_initials_group_boosts(match_prep(raw)) == []


def test_j_and_r_and_m_keeps_and_and_does_not_glue():
    """AND is not initials punctuation and is not a designation."""
    terms = match_prep("J AND R AND M INVESTMENTS")
    assert "and" in terms
    assert terms == ["j", "and", "r", "and", "m", "investments"]
    assert build_initials_group_boosts(terms) == []


def test_ltd_inc_are_not_required_boost_terms():
    for raw in ("J.R.M. INVESTMENTS LTD", "J.R.M. INVESTMENTS INC"):
        values = build_initials_group_boosts(match_prep(raw))[0]["values"]
        assert values == ["jrm", "investments"]
        assert "ltd" not in values
        assert "inc" not in values


def test_jm_does_not_generate_jrm_boost():
    items = build_initials_group_boosts(match_prep("JM INVESTMENTS"))
    assert group_values(items) == [["jm", "investments"]]
    assert "jrm" not in items[0]["values"]


def test_no_namex_filter_words_on_this_path():
    assert not hasattr(Config, "NAMEX_FILTER_WORDS")
    skip = {word.lower() for word in Config.DEFAULT_DESIGNATIONS}
    assert "and" not in skip
    assert "be" not in skip
    assert "the" not in skip
    assert "or" not in skip
    assert {"ltd", "inc"} <= skip


def test_render_values_form_is_and_group():
    info = {
        "field": NameField.NAME_Q,
        "values": ["jrm", "investments"],
        "boost": INITIALS_GROUP_BOOST_WEIGHT,
    }
    rendered = format_full_query_boost(info)
    assert rendered == "((name_q:jrm AND name_q:investments)^80)"
    assert '"jrm investments"' not in rendered
    assert "name_q_exact" not in rendered


def test_render_keeps_existing_phrase_and_fuzzy_shapes():
    phrase = {"field": NameField.NAME_Q_EXACT, "value": "be kind", "boost": "3"}
    fuzzy = {"field": NameField.NAME_Q, "value": "be kind", "boost": "5", "fuzzy": "5"}
    assert format_full_query_boost(phrase) == '(name_q_exact:"be kind"^3)'
    assert format_full_query_boost(fuzzy) == '(name_q:"be kind"~5^5)'


def test_boost_weight_is_named_constant_not_unrelated_retune():
    """Existing phrase boosts stay 2–7; initials group is a named constant."""
    classic = NamexSolr.get_name_search_full_query_boost("be kind")
    assert {item["boost"] for item in classic if "value" in item} <= {"2", "3", "5", "7"}
    assert INITIALS_GROUP_BOOST_WEIGHT == "80"


@pytest.mark.parametrize(("raw", "expected"), LOCKED_CLAUSES)
def test_builder_appends_initials_clause(raw, expected, app):
    app.config["DESIGNATIONS"] = list(Config.DEFAULT_DESIGNATIONS)
    items = initials_items(raw)
    assert group_values(items) == [expected]
    assert items[0]["field"] == NameField.NAME_Q
    assert items[0]["boost"] == INITIALS_GROUP_BOOST_WEIGHT


@pytest.mark.parametrize("raw", NO_INITIALS_BOOST)
def test_builder_does_not_append_initials_clause(raw, app):
    app.config["DESIGNATIONS"] = list(Config.DEFAULT_DESIGNATIONS)
    assert initials_items(raw) == []


def test_builder_keeps_classic_phrase_boosts_beside_initials(app):
    app.config["DESIGNATIONS"] = list(Config.DEFAULT_DESIGNATIONS)
    boosts = NamexSolr.get_name_search_full_query_boost("J.R.M. INVESTMENTS")
    classic_fields = {item["field"] for item in boosts if "value" in item}
    assert NameField.NAME_Q_EXACT in classic_fields
    assert NameField.NAME_Q in classic_fields
    exact = next(item for item in boosts if item["field"] == NameField.NAME_Q_EXACT)
    assert "j.r.m" in exact["value"]
    assert group_values([item for item in boosts if item.get("values")]) == [["jrm", "investments"]]


def test_conflict_call_site_still_passes_raw_value():
    source = inspect.getsource(search.possible_conflict_names)
    assert "get_name_search_full_query_boost(value)" in source
    assert "value = normalize_conflict_initials(" not in source


def test_nrs_still_has_empty_boosts():
    source = inspect.getsource(search.nrs)
    assert "full_query_boosts=[]" in source


def test_strict_and_nonstrict_behavior_unchanged():
    """Base match still uses is_strict AND/OR. Initials are an extra full-query boost.

    Does not claim the candidate set is unchanged: boosts are OR-appended
    onto the existing query, same as the phrase boosts.
    """
    source = inspect.getsource(search.possible_conflict_names)
    assert 'request_json.get("strict", False)' in source
    assert "SOLR_SVC_NAMEX_MAX_ROWS" in source
    helper = inspect.getsource(namex_search)
    assert 'clause_bridge="AND" if is_strict else "OR"' in helper
    assert 'OR {format_full_query_boost(info)}' in helper
    boost_builder = inspect.getsource(NamexSolr.get_name_search_full_query_boost)
    assert "build_initials_group_boosts" in boost_builder
    assert "build_distinctive_coverage_boosts" in boost_builder
