"""Unit tests for ticket 34730 conflict initials query normalization."""

import inspect

import pytest

from namex_solr_api.config import Config
from namex_solr_api.resources.v1 import search
from namex_solr_api.services.base_solr.utils.formatting_helpers import prep_query_str
from namex_solr_api.services.namex_solr import NamexSolr
from namex_solr_api.services.namex_solr.doc_models import NameField
from namex_solr_api.services.namex_solr.utils.formatting_helpers import (
    normalize_conflict_initials,
    prep_query_str_namex,
    remove_designation_tokens,
    strip_trailing_designations,
)
from namex_solr_api.services.namex_solr.utils.namex_search_helper import namex_search

H_EQUIVALENTS = [
    "HH INVESTMENTS",
    "H H INVESTMENTS",
    "H&H INVESTMENTS",
    "H.H. INVESTMENTS",
    "H & H INVESTMENTS",
    "H. & H. INVESTMENTS",
]

JM_EQUIVALENTS = [
    "JM HOLDINGS",
    "J.M. HOLDINGS",
    "J&M HOLDINGS",
    "J & M HOLDINGS",
    "J. & M. HOLDINGS",
]


def conflict_terms(name: str) -> list[str]:
    """Mirror possible-conflict value prep: normalize initials, then existing prep/split."""
    return prep_query_str(normalize_conflict_initials(name), "replace").split()


def conflict_match_terms(name: str) -> list[str]:
    """Mirror conflict AND-term prep: initials, then DESIGNATIONS token skip."""
    prepped = prep_query_str(normalize_conflict_initials(name), "replace")
    return remove_designation_tokens(prepped, Config.DEFAULT_DESIGNATIONS).split()


@pytest.mark.parametrize("name", H_EQUIVALENTS)
def test_h_initial_forms_produce_equivalent_conflict_terms(name):
    """HH / H H / H&H / H.H. / H & H / H. & H. must share conflict AND terms."""
    assert conflict_terms(name) == conflict_terms("H H INVESTMENTS")
    assert "and" not in conflict_terms(name)


def test_h_investments_stays_one_h():
    """A single H must not gain a second initial."""
    assert conflict_terms("H INVESTMENTS") == ["h", "investments"]
    assert conflict_terms("H INVESTMENTS") != conflict_terms("HH INVESTMENTS")


def test_in_business_does_not_split_in():
    """IN is a Solr English stopword and must stay a word."""
    assert conflict_terms("IN BUSINESS")[0] == "in"
    assert conflict_terms("IN BUSINESS") != ["i", "n", "business"]


def test_bc_does_not_split_to_b_c():
    """BC is the schema/NameX British Columbia token and must stay intact."""
    assert conflict_terms("BC HOLDINGS")[0] == "bc"
    assert conflict_terms("BC HOLDINGS") != ["b", "c", "holdings"]


@pytest.mark.parametrize("name", JM_EQUIVALENTS)
def test_jm_initial_forms_produce_equivalent_conflict_terms(name):
    """JM / J.M. / J&M / J & M / J. & M. must share conflict AND terms."""
    assert conflict_terms(name) == ["j", "m", "holdings"]


def test_jmj_stays_three_initials():
    """J.M.J. must not collapse to JM."""
    assert conflict_terms("J.M.J. HOLDINGS") == ["j", "m", "j", "holdings"]
    assert conflict_terms("J.M.J. HOLDINGS") != conflict_terms("J.M. HOLDINGS")


def test_possible_conflict_names_normalizes_before_prep():
    """Normalizer and DESIGNATIONS skip run on the conflict query path only; raw value stays for ranking."""
    source = inspect.getsource(search.possible_conflict_names)
    assert 'value = query_json.get("value")' in source
    assert 'prep_query_str_namex(normalize_conflict_initials(value), "replace")' in source
    assert "remove_designation_tokens(" in source
    assert "get_name_search_full_query_boost(value)" in source
    assert "value = normalize_conflict_initials(" not in source
    assert "value = remove_designation_tokens(" not in source


