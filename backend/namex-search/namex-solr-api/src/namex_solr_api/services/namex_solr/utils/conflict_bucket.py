from namex_solr_api.config import Config
from namex_solr_api.services.base_solr.utils.formatting_helpers import prep_query_str
from namex_solr_api.services.base_solr.utils.query_builder import (
    SYNONYM_SKIP_WORDS,
    QueryBuilder,
)

from .formatting_helpers import (
    GLUED_FIRST_MIN_LEN,
    distinctive_coverage_terms,
    normalize_conflict_initials,
)
from .phonetic import keep_phonetic_match, replace_special_leading_sounds
from .synonym_helpers import keep_family_synonym_highlights, name_surface_tokens

BUCKET_SYNONYM = "synonym"
BUCKET_PHONETIC = "phonetic"
BUCKET_DROP = "drop"

_COVER_EXACT = "exact"
_COVER_STEM = "stem"
_COVER_FAMILY = "family"
_COVER_PHONETIC = "phonetic"
_COVER_FUZZY = "fuzzy"
_COVER_STRONG = frozenset({_COVER_EXACT, _COVER_STEM})
_COVER_RANK = {
    _COVER_EXACT: 4,
    _COVER_STEM: 3,
    _COVER_FAMILY: 2,
    _COVER_FUZZY: 1,
    _COVER_PHONETIC: 1,
}
_COVER_TIER = {
    _COVER_EXACT: 2,
    _COVER_STEM: 2,
    _COVER_FAMILY: 1,
    _COVER_FUZZY: 1,
    _COVER_PHONETIC: 0,
}
_MIN_STEM = 4
_MIN_DISTINCTIVE = 4
_RANK_PREFIX_LEN = 3
_MIN_INITIALS_RUN = 2
_LONG_PHONETIC = 6
_STEM_SUFFIXES = (
    "ational",
    "ization",
    "iveness",
    "fulness",
    "ousness",
    "ations",
    "ings",
    "edly",
    "ally",
    "ation",
    "ators",
    "ences",
    "ances",
    "ions",
    "ing",
    "ers",
    "ied",
    "ies",
    "ion",
    "ity",
    "es",
    "ed",
    "er",
    "ly",
    "al",
    "s",
)


def _skip_tokens(query_terms: set[str]) -> set[str]:
    skip = {word.lower() for word in SYNONYM_SKIP_WORDS}
    for item in Config.DEFAULT_DESIGNATIONS:
        token = (item or "").lower().strip(".")
        if token and " " not in token:
            skip.add(token)
    return {token for token in skip if token not in query_terms}


def _usable_name_tokens(name: str, query_terms: set[str]) -> list[str]:
    normalized = prep_query_str(normalize_conflict_initials(name or ""), "replace")
    skip = _skip_tokens(query_terms)
    tokens = []
    for token in name_surface_tokens(normalized):
        lowered = token.lower().strip(".")
        if lowered and lowered not in skip:
            tokens.append(token)
    return tokens


def _edit_distance(left: str, right: str) -> int:
    if left == right:
        return 0
    if not left:
        return len(right)
    if not right:
        return len(left)
    previous = list(range(len(right) + 1))
    for i, left_ch in enumerate(left, start=1):
        current = [i]
        for j, right_ch in enumerate(right, start=1):
            insert_cost = current[j - 1] + 1
            delete_cost = previous[j] + 1
            replace_cost = previous[j - 1] + (left_ch != right_ch)
            current.append(min(insert_cost, delete_cost, replace_cost))
        previous = current
    return previous[-1]


def _fuzzy_allowed(term: str) -> int | None:
    fuzzy = QueryBuilder.get_fuzzy_str(term, 1, 2)
    if not fuzzy:
        return None
    return int(fuzzy[1:])


def _ck_fold(word: str) -> str:
    folded = replace_special_leading_sounds((word or "").upper())
    if folded.startswith("C"):
        return "K" + folded[1:]
    return folded


def _distinctive_name_anchor(name_tokens: list[str]) -> list[str]:
    for token in name_tokens:
        if len(token) >= _MIN_DISTINCTIVE:
            return [token]
    return list(name_tokens[:1]) if name_tokens else []


