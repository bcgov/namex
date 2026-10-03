import string

from flask import current_app, has_app_context
from sqlalchemy import text

from namex.constants import Designations
from namex.models import db
from namex.services.solr import words_to_filter_from_name
from namex.services.solr.solr_client import SolrClient


def comma_entries(value: str) -> list[str]:
    return [part.strip().lower() for part in (value or "").split(",") if part.strip()]


def lookup_forms(word: str) -> set[str]:
    forms = {word}
    if len(word) > 4 and word.endswith("ies"):
        forms.add(word[:-3] + "y")
    if len(word) > 4 and word.endswith("es"):
        forms.add(word[:-2])
    if len(word) > 4 and word.endswith("s"):
        forms.add(word[:-1])
    return {form for form in forms if len(form) >= 4}


def _unique_terms(words: list[str]) -> list[str]:
    cleaned: list[str] = []
    seen: set[str] = set()
    for word in words:
        token = (word or "").strip().lower()
        if token and token not in seen:
            seen.add(token)
            cleaned.append(token)
    return cleaned


def _merge_synonym_row(
    families: dict[str, list[str]],
    forms_by_word: dict[str, set[str]],
    synonyms_text: str,
    stems_text: str,
) -> None:
    entries = comma_entries(synonyms_text) + comma_entries(stems_text)
    listed = set(entries)
    for word, forms in forms_by_word.items():
        if forms.isdisjoint(listed):
            continue
        merged = families[word]
        for entry in entries:
            if entry not in merged:
                merged.append(entry)