def test_nrs_does_not_use_conflict_match_prep():
    """/nrs is out of scope for conflict skip-word and initials prep.

    Token-anywhere DESIGNATIONS skip is only wrapped around possible_conflict_names.
    /nrs still calls prep_query_str_namex(value) with remove_designations=True, which
    only strips trailing designations (ltd, llc, limited liability company, ...),
    not leading BE / THE / AND.
    """
    source = inspect.getsource(search.nrs)
    assert "normalize_conflict_initials" not in source
    assert "remove_designation_tokens" not in source
    assert 'prep_query_str_namex(value)' in source
    assert "full_query_boosts=[]" in source


def test_nrs_keeps_leading_skip_words(app):
    """NR search must still require BE / THE / AND when they are not the last token."""
    with app.app_context():
        assert prep_query_str_namex("be kind").split() == ["be", "kind"]
        assert prep_query_str_namex("the holding").split() == ["the", "holding"]
        assert "and" in prep_query_str_namex("jm and holding").split()
        assert prep_query_str_namex("kind ltd").split() == ["kind"]
        assert prep_query_str_namex("kind llc").split() == ["kind"]
        assert prep_query_str_namex("kind limited liability company").split() == ["kind"]


def test_remove_designation_tokens_drops_be_from_match_prep():
    """BE KIND match terms are KIND; the skipped word is still available for ranking."""
    designations = ["be", "the", "and", "ltd", "ltd.", "o", "on"]
    assert remove_designation_tokens("be kind", designations) == "kind"
    assert remove_designation_tokens("be kind ltd.", designations) == "kind"
    assert remove_designation_tokens("bekind", designations) == "bekind"
    assert remove_designation_tokens("hello", designations) == "hello"


def test_boosts_keep_raw_be_kind():
    """Ranking boosts must see the original phrase, not the skip-filtered match string."""
    boosts = NamexSolr.get_name_search_full_query_boost("be kind")
    boost_values = [item["value"] for item in boosts if "value" in item]
    assert any("be kind" in value for value in boost_values)
    assert all(value != "kind" for value in boost_values)
    assert not any(item.get("values") for item in boosts)


def test_nrs_trailing_strip_keeps_legal_designations():
    """/nrs trailing strip still removes the old Solr legal-designation fallback.

    Multi-word phrases are stripped as a unit. Skip tokens like o/on must not
    clip hello/boston. Conflict token skip must not treat French 'a' as a skip word.
    """
    designations = Config.DEFAULT_DESIGNATIONS
    assert strip_trailing_designations("foo limited liability company", designations) == "foo"
    assert strip_trailing_designations("foo limited liability partnership", designations) == "foo"
    assert strip_trailing_designations("foo unlimited liability company", designations) == "foo"
    assert strip_trailing_designations("foo llc", designations) == "foo"
    assert strip_trailing_designations("foo llp", designations) == "foo"
    assert strip_trailing_designations("foo sencrl", designations) == "foo"
    assert strip_trailing_designations("kind ltd inc", designations) == "kind"
    assert strip_trailing_designations("hello", designations) == "hello"
    assert strip_trailing_designations("boston", designations) == "boston"
    assert strip_trailing_designations("be kind", designations) == "be kind"

    assert remove_designation_tokens("a holding", designations) == "a holding"
    assert remove_designation_tokens("foo llc", designations) == "foo"
    assert "partnership" not in {
        token for token in designations if " " not in token
    }


def test_vaults_designations_uses_onepassword_ref():
    """Deployed DESIGNATIONS must be injected from 1Password like the other vaults lines."""
    from pathlib import Path

    vaults_path = Path(__file__).resolve().parents[2] / "devops" / "vaults.gcp.env"
    designations_line = next(
        line for line in vaults_path.read_text(encoding="utf-8").splitlines()
        if line.startswith("DESIGNATIONS=")
    )
    assert designations_line == 'DESIGNATIONS="op://solr/$APP_ENV/namex-search/DESIGNATIONS"'
