import re
import string

from namex.constants import Designations
from namex.services.solr import words_to_filter_from_name
from namex.services.solr.solr_client import SolrClient


class SolrHlpers:
    @classmethod
    def _name_pre_processing(cls, name):
        if not name:
            return ''

        # Replace ampersands and pluses with space (e.g. H&H -> H H)
        processed_name = re.sub(r'([&+])', ' ', name.lower())

        # Currency symbol replacements
        processed_name = (
            processed_name
            .replace(' $ ', ' dollar ')
            .replace('$', 's')
            .replace(' ¢ ', ' cent ')
            .replace('¢', 'c')
        )

        # Region standardization (british columbia / britishcolumbian(s) -> bc)
        processed_name = re.sub(r'\bbritish\s*columbia(ns|n|s)?\b|\bbritishcolumbia(ns|n|s)?\b', 'bc', processed_name)

        # Regex removal of punctuation & Solr special characters
        rmv_spec_chars_rgx = r"([\[\]!()\"~*?:/\\={}^%`#|<>,.@$;_\-])"
        processed_name = re.sub(rmv_spec_chars_rgx, ' ', processed_name)

        return ' '.join(processed_name.split())

    @classmethod
    def _compress_name(cls, name: str) -> str:
        """Return name with spaces and non-alphanumeric characters removed."""
        return re.sub(r'[^a-zA-Z0-9]', '', name or '').upper()

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
            rcd_name = cls._name_pre_processing(rcd.get('name', ''))
            nm = cls._get_name_without_designation(rcd_name)
            if cls._compress_name(nm) == cls._compress_name(query_name):
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
    def get_possible_conflicts(cls, name, start=0, rows=100):
        q_name = cls._name_pre_processing(name)
        q_name = cls._get_name_without_designation(q_name)

        candidates = SolrClient.get_possible_conflicts(q_name, start, rows)
        return cls._conflicts_post_process(candidates, q_name)

