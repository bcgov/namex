"""Manages common solr query building methods."""
import re

from namex_solr_api.common.base_enum import BaseEnum

# NameX function skip words (same set as namex-solr skipwords.txt).
# Raw synonym lookup bypasses the query-time stop filter, so these keys
# must not be emitted on the retrieval query.
SYNONYM_SKIP_WORDS = frozenset({
    "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in",
    "into", "is", "it", "no", "not", "o", "on", "or", "such", "that", "the",
    "their", "then", "there", "these", "they", "this", "to", "of",
})
_RAW_SYNONYM_TOKEN = re.compile(r"^[a-z0-9]+(?:'[a-z0-9]+)?$")


class QueryBuilder:
    """Manages shared query building code."""
    identifier_field_values = None
    pre_child_filter_clause = None
    pre_parent_filter_clause = None
    synonym_field_map = None

    def __init__(self, identifier_field_values: list[str], unique_parent_field: BaseEnum, synonym_field_map: dict[BaseEnum, BaseEnum]):
        """Initialize the solr class."""
        self.identifier_field_values = identifier_field_values
        self.pre_child_filter_clause = "{!parent which=\"" + unique_parent_field.value + ":*\"}"
        self.pre_parent_filter_clause = "{!child of=\"" + unique_parent_field.value + ":*\"}"
        self.synonym_field_map = synonym_field_map

    def create_clause(self, field_value: str, term: str, is_child: bool, is_child_search: bool, phrase: bool = False) -> str:
        """Return the query clause for the field and term."""
        corp_prefix_regex = r"(^[aA-zZ]+)[0-9]+$"

        search_field = field_value
        if is_child and not is_child_search:
            search_field = self.pre_child_filter_clause + search_field
        elif not is_child and is_child_search:
            search_field = self.pre_parent_filter_clause + search_field

        if field_value in self.identifier_field_values and (identifier := re.search(corp_prefix_regex, term)):
            prefix = identifier.group(1)
            no_prefix_term = term.replace(prefix, "", 1)

            return f'({search_field}:"{no_prefix_term}" AND {search_field}:"{prefix.upper()}")'

        if phrase:
            return f'{search_field}:"{term}"'

        return f"{search_field}:{term}"

    def build_filter_clause(self, query: dict[str, str], is_child_search: bool) -> list[str]:
        """Return the filters for the query."""
        filters = []
        for key, value in query.items():
            if key in ["value"] or not value:
                continue
            terms = value.split()
            for term in terms:
                # NOTE: is_child is always false for now in supported filters
                filters.append(self.create_clause(key, term, False, is_child_search))
        return filters

    def build_child_query(self, child_query: dict[str, str], is_child_search: bool, keep_phrase: bool = False) -> str | None:
        """Return the child query fq."""
        # add filter clauses for child query items
        child_q = ""
        for key, value in child_query.items():
            if not value:
                continue

            if keep_phrase:
                child_q = self.join_clause(child_q, self.create_clause(key, value, True, is_child_search, True), "AND")
                continue
            
            terms = value.split()
            child_q = self.join_clause(child_q, self.create_clause(key, terms[0], True, is_child_search), "AND")

            for term in terms[1:]:
                child_q += f" AND {self.create_clause(key, term, True, is_child_search)}"

        if not child_q:
            return None

        return f"({child_q})"

    def build_facet_query(self,
                          field: BaseEnum,
                          values: list[str],
                          is_child: bool,
                          is_child_search: bool) -> str:
        """Return the facet filter clause for the given params."""
        filter_q = ''
        if is_child and not is_child_search:
            filter_q = self.pre_child_filter_clause
        elif not is_child and is_child_search:
            filter_q = self.pre_parent_filter_clause
        filter_q += f'{field.value}:("{values[0]}"'
        for val in values[1:]:
            filter_q += f' OR "{val}"'
        filter_q += ")"
        return filter_q
    
    @staticmethod
    def _term_score_suffix(
        term: str,
        constant_score_terms: frozenset[str],
        boost: int | None = None,
    ) -> str:
        """Return a Solr score suffix.

        Outer-wildcard tokens use ^= so repeated occurrences do not add BM25
        term frequency. Other terms keep the existing ^boost / unboosted form.
        """
        if term in constant_score_terms:
            return f"^={boost if boost is not None else 1}"
        if boost is not None:
            return f"^{boost}"
        return ""

    def build_term_clause(  # noqa: PLR0913
        self,
        term: str,
        fields: dict[BaseEnum, str],
        boost_fields: dict[BaseEnum, int],
        fuzzy_fields: dict[BaseEnum, dict[str, int]],
        is_child_search: bool,
        constant_score_terms: frozenset[str] | None = None,
    ) -> str:
        """Return the base term clause."""
        constant_score_terms = constant_score_terms or frozenset()
        term_clause = ""
        for field, level in fields.items():
            field_clause = self.create_clause(field.value, term, level == "child", is_child_search)
            pre_boost_clause = field_clause
            # add boost
            field_clause += self._term_score_suffix(
                term,
                constant_score_terms,
                boost_fields.get(field),
            )

            term_clause = self.join_clause(term_clause, field_clause, "OR")
            # add fuzzy matching
            if field in fuzzy_fields and (fuzzy_str := self.get_fuzzy_str(term,
                                          fuzzy_fields[field]["short"],
                                          fuzzy_fields[field]["long"])):
                # add another with fuzzy (this one will give a lower score on a hit if the original has a boost)
                fuzzy_clause = f"{pre_boost_clause}{fuzzy_str}"
                fuzzy_clause += self._term_score_suffix(term, constant_score_terms)
                term_clause = self.join_clause(term_clause, fuzzy_clause, "OR")
        return term_clause

    def build_term_synonym_clauses(  # noqa: PLR0913
        self,
        term_clause: str,
        terms: list[str],
        term_index: int,
        synonym_info: dict,
        synonym_fields: dict[BaseEnum, str],
        is_child_search: bool,
        boost_fields: dict[BaseEnum, int],
        stemmed_terms: list[str] | None = None,
        synonym_as_raw: bool = False,
        constant_score_terms: frozenset[str] | None = None,
    ):
        """Return the term clause with the added synonym clauses."""
        term = terms[term_index]
        for field, level in synonym_fields.items():
            if not synonym_info.get(field):
                synonym_info[field] = {"synonym_terms": [], "synonym_start_index": None}
            synonym_terms = synonym_info[field]["synonym_terms"]
            synonym_start_index = synonym_info[field]["synonym_start_index"]

            field_value = field.value
            if level == "child" and not is_child_search:
                field_value = self.pre_child_filter_clause + field.value
            elif level != "child" and is_child_search:
                field_value = self.pre_parent_filter_clause + field.value

            synonym_clause = ""
            active_key: list[str] = []
            if synonym_terms and term_index < synonym_start_index + len(synonym_terms):
                # a synonym matched on a previous term and includes the current term (multi word synonym)
                active_key = synonym_terms
            elif new_synonym_terms := self.find_synonym_terms(
                term, term_index, terms, field, stemmed_terms
            ):
                synonym_info[field]["synonym_terms"] = new_synonym_terms
                synonym_info[field]["synonym_start_index"] = term_index
                active_key = new_synonym_terms
            if active_key:
                synonym_clause = self._synonym_field_clause(
                    field.value,
                    field_value,
                    active_key,
                    synonym_as_raw,
                )

            if synonym_clause:
                synonym_clause += self._term_score_suffix(
                    term,
                    constant_score_terms or frozenset(),
                    boost_fields.get(field),
                )
                term_clause = self.join_clause(term_clause, f"({synonym_clause})", "OR")

        return term_clause

    def build_base_query(self,  # noqa: PLR0913
                         query: dict[str, str],
                         fields: dict[BaseEnum, str],
                         boost_fields: dict[BaseEnum, int],
                         fuzzy_fields: dict[BaseEnum, dict[str, int]],
                         synonym_fields: dict[BaseEnum, str],
                         is_child_search: bool,
                         clause_bridge="AND",
                         stemmed_terms: list[str] | None = None,
                         synonym_as_raw: bool = False,
                         constant_score_terms: frozenset[str] | None = None) -> dict[str, list[str]]:
        """Return a solr query with filters for each subsequent term."""
        terms = query["value"].split()
        if not stemmed_terms or len(stemmed_terms) != len(terms):
            stemmed_terms = terms
        synonym_info = {}
        query_clause = ""
        # Each term in the searched 'value' must match on at least one of:
        # 'fields', 'fuzzy_fields' or 'synonym_fields' query clauses.
        # This loop adds clauses for the all the given fields for each term
        for term_index, term in enumerate(terms):
            # Get the base clause, which references the fields, fuzzy fields and adds the boost clause for ordering
            term_clause = self.build_term_clause(
                term, fields, boost_fields, fuzzy_fields, is_child_search, constant_score_terms
            )

            # Add the synonym field clauses
            term_clause = self.build_term_synonym_clauses(
                term_clause, terms, term_index, synonym_info, synonym_fields, is_child_search,
                boost_fields, stemmed_terms, synonym_as_raw, constant_score_terms,
            )

            # Join the term clause to the full query
            query_clause = self.join_clause(query_clause, f"({term_clause})", clause_bridge)

        # Add extra filters if applicable
        filters = self.build_filter_clause(query, is_child_search)

        if not query_clause:
            # handle empty string provided for query value
            query_clause = '""'

        return {"query": query_clause, "filter": filters}
    
    def find_synonym_terms(
        self,
        start_term: str,
        start_term_index: int,
        terms: list[str],
        field: BaseEnum,
        stemmed_terms: list[str] | None = None,
    ) -> list[str]:
        """Return the synonym key tokens matching the query's agro stems.

        Stored synonym keys are agro stems (stemmed on write),
        so the only legitimate match is stem equality per key token.
        """
        from namex_solr_api.models import SolrSynonymList

        stemmed_terms = stemmed_terms or terms
        if self._is_synonym_skip_token(start_term):
            return []
        start_stem = (
            stemmed_terms[start_term_index]
            if start_term_index < len(stemmed_terms)
            else start_term
        )
        if not start_stem or self._is_synonym_skip_token(start_stem):
            return []

        best_synonym_match_terms: list[str] = []
        for row in SolrSynonymList.find_all_beginning_with_phrase(
            start_stem, self.synonym_field_map[field]
        ):
            synonym_terms = row.synonym.split()
            if not synonym_terms or len(synonym_terms) > len(terms[start_term_index:]):
                continue
            if any(self._is_synonym_skip_token(token) for token in synonym_terms):
                continue
            if not self._query_covers_synonym_key(
                synonym_terms, start_term_index, terms, stemmed_terms
            ):
                continue
            if len(synonym_terms) > len(best_synonym_match_terms):
                best_synonym_match_terms = synonym_terms

        return best_synonym_match_terms

    @staticmethod
    def _is_synonym_skip_token(token: str) -> bool:
        return bool(token) and token.lower() in SYNONYM_SKIP_WORDS

    @staticmethod
    def _synonym_field_clause(
        leaf_field: str,
        field_value: str,
        synonym_terms: list[str],
        synonym_as_raw: bool,
    ) -> str:
        """Build a synonym field clause."""
        if not synonym_as_raw:
            return f"{field_value}:{' '.join(synonym_terms)}"
        if field_value != leaf_field:
            # A block-join prefix ({!parent}/{!child}) cannot wrap an embedded _query_ clause
            return f"{field_value}:{' '.join(synonym_terms)}"
        raw_parts = []
        for token in synonym_terms:
            safe = token.lower()
            if not _RAW_SYNONYM_TOKEN.match(safe):
                return f"{field_value}:{' '.join(synonym_terms)}"
            raw_parts.append(f'_query_:"{{!raw f={leaf_field}}}{safe}"')
        raw_clause = " AND ".join(raw_parts)
        if len(raw_parts) > 1:
            # parenthesize so a caller OR-ing this clause keeps the AND grouping
            raw_clause = f"({raw_clause})"
        return raw_clause

    @staticmethod
    def _query_covers_synonym_key(
        key_terms: list[str],
        start_index: int,
        terms: list[str],
        stemmed_terms: list[str],
    ) -> bool:
        """True if each key token (a stored agro stem) equals the query token's stem."""
        for i, key_term in enumerate(key_terms):
            query_term = terms[start_index + i]
            query_stem = (
                stemmed_terms[start_index + i]
                if start_index + i < len(stemmed_terms)
                else query_term
            )
            if key_term.lower() != query_stem.lower():
                return False
        return True

    @staticmethod
    def build_facet(field: BaseEnum, is_nested: bool) -> dict[str, dict]:
        """Return the facet dict for the field."""
        facet = {field.value: {"type": "terms", "field": field.value}}
        if is_nested:
            facet[field.value]["domain"] = {"blockChildren": "{!v=$parents}"}
            facet[field.value]["facet"] = {"by_parent": "uniqueBlock({!v=$parents})"}

        return facet

    @staticmethod
    def get_fuzzy_str(term: str, short: int, long: int) -> str:
        """Return the fuzzy string for the term."""
        if len(term) < 4:  # noqa: PLR2004
            return ""
        if len(term) < 7:  # noqa: PLR2004
            return f"~{short}"
        return f"~{long}"

    @staticmethod
    def join_clause(current_clause: str, new_clause: str, join_str: str):
        """Return the current clause added with the new clause."""
        if current_clause:
            current_clause += f" {join_str} "
        return current_clause + new_clause
