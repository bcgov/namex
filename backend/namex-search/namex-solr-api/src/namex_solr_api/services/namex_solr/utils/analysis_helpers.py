"""Solr analysis helpers for synonym stem lookup."""
from contextlib import suppress

from flask_caching import Cache

STEMMED_AGRO_FIELD_TYPE = "text_stemmed_agro"
_STEM_CHUNK_SIZE = 200
# Matches the String(50) limit on solr_synonym_lists.synonym
MAX_SYNONYM_KEY_LENGTH = 50

# Cross-request cache for query-value stem maps (initialized in create_app,
# same wiring as auth_cache). Porter stems are deterministic, so entries only
# go stale on a schema/analyzer change; the default TTL bounds that.
analysis_cache = Cache()


def _analysis_index_steps(analysis_response: dict) -> list:
    analysis = (analysis_response or {}).get("analysis") or {}
    field_types = analysis.get("field_types") or analysis.get("fieldTypes") or {}
    typed = field_types.get(STEMMED_AGRO_FIELD_TYPE) or {}
    if steps := typed.get("index"):
        return steps
    field_names = analysis.get("field_names") or analysis.get("fieldNames") or {}
    named = field_names.get(STEMMED_AGRO_FIELD_TYPE) or {}
    if steps := named.get("index"):
        return steps
    for payload in field_names.values():
        if isinstance(payload, dict) and payload.get("index"):
            return payload["index"]
    return []


def parse_stemmed_tokens(analysis_response: dict) -> list[str]:
    """Return final index tokens from a text_stemmed_agro analysis response."""
    index_steps = _analysis_index_steps(analysis_response)
    if not index_steps:
        return []
    last_step = index_steps[-1]
    if not isinstance(last_step, list):
        return []
    return [token["text"] for token in last_step if isinstance(token, dict) and token.get("text")]


def analyze_stemmed_agro_tokens(solr, query_value: str) -> list[str]:
    """Stem query tokens with the same analyzer as name_q_agro (Kial's path)."""
    if not query_value or not str(query_value).strip():
        return []
    return parse_stemmed_tokens(solr.analyze_field(query_value.strip(), STEMMED_AGRO_FIELD_TYPE))


def build_stem_map(terms: list[str], stems: list[str]) -> dict[str, str]:
    """Return {term: stem}; empty when the analysis token count doesn't line up."""
    if not stems or len(stems) != len(terms):
        return {}
    return {term: stem for term, stem in zip(terms, stems, strict=True) if stem}


def analyze_stemmed_agro_stem_map(solr, query_value: str) -> dict[str, str]:
    """Return {term: agro stem} for the query value using a single analyzer call.

    Empty dict when analysis is unavailable (callers fall back to raw terms).
    Successful results are cached across requests; failures are never cached.
    """
    value = " ".join((query_value or "").split())
    if not value:
        return {}
    cache_key = f"agro-stem::{value}"
    # the cache is best-effort - it must never break search
    with suppress(Exception):
        if (cached := analysis_cache.get(cache_key)) is not None:
            return dict(cached)
    stem_map = build_stem_map(value.split(), analyze_stemmed_agro_tokens(solr, value))
    if stem_map:
        with suppress(Exception):
            analysis_cache.set(cache_key, stem_map)
    return stem_map


def analyze_stemmed_agro_token_map(
    solr, tokens: list[str], *, chunk_size: int = _STEM_CHUNK_SIZE, timeout: int = 30
) -> dict[str, str]:
    """Return {token: agro stem} for the unique tokens, batched into few analyzer calls."""
    unique_tokens = []
    seen = set()
    for token in tokens:
        lowered = (token or "").lower().strip()
        if lowered and lowered not in seen:
            seen.add(lowered)
            unique_tokens.append(lowered)

    stem_map: dict[str, str] = {}
    for chunk_start in range(0, len(unique_tokens), chunk_size):
        chunk = unique_tokens[chunk_start:chunk_start + chunk_size]
        stems = parse_stemmed_tokens(
            solr.analyze_field(" ".join(chunk), STEMMED_AGRO_FIELD_TYPE, timeout=timeout, fail_soft=False)
        )
        if len(stems) == len(chunk):
            stem_map.update(zip(chunk, stems, strict=True))
            continue
        # token counts diverged (a filter dropped or split a token) - map that
        # chunk one token at a time; an unmappable token stems to itself
        for token in chunk:
            token_stems = parse_stemmed_tokens(
                solr.analyze_field(token, STEMMED_AGRO_FIELD_TYPE, timeout=timeout, fail_soft=False)
            )
            stem_map[token] = token_stems[0] if len(token_stems) == 1 else token
    return stem_map


def analyze_stemmed_agro_token_stems(solr, tokens: list[str]) -> dict[str, list[str]]:
    """Return {token: [agro stem]} for doc-side surface tokens."""
    unique = sorted({(token or "").lower().strip() for token in tokens} - {""})
    resolved: dict[str, list[str]] = {}
    missing: list[str] = []
    for token in unique:
        cached = None
        with suppress(Exception):
            cached = analysis_cache.get(f"agro-tok::{token}")
        if cached:
            resolved[token] = list(cached)
        else:
            missing.append(token)
    if missing:
        try:
            stem_map = analyze_stemmed_agro_token_map(solr, missing, timeout=5)
        except Exception:
            return resolved
        for token, stem in stem_map.items():
            resolved[token] = [stem]
            with suppress(Exception):
                analysis_cache.set(f"agro-tok::{token}", [stem])
    return resolved


def stem_phrase(phrase: str, stem_map: dict[str, str]) -> str:
    """Return the phrase with each token replaced by its stem (tokens keep their order)."""
    return " ".join(stem_map.get(token, token) for token in (phrase or "").lower().split())


def stem_synonym_payload(
    synonym_lists: dict[str, list[str]],
    stem_map: dict[str, str],
    max_key_length: int = MAX_SYNONYM_KEY_LENGTH,
) -> tuple[dict[str, list[str]], list[str]]:
    """Return ({stemmed key: stemmed members}, skipped surface keys).

    Members are deduped after stemming and self-references (member == key) are dropped.
    Keys/members whose stemmed form exceeds max_key_length are skipped
    (each row, including reverse-mapping rows, must fit the synonym column).
    """
    stemmed_lists: dict[str, list[str]] = {}
    skipped: list[str] = []
    for key, members in (synonym_lists or {}).items():
        stemmed_key = stem_phrase(key, stem_map)
        if not stemmed_key:
            continue
        if len(stemmed_key) > max_key_length:
            skipped.append(key)
            continue
        # distinct surface keys can share a stem - merge their member lists
        stemmed_members = stemmed_lists.setdefault(stemmed_key, [])
        seen_members = {stemmed_key, *stemmed_members}
        for member in members or []:
            stemmed_member = stem_phrase(member, stem_map)
            if not stemmed_member or stemmed_member in seen_members:
                continue
            if len(stemmed_member) > max_key_length:
                skipped.append(member)
                continue
            seen_members.add(stemmed_member)
            stemmed_members.append(stemmed_member)
    return stemmed_lists, skipped