def _phonetic_distance_allowed(query: str, name_token: str) -> int:
    fuzzy = max(_fuzzy_allowed(query) or 0, _fuzzy_allowed(name_token) or 0)
    if min(len(query), len(name_token)) >= _LONG_PHONETIC:
        return max(fuzzy, 2)
    return fuzzy


def _real_phonetic_match(name_token: str, query: str) -> bool:
    if not keep_phonetic_match(name_token, query):
        return False
    distance = _edit_distance(_ck_fold(name_token), _ck_fold(query))
    return distance <= _phonetic_distance_allowed(query, name_token)


def _fuzzy_cover(query: str, name_tokens: list[str]) -> bool:
    allowed = _fuzzy_allowed(query)
    if allowed is None:
        return False
    query_lower = query.lower()
    return any(_edit_distance(query_lower, name_token.lower()) <= allowed for name_token in name_tokens)


def _initials_run_covered(letters: list[str], name_tokens: list[str]) -> bool:
    if not letters:
        return False
    glued = "".join(letter.lower() for letter in letters)
    lowered = [token.lower() for token in name_tokens]
    if glued in lowered:
        return True
    width = len(letters)
    for index in range(len(lowered) - width + 1):
        window = lowered[index : index + width]
        if all(
            len(token) == 1 and token == letters[offset].lower()
            for offset, token in enumerate(window)
        ):
            return True
    return False


def _light_stem(word: str) -> str:
    lowered = (word or "").lower()
    for suffix in _STEM_SUFFIXES:
        if lowered.endswith(suffix) and len(lowered) - len(suffix) >= _MIN_STEM:
            return lowered[: -len(suffix)]
    return lowered


def _tokens_share_stem(left: str, right: str) -> bool:
    query = (left or "").lower()
    name = (right or "").lower()
    if len(query) < _MIN_STEM or len(name) < _MIN_STEM:
        return False
    if query == name:
        return True
    if query.startswith(name) or name.startswith(query):
        return True
    return _light_stem(query) == _light_stem(name)


def _stem_cover(
    query: str,
    name_tokens: list[str],
    query_stems: set[str] | None = None,
    name_token_stems: dict[str, list[str]] | None = None,
) -> bool:
    stems = {stem.lower() for stem in (query_stems or set()) if stem}
    if keep_family_synonym_highlights(name_tokens, {query.lower()} | stems, stems, name_token_stems):
        return True
    for name_token in name_tokens:
        if _tokens_share_stem(query, name_token):
            return True
        for stem in stems:
            if _tokens_share_stem(stem, name_token) or name_token.lower().startswith(stem):
                return True
    return False


def _is_rank_slot(term: str) -> bool:
    if len(term) >= _MIN_DISTINCTIVE:
        return True
    return len(term) == _RANK_PREFIX_LEN and term.lower() not in SYNONYM_SKIP_WORDS


def _query_initials_covered(query_value: str, name_tokens: list[str]) -> int:
    terms = (query_value or "").split()
    index = 0
    while index < len(terms):
        if run := _letter_run(terms, index):
            if _initials_run_covered(run, name_tokens):
                return 1
            index += len(run)
        else:
            index += 1
    return 0


def _letter_run(terms: list[str], index: int) -> list[str] | None:
    term = terms[index]
    if not (len(term) == 1 and term.isalpha()):
        return None
    end = index + 1
    while end < len(terms) and len(terms[end]) == 1 and terms[end].isalpha():
        end += 1
    if end - index >= _MIN_INITIALS_RUN:
        return terms[index:end]
    return None


def _query_has_distinctive(terms: list[str]) -> bool:
    index = 0
    while index < len(terms):
        if run := _letter_run(terms, index):
            return True
        if len(terms[index]) >= _MIN_DISTINCTIVE:
            return True
        index += len(run) if run else 1
    return False


def _sets_for_term(mapping: dict[str, set[str]], term: str) -> set[str]:
    return mapping.get(term) or mapping.get(term.lower()) or set()


