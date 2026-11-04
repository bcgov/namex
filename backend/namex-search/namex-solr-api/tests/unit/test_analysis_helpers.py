"""Tests for the solr analysis stem-map helpers."""
from typing import ClassVar
from unittest.mock import Mock

import pytest

from namex_solr_api.services.namex_solr.utils.analysis_helpers import (
    STEMMED_AGRO_FIELD_TYPE,
    analyze_stemmed_agro_stem_map,
    analyze_stemmed_agro_token_map,
    analyze_stemmed_agro_token_stems,
    build_stem_map,
    parse_stemmed_tokens,
    stem_phrase,
    stem_synonym_payload,
)


def _analysis_response(tokens: list[str]) -> dict:
    """Return a minimal analysis/field response whose final index step yields the tokens."""
    return {
        "analysis": {
            "field_types": {
                STEMMED_AGRO_FIELD_TYPE: {
                    "index": [[{"text": token} for token in tokens]]
                }
            }
        }
    }


class TestParseStemmedTokens:
    def test_happy_path(self):
        assert parse_stemmed_tokens(_analysis_response(["pacif", "worker"])) == ["pacif", "worker"]

    def test_empty_response(self):
        assert parse_stemmed_tokens({}) == []

    def test_malformed_last_step(self):
        response = {"analysis": {"field_types": {STEMMED_AGRO_FIELD_TYPE: {"index": ["oops"]}}}}
        assert parse_stemmed_tokens(response) == []


class TestBuildStemMap:
    def test_happy_path(self):
        assert build_stem_map(["workers", "pacific"], ["worker", "pacif"]) == {
            "workers": "worker",
            "pacific": "pacif",
        }

    def test_count_mismatch_returns_empty(self):
        assert build_stem_map(["a", "b"], ["a"]) == {}

    def test_no_stems_returns_empty(self):
        assert build_stem_map(["a"], []) == {}


class TestAnalyzeStemmedAgroStemMap:
    def test_single_analyzer_call(self):
        solr = Mock()
        solr.analyze_field.return_value = _analysis_response(["pacif", "worker"])
        stem_map = analyze_stemmed_agro_stem_map(solr, "pacific workers")
        assert stem_map == {"pacific": "pacif", "workers": "worker"}
        assert solr.analyze_field.call_count == 1

    def test_analysis_down_returns_empty(self):
        solr = Mock()
        solr.analyze_field.return_value = {}
        assert analyze_stemmed_agro_stem_map(solr, "pacific workers") == {}

    def test_blank_value_skips_analyzer(self):
        solr = Mock()
        assert analyze_stemmed_agro_stem_map(solr, "   ") == {}
        solr.analyze_field.assert_not_called()


class TestAnalyzeStemmedAgroTokenMap:
    def test_batches_unique_tokens(self):
        solr = Mock()
        solr.analyze_field.return_value = _analysis_response(["worker", "labour", "employe"])
        stem_map = analyze_stemmed_agro_token_map(
            solr, ["Worker", "labourer", "employee", "worker"]
        )
        assert stem_map == {"worker": "worker", "labourer": "labour", "employee": "employe"}
        assert solr.analyze_field.call_count == 1
        _, kwargs = solr.analyze_field.call_args
        assert kwargs == {"timeout": 30, "fail_soft": False}

    def test_chunking(self):
        solr = Mock()
        solr.analyze_field.side_effect = [
            _analysis_response(["a", "b"]),
            _analysis_response(["c"]),
        ]
        stem_map = analyze_stemmed_agro_token_map(solr, ["a", "b", "c"], chunk_size=2)
        assert stem_map == {"a": "a", "b": "b", "c": "c"}
        expected_calls = 2  # ceil(3 tokens / chunk_size 2)
        assert solr.analyze_field.call_count == expected_calls

    def test_count_mismatch_falls_back_per_token(self):
        solr = Mock()
        solr.analyze_field.side_effect = [
            _analysis_response(["one", "two", "three"]),  # 3 stems for a 2-token chunk
            _analysis_response(["worker"]),
            _analysis_response([]),  # unmappable token stems to itself
        ]
        stem_map = analyze_stemmed_agro_token_map(solr, ["workers", "x&y"], chunk_size=5)
        assert stem_map == {"workers": "worker", "x&y": "x&y"}
        expected_calls = 3  # 1 mismatched chunk + 2 per-token retries
        assert solr.analyze_field.call_count == expected_calls

    def test_analysis_failure_propagates(self):
        solr = Mock()
        solr.analyze_field.side_effect = RuntimeError("solr down")
        with pytest.raises(RuntimeError):
            analyze_stemmed_agro_token_map(solr, ["workers"])


class TestStemSynonymPayload:
    STEM_MAP: ClassVar[dict[str, str]] = {
        "workers": "worker",
        "labourers": "labour",
        "labourer": "labour",
        "employee": "employe",
        "british": "british",
        "columbia": "columbia",
    }

    def test_multi_word_key(self):
        stemmed, skipped = stem_synonym_payload({"British Columbia": ["bc"]}, self.STEM_MAP)
        assert stemmed == {"british columbia": ["bc"]}
        assert skipped == []

    def test_members_deduped_after_stemming(self):
        stemmed, _ = stem_synonym_payload(
            {"workers": ["labourers", "labourer", "employee"]}, self.STEM_MAP
        )
        assert stemmed == {"worker": ["labour", "employe"]}

    def test_self_reference_dropped_after_stemming(self):
        stemmed, _ = stem_synonym_payload({"workers": ["workers", "worker", "employee"]}, self.STEM_MAP)
        assert stemmed == {"worker": ["employe"]}

    def test_keys_sharing_a_stem_merge(self):
        stemmed, _ = stem_synonym_payload(
            {"labourer": ["workers"], "labourers": ["employee"]}, self.STEM_MAP
        )
        assert stemmed == {"labour": ["worker", "employe"]}

    def test_overlong_key_skipped_and_reported(self):
        long_key = "x" * 60
        stemmed, skipped = stem_synonym_payload({long_key: ["workers"], "workers": []}, {})
        assert long_key not in stemmed
        assert stemmed == {"workers": []}
        assert skipped == [long_key]

    def test_empty_inputs(self):
        assert stem_synonym_payload({}, {}) == ({}, [])
        assert stem_synonym_payload({"": ["a"], "  ": []}, {}) == ({}, [])


class TestStemPhrase:
    def test_tokens_replaced_in_order(self):
        assert stem_phrase("British Columbia Workers", TestStemSynonymPayload.STEM_MAP) == "british columbia worker"

    def test_unknown_tokens_kept(self):
        assert stem_phrase("kial workers", {"workers": "worker"}) == "kial worker"


class TestAnalyzeStemmedAgroTokenStems:
    def test_bridges_surface_to_stem(self):
        solr = Mock()
        solr.analyze_field.return_value = _analysis_response(["beauti", "caleza", "inc"])
        stems = analyze_stemmed_agro_token_stems(solr, ["BEAUTY", "CALEZA", "INC"])
        assert stems == {"beauty": ["beauti"], "caleza": ["caleza"], "inc": ["inc"]}
        assert solr.analyze_field.call_count == 1

    def test_soft_fails_to_empty(self):
        solr = Mock()
        solr.analyze_field.side_effect = RuntimeError("solr down")
        assert analyze_stemmed_agro_token_stems(solr, ["beauty"]) == {}
