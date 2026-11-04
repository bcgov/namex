"""Tests for stemmed-key synonym matching and the single-analyzer-call threading."""
from types import SimpleNamespace
from typing import ClassVar
from unittest.mock import Mock, patch

from namex_solr_api.models import SolrSynonymList
from namex_solr_api.services.base_solr.utils import QueryParams
from namex_solr_api.services.base_solr.utils.query_builder import QueryBuilder
from namex_solr_api.services.namex_solr.doc_models import NameField, PCField
from namex_solr_api.services.namex_solr.utils.namex_search_helper import build_namex_query_payload

SYNONYM_FIELD_MAP = {NameField.NAME_Q_SYN: SolrSynonymList.Type.ALL}


def _query_builder() -> QueryBuilder:
    return QueryBuilder(
        identifier_field_values=[],
        unique_parent_field=PCField.TYPE,
        synonym_field_map=SYNONYM_FIELD_MAP,
    )


def _row(synonym: str) -> SimpleNamespace:
    return SimpleNamespace(synonym=synonym, synonym_list=[])


class TestFindSynonymTerms:
    def test_single_lookup_uses_the_stem(self):
        builder = _query_builder()
        with patch.object(
            SolrSynonymList, "find_all_beginning_with_phrase", return_value=[_row("worker")]
        ) as lookup:
            key = builder.find_synonym_terms(
                "workers", 0, ["workers"], NameField.NAME_Q_SYN, ["worker"]
            )
        assert key == ["worker"]
        lookup.assert_called_once_with("worker", SolrSynonymList.Type.ALL)

    def test_no_raw_surface_fallback(self):
        # a key that matches the surface term but not its stem is rejected
        builder = _query_builder()
        with patch.object(
            SolrSynonymList, "find_all_beginning_with_phrase", return_value=[_row("workers")]
        ):
            key = builder.find_synonym_terms(
                "workers", 0, ["workers"], NameField.NAME_Q_SYN, ["worker"]
            )
        assert key == []

    def test_multi_word_key_positional_coverage(self):
        builder = _query_builder()
        terms = ["british", "columbia", "workers"]
        stems = ["british", "columbia", "worker"]
        with patch.object(
            SolrSynonymList,
            "find_all_beginning_with_phrase",
            return_value=[_row("british"), _row("british columbia")],
        ):
            key = builder.find_synonym_terms("british", 0, terms, NameField.NAME_Q_SYN, stems)
        assert key == ["british", "columbia"]  # longest covered key wins

    def test_key_longer_than_remaining_terms_rejected(self):
        builder = _query_builder()
        with patch.object(
            SolrSynonymList, "find_all_beginning_with_phrase", return_value=[_row("british columbia")]
        ):
            key = builder.find_synonym_terms(
                "british", 0, ["british"], NameField.NAME_Q_SYN, ["british"]
            )
        assert key == []

    def test_skip_word_terms_never_lookup(self):
        builder = _query_builder()
        with patch.object(SolrSynonymList, "find_all_beginning_with_phrase") as lookup:
            assert builder.find_synonym_terms("the", 0, ["the"], NameField.NAME_Q_SYN, ["the"]) == []
        lookup.assert_not_called()


class TestSynonymFieldClause:
    def test_single_token_raw_clause(self):
        clause = QueryBuilder._synonym_field_clause(
            "name_q_synonym", "name_q_synonym", ["worker"], True
        )
        assert clause == '_query_:"{!raw f=name_q_synonym}worker"'

    def test_multi_token_raw_clause_is_parenthesized(self):
        clause = QueryBuilder._synonym_field_clause(
            "name_q_synonym", "name_q_synonym", ["british", "columbia"], True
        )
        assert clause == (
            '(_query_:"{!raw f=name_q_synonym}british"'
            ' AND _query_:"{!raw f=name_q_synonym}columbia")'
        )


class TestStemMapThreading:
    @staticmethod
    def _params(value: str, stem_map: dict[str, str] | None) -> QueryParams:
        return QueryParams(
            query={"value": value},
            rows=10,
            start=0,
            categories={},
            child_query={},
            child_categories={},
            fields=[],
            highlighted_fields=[],
            query_fields={NameField.NAME_Q: "child"},
            query_boost_fields={},
            query_fuzzy_fields={},
            query_synonym_fields={NameField.NAME_Q_SYN: "child"},
            full_query_boosts=[],
            exclude_sub_types=[],
            stemmed_terms_map=stem_map,
        )

    @staticmethod
    def _solr() -> Mock:
        solr = Mock()
        solr.query_builder = _query_builder()
        solr.analyze_field.return_value = {}
        return solr

    def test_stem_map_set_makes_zero_analyzer_calls(self):
        solr = self._solr()
        params = self._params("pacific workers", {"pacific": "pacif", "workers": "worker"})
        with patch.object(
            SolrSynonymList, "find_all_beginning_with_phrase", return_value=[_row("worker")]
        ) as lookup:
            payload = build_namex_query_payload(params, solr, True, False)
        solr.analyze_field.assert_not_called()
        # the stems from the map drove the synonym lookup and the raw clause
        assert ("worker", SolrSynonymList.Type.ALL) in [c.args for c in lookup.call_args_list]
        assert '_query_:"{!raw f=name_q_synonym}worker"' in payload["query"]

    def test_no_stem_map_falls_back_to_one_analyzer_call(self):
        solr = self._solr()
        params = self._params("pacific workers", None)
        with patch.object(SolrSynonymList, "find_all_beginning_with_phrase", return_value=[]):
            build_namex_query_payload(params, solr, True, False)
        assert solr.analyze_field.call_count == 1


class TestSurfaceStemBridging:
    """Doc tokens are surfaces, families hold agro stems - token_stems bridges them."""

    FAMILY: ClassVar[set[str]] = {"aesthet", "beauti", "cosmet"}

    def test_highlight_kept_with_token_stems(self):
        from namex_solr_api.services.namex_solr.utils import keep_family_synonym_highlights

        kept = keep_family_synonym_highlights(
            ["BEAUTY", "CALEZA", "INC"], self.FAMILY, None, {"beauty": ["beauti"]}
        )
        assert kept == ["BEAUTY"]

    def test_highlight_dropped_without_token_stems_documents_the_gap(self):
        # porter's y->i rewrite defeats the prefix fallback
        from namex_solr_api.services.namex_solr.utils import keep_family_synonym_highlights

        assert keep_family_synonym_highlights(["BEAUTY"], self.FAMILY) == []

    def test_family_cover_with_token_stems(self):
        from namex_solr_api.services.namex_solr.utils.conflict_bucket import cover_query_token

        cover = cover_query_token(
            "aesthetics",
            ["CALEZA", "BEAUTY", "INC"],
            family=self.FAMILY,
            name_token_stems={"beauty": ["beauti"], "caleza": ["caleza"], "inc": ["inc"]},
        )
        assert cover == "family"

    def test_rank_prefers_family_covered_doc(self):
        from namex_solr_api.services.namex_solr.utils import rank_conflict_docs

        docs = [
            {"name": "CALEZA HOLDINGS INC"},
            {"name": "CALEZA BEAUTY INC"},
        ]
        ranked = rank_conflict_docs(
            docs,
            "caleza aesthetics",
            family_by_term={"aesthetics": self.FAMILY},
            query_stems_by_term={"caleza": {"caleza"}, "aesthetics": {"aesthet"}},
            name_token_stems={"beauty": ["beauti"], "caleza": ["caleza"], "holdings": ["hold"], "inc": ["inc"]},
        )
        assert ranked[0]["name"] == "CALEZA BEAUTY INC"