def _consecutive_concat_cover(query: str, name_tokens: list[str]) -> bool:
    target = (query or "").lower()
    if len(target) < GLUED_FIRST_MIN_LEN:
        return False
    pieces = [token.lower().strip(".") for token in name_tokens if token]
    for start in range(len(pieces)):
        acc = ""
        for used, token in enumerate(pieces[start:], start=1):
            acc += token
            if used >= 2 and acc == target:  # noqa: PLR2004
                return True
            if len(acc) > len(target):
                break
    return False


def cover_query_token(  # noqa: PLR0913
    query_token: str,
    name_tokens: list[str],
    family: set[str] | None = None,
    family_stems: set[str] | None = None,
    query_stems: set[str] | None = None,
    sound_tokens: list[str] | None = None,
    name_token_stems: dict[str, list[str]] | None = None,
) -> str | None:
    query = (query_token or "").strip()
    if not query:
        cover = None
    else:
        family = {token.lower() for token in (family or set())}
        family_stems = {stem.lower() for stem in (family_stems or set())}
        query_lower = query.lower()
        sound_tokens = name_tokens if sound_tokens is None else sound_tokens
        if (
            any(name_token.lower() == query_lower for name_token in name_tokens)
            or _consecutive_concat_cover(query, name_tokens)
        ):
            cover = _COVER_EXACT
        elif _stem_cover(query, name_tokens, query_stems, name_token_stems):
            cover = _COVER_STEM
        elif family and keep_family_synonym_highlights(name_tokens, family, family_stems, name_token_stems):
            cover = _COVER_FAMILY
        elif any(_real_phonetic_match(name_token, query) for name_token in sound_tokens):
            cover = _COVER_PHONETIC
        elif _fuzzy_cover(query, sound_tokens):
            cover = _COVER_FUZZY
        else:
            cover = None
    return cover


def _cover_for_run(  # noqa: PLR0913
    run: list[str],
    name_tokens: list[str],
    family_by_term: dict[str, set[str]],
    family_stems_by_term: dict[str, set[str]],
    query_stems_by_term: dict[str, set[str]],
    sound_tokens: list[str],
    name_token_stems: dict[str, list[str]] | None = None,
) -> str | None:
    if _initials_run_covered(run, name_tokens):
        return _COVER_EXACT
    glued = "".join(run)
    if len(run) >= _MIN_DISTINCTIVE and glued:
        return cover_query_token(
            glued,
            name_tokens,
            _sets_for_term(family_by_term, glued),
            _sets_for_term(family_stems_by_term, glued),
            _sets_for_term(query_stems_by_term, glued),
            sound_tokens,
            name_token_stems,
        )
    return None


def _iter_query_covers(  # noqa: PLR0913
    query_value: str,
    name: str,
    family_by_term: dict[str, set[str]] | None = None,
    family_stems_by_term: dict[str, set[str]] | None = None,
    query_stems_by_term: dict[str, set[str]] | None = None,
    name_token_stems: dict[str, list[str]] | None = None,
):
    terms = [term for term in (query_value or "").split() if term]
    if not terms:
        return
    query_terms = {term.lower() for term in terms}
    name_tokens = _usable_name_tokens(name, query_terms)
    family_by_term = family_by_term or {}
    family_stems_by_term = family_stems_by_term or {}
    query_stems_by_term = query_stems_by_term or {}
    require_all = not _query_has_distinctive(terms)
    awaiting_distinctive = not require_all
    index = 0
    while index < len(terms):
        term = terms[index]
        run = _letter_run(terms, index)
        if run:
            is_distinctive = True
            counts_for_rank = True
            consume_to = index + len(run)
        else:
            is_distinctive = len(term) >= _MIN_DISTINCTIVE
            counts_for_rank = is_distinctive or _is_rank_slot(term)
            consume_to = index + 1
        sound_tokens = (
            _distinctive_name_anchor(name_tokens)
            if awaiting_distinctive and is_distinctive
            else name_tokens
        )
        if run:
            cover = _cover_for_run(
                run,
                name_tokens,
                family_by_term,
                family_stems_by_term,
                query_stems_by_term,
                sound_tokens,
                name_token_stems,
            )
        else:
            cover = cover_query_token(
                term,
                name_tokens,
                _sets_for_term(family_by_term, term),
                _sets_for_term(family_stems_by_term, term),
                _sets_for_term(query_stems_by_term, term),
                sound_tokens,
                name_token_stems,
            )
        yield require_all, awaiting_distinctive, is_distinctive, counts_for_rank, cover
        if not require_all and awaiting_distinctive and is_distinctive and cover is not None:
            awaiting_distinctive = False
        index = consume_to


