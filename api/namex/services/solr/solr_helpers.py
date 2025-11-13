import string

from namex.constants import Designations
from namex.services.solr import (
    words_to_filter_from_name
)
from namex.services.solr.solr_client import SolrClient


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
                highlighting = rcd.get("highlighting", {})
                exact = cls.normalize_words(highlighting.get("exact", []))
                stems = cls.normalize_words(highlighting.get("stems", []))
                synonyms = cls.normalize_words(highlighting.get("synonyms", []))

                rcd['type'] = 'similar'
                rcd['highlighting'] = { "exact": list(exact), "stems": list(stems), "synonyms": list(synonyms) }
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