def families_from_synonym_rows(words: list[str], rows: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Map each search word to the browsable synonym row that lists that word."""
    cleaned = _unique_terms(words)
    forms_by_word = {word: lookup_forms(word) for word in cleaned}
    families = {word: [] for word in cleaned}
    for synonyms_text, stems_text in rows:
        _merge_synonym_row(families, forms_by_word, synonyms_text, stems_text)
    return families


def load_browse_synonym_families(words: list[str]) -> dict[str, list[str]] | None:
    """Read enabled rows from the NameX synonym table. None when that read is unavailable."""
    if not has_app_context():
        return None
    cleaned = [(word or "").strip().lower() for word in words if (word or "").strip()]
    if not cleaned:
        return {}
    clauses = []
    params: dict[str, str] = {}
    needles: list[str] = []
    for word in dict.fromkeys(cleaned):
        needles.extend(lookup_forms(word))
    for index, needle in enumerate(dict.fromkeys(needles)):
        params[f"w{index}"] = f"%{needle}%"
        clauses.append(f"(synonyms_text ILIKE :w{index} OR stems_text ILIKE :w{index})")
    statement = text(
        "SELECT synonyms_text, stems_text FROM synonym WHERE enabled IS TRUE AND ("
        + " OR ".join(clauses)
        + ")"
    )
    try:
        rows = db.session.execute(statement, params).fetchall()
    except Exception:
        current_app.logger.exception("synonym table lookup failed")
        return None
    return families_from_synonym_rows(cleaned, [(row[0], row[1]) for row in rows])


class SolrHlpers:
    @classmethod
    def _name_pre_processing(cls, name):
        processed_name = (
            (' ' + name.lower() + ' ')
            .replace('!', '')
            .replace('@', '')
            .replace('#', '')
            .replace('%', '')
            .replace('&', '')
            .replace('\\', '')
            .replace('/', '')
            .replace('{', '')
            .replace('}', '')
            .replace('[', '')
            .replace(']', '')
            .replace(')', '')
            .replace('(', '')
            .replace('+', '')
            .replace('-', '')
            .replace('|', '')
            .replace('?', '')
            .replace('.', '')
            .replace(',', '')
            .replace('_', '')
            .replace("'n", '')
            .replace("'", '')
            .replace('"', '')
            .replace(' $ ', 'dollar')
            .replace('$', 's')
            .replace(' ¢ ', 'cent')
            .replace('¢', 'c')
            .replace('britishcolumbia', 'bc')
            .replace('britishcolumbias', 'bc')
            .replace('britishcolumbian', 'bc')
            .replace('britishcolumbians', 'bc')
            .replace('british columbia', 'bc')
            .replace('british columbias', 'bc')
            .replace('british columbian', 'bc')
            .replace('british columbians', 'bc')
        )
        return processed_name.strip()

    @classmethod
    def _conflicts_post_process(cls, q_data, query_name):
        """
        Processes Solr search results to filter candidates based on phonetic matching and designation exclusion.

        Args:
            docs (list): Solr search results, each item is a dict representing a candidate name document.
            query_name (str): The name input to the query, used for matching against candidate names.

        Returns:
            list: Filtered list of candidate names that match the query criteria.
        """
        exact_matches = []
        similar_matches = []
        histories = []

        for rcd in q_data.get('searchResults', {}).get('results', []):
            nm = cls._get_name_without_designation(rcd.get('name'))
            if nm == query_name:
                rcd['type'] = 'exact'
                exact_matches.append(rcd)
                if rcd.get('name_state') in ('CORP', 'A'):
                    histories.append(rcd)
            else:
                highlighting = rcd.get('highlighting', {})
                exact = cls.normalize_words(highlighting.get('exact', []))
                stems = cls.normalize_words(highlighting.get('stems', []))
                synonyms = cls.normalize_words(highlighting.get('synonyms', []))
                phonetic = cls.normalize_words(highlighting.get('phonetic', []))

                rcd['type'] = 'similar'
                rcd['bucket'] = rcd.get('bucket')
                rcd['highlighting'] = { 'exact': list(exact), 'stems': list(stems), 'synonyms': list(synonyms), 'phonetic': list(phonetic) }
                similar_matches.append(rcd)

        return {
            'names': similar_matches,
            'exactNames': exact_matches,
            'histories': histories}

    def normalize_words(word):
        """
        Normalize a list of words by removing punctuation and converting to uppercase.
        """
        return [w.upper().translate(str.maketrans('', '', string.punctuation)) for w in word]

    @classmethod
    def _find_stems(cls, name, query_name, synonyms):
        def clean_word(word):
            return word.translate(str.maketrans('', '', string.punctuation))

        words = [clean_word(w) for w in name.split()]
        qwords = [clean_word(q) for q in query_name.split()]
        stems = set()

        for qword in qwords:
            for word in words:
                if len(word) == 0 or len(qword) == 0:
                    continue
                phonetic_match = cls._phonetic_match(word, qword)
                # Count as a stem if phonetic_match is True or qword is a substring of word
                if phonetic_match:
                    stems.add(word)
                elif qword in word:
                    stems.add(qword)

        # find synonyms matches
        for word in words:
            for syn in synonyms:
                if len(word) == 0 or len(syn) == 0:
                    continue
                if word == syn or word in syn or syn in word:
                    stems.add(word)

        return list(stems)

    @classmethod
    def _get_name_without_designation(cls, name):
        if not name:
            return ''
        name = name.upper().strip()
        # Remove trailing designation phrase if present
        for designation in sorted(Designations.list(), key=lambda x: -len(x)):
            if name.endswith(' ' + designation) or name == designation:
                name = name[: -len(designation)].strip()
                break
        # Now filter out any remaining words that are in words_to_filter_from_name
        words = name.split()
        filtered_words = [word for word in words if word not in words_to_filter_from_name()]
        return ' '.join(filtered_words)

    @classmethod
    def get_possible_conflicts(cls, name, start=0, rows=100, exact_phrase='', distinctive='', descriptive=''):
        # q_name = cls._name_pre_processing(name)
        q_name = name.lower().strip()
        stripped_name = cls._get_name_without_designation(q_name)
        lookup_words = [
            *q_name.split(),
            *(distinctive or "").split(),
            *(descriptive or "").split(),
        ]
        synonym_families = load_browse_synonym_families(lookup_words)

        candidates = SolrClient.get_possible_conflicts(
            q_name,
            start,
            rows,
            exact_phrase=exact_phrase,
            distinctive=distinctive,
            descriptive=descriptive,
            synonym_families=synonym_families,
        )
        return cls._conflicts_post_process(candidates, stripped_name)