def distinctive_cover_count(  # noqa: PLR0913
    query_value: str,
    name: str,
    family_by_term: dict[str, set[str]] | None = None,
    family_stems_by_term: dict[str, set[str]] | None = None,
    query_stems_by_term: dict[str, set[str]] | None = None,
    name_token_stems: dict[str, list[str]] | None = None,
) -> int:
    covered, _strong = distinctive_cover_rank(
        query_value, name, family_by_term, family_stems_by_term, query_stems_by_term, name_token_stems
    )
    return covered


def distinctive_cover_rank(  # noqa: PLR0913
    query_value: str,
    name: str,
    family_by_term: dict[str, set[str]] | None = None,
    family_stems_by_term: dict[str, set[str]] | None = None,
    query_stems_by_term: dict[str, set[str]] | None = None,
    name_token_stems: dict[str, list[str]] | None = None,
) -> tuple[int, int]:
    covered = 0
    strong = 0
    for _require_all, _awaiting, _is_distinctive, counts_for_rank, cover in _iter_query_covers(
        query_value, name, family_by_term, family_stems_by_term, query_stems_by_term, name_token_stems
    ):
        if counts_for_rank and cover is not None:
            covered += 1
            if cover in _COVER_STRONG:
                strong += 1
    return covered, strong


def _token_cover(  # noqa: PLR0913
    term: str,
    name_tokens: list[str],
    family_by_term: dict[str, set[str]] | None,
    family_stems_by_term: dict[str, set[str]] | None,
    query_stems_by_term: dict[str, set[str]] | None,
    name_token_stems: dict[str, list[str]] | None = None,
) -> str | None:
    return cover_query_token(
        term,
        name_tokens,
        _sets_for_term(family_by_term or {}, term),
        _sets_for_term(family_stems_by_term or {}, term),
        _sets_for_term(query_stems_by_term or {}, term),
        name_tokens,
        name_token_stems,
    )


def _hyphen_glued_cover(
    glued_tokens: list[str] | None,
    name_tokens: list[str],
    *args,
) -> str | None:
    best = None
    for token in glued_tokens or ():
        cover = _token_cover(token, name_tokens, *args)
        if cover and (best is None or _COVER_RANK[cover] > _COVER_RANK[best]):
            best = cover
    return best


def conflict_rank_key(  # noqa: PLR0913
    query_value: str,
    name: str,
    family_by_term: dict[str, set[str]] | None = None,
    family_stems_by_term: dict[str, set[str]] | None = None,
    query_stems_by_term: dict[str, set[str]] | None = None,
    name_token_stems: dict[str, list[str]] | None = None,
    glued_tokens: list[str] | None = None,
) -> tuple[int, int, int, int, int, int, int]:
    """Pin closer leftover after identity is present.

    identity_present: first coverage token is family or better (bc counts).
    leftover_exact: last coverage token is exact/stem, not only family.
    first_identity_tier: 2 exact/stem, 1 family/fuzzy, 0 missing/phonetic.
    leftover_covered: last coverage term matched at all.
    prefix_complete: every prefix-span token is exact/stem.
    """
    terms = distinctive_coverage_terms(query_value)
    query_terms = {term.lower() for term in (query_value or "").split() if term}
    name_tokens = _usable_name_tokens(name, query_terms)
    initials_exact = _query_initials_covered(query_value, name_tokens)
    _covered, strong = distinctive_cover_rank(
        query_value, name, family_by_term, family_stems_by_term, query_stems_by_term, name_token_stems
    )
    leftover_covered = leftover_exact = identity_present = first_tier = prefix_complete = 0
    if terms:
        first_cover = _token_cover(
            terms[0], name_tokens, family_by_term, family_stems_by_term, query_stems_by_term, name_token_stems
        )
        if first_cover in _COVER_STRONG:
            first_tier = 2
        elif first_cover in {_COVER_FAMILY, _COVER_FUZZY}:
            first_tier = 1
        else:
            first_tier = 0
        identity_present = int(first_tier > 0)
        prefix_span = terms[:-1]
        if len(terms) >= 2:  # noqa: PLR2004
            leftover_cover = _token_cover(
                terms[-1],
                name_tokens,
                family_by_term,
                family_stems_by_term,
                query_stems_by_term,
                name_token_stems,
            )
            leftover_covered = int(leftover_cover is not None)
            leftover_exact = int(leftover_cover in _COVER_STRONG)
        else:
            prefix_span = []
        if prefix_span:
            prefix_complete = int(
                all(
                    _token_cover(
                        term,
                        name_tokens,
                        family_by_term,
                        family_stems_by_term,
                        query_stems_by_term,
                        name_token_stems,
                    )
                    in _COVER_STRONG
                    for term in prefix_span
                )
            )
        else:
            prefix_complete = 1
    glued_cover = _hyphen_glued_cover(
        glued_tokens,
        name_tokens,
        family_by_term,
        family_stems_by_term,
        query_stems_by_term,
        name_token_stems,
    )
    if glued_cover:
        leftover_covered = 1
        leftover_exact = max(leftover_exact, int(glued_cover in _COVER_STRONG))
        identity_present = 1
        first_tier = max(first_tier, _COVER_TIER[glued_cover])
        if not terms:
            prefix_complete = 1
    return (
        initials_exact,
        identity_present,
        leftover_exact,
        first_tier,
        leftover_covered,
        prefix_complete,
        strong,
    )


def rank_conflict_docs(  # noqa: PLR0913
    docs: list[dict],
    query_value: str,
    family_by_term: dict[str, set[str]] | None = None,
    family_stems_by_term: dict[str, set[str]] | None = None,
    query_stems_by_term: dict[str, set[str]] | None = None,
    name_token_stems: dict[str, list[str]] | None = None,
    glued_tokens: list[str] | None = None,
) -> list[dict]:
    return sorted(
        docs,
        key=lambda doc: tuple(
            -n
            for n in conflict_rank_key(
                query_value,
                doc.get("name") or "",
                family_by_term,
                family_stems_by_term,
                query_stems_by_term,
                name_token_stems,
                glued_tokens,
            )
        ),
    )


def visible_conflict_bucket(bucket: str) -> str:
    """Keep Solr hits on the page. Uncovered identity is synonym, ranked last."""
    return BUCKET_SYNONYM if bucket == BUCKET_DROP else bucket


def classify_conflict_bucket(  # noqa: PLR0913
    query_value: str,
    name: str,
    family_by_term: dict[str, set[str]] | None = None,
    family_stems_by_term: dict[str, set[str]] | None = None,
    query_stems_by_term: dict[str, set[str]] | None = None,
    name_token_stems: dict[str, list[str]] | None = None,
    glued_tokens: list[str] | None = None,
) -> str:
    terms = [term for term in (query_value or "").split() if term]
    if not terms:
        return BUCKET_SYNONYM

    saw_phonetic = False
    dropped = False
    for require_all, awaiting_distinctive, is_distinctive, _counts_for_rank, cover in _iter_query_covers(
        query_value, name, family_by_term, family_stems_by_term, query_stems_by_term, name_token_stems
    ):
        if cover == _COVER_PHONETIC and (require_all or (awaiting_distinctive and is_distinctive)):
            saw_phonetic = True

        if require_all and cover is None:
            dropped = True
            break
        if awaiting_distinctive and is_distinctive and cover is None:
            dropped = True
            break
    glued_cover = _hyphen_glued_cover(
        glued_tokens,
        _usable_name_tokens(name, {term.lower() for term in terms}),
        family_by_term,
        family_stems_by_term,
        query_stems_by_term,
        name_token_stems,
    )
    if glued_cover:
        return BUCKET_PHONETIC if glued_cover == _COVER_PHONETIC else BUCKET_SYNONYM
    if dropped:
        return BUCKET_DROP
    return BUCKET_PHONETIC if saw_phonetic else BUCKET_SYNONYM
