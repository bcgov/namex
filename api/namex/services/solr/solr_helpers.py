import string

from namex.services.solr import (
    designations,
    first_consonants,
    first_vowels,
    has_leading_vowel,
    replace_special_leading_sounds,
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
    def _conflicts_post_process(cls, q_data, synonyms, query_name):
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
                rcd['type'] = 'similar'
                stems = cls._find_stems(nm, query_name, synonyms)
                rcd['stems'] = stems
                similar_matches.append(rcd)
        return {
            'names': similar_matches,
            'exactNames': exact_matches,
            'histories': histories}

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
        words = name.upper().split()
        filtered_words = [word for word in words if word not in designations()]
        return ' '.join(filtered_words)

    @classmethod
    def _phonetic_match(cls, word, query):
        # NOTE: The previous Solr search supported phonetic matching.
        # The current Solr service only matches exact words.
        # Business requirements for phonetic matching are unclear, and it is unknown if this feature will return.
        # This function is retained for possible future use if phonetic matching is reintroduced.
        word = replace_special_leading_sounds(word)
        query = replace_special_leading_sounds(query)

        word_has_leading_vowel = has_leading_vowel(word)
        query_has_leading_vowel = has_leading_vowel(query)

        word_first_consonant = first_consonants(word)
        query_first_consonant = first_consonants(query)

        query_first_vowels = first_vowels(query, query_has_leading_vowel)
        word_first_vowels = first_vowels(word, word_has_leading_vowel)

        if query_has_leading_vowel:
            query_sound = query_first_vowels + query_first_consonant
        else:
            query_sound = query_first_consonant + query_first_vowels

        if word_has_leading_vowel:
            word_sound = word_first_vowels + word_first_consonant
        else:
            word_sound = word_first_consonant + word_first_vowels

        if word_sound == query_sound:
            return True

        return False

    @classmethod
    def _keep_candidate(cls, candidate, name, names):
        if len([doc['id'] for doc in names if doc['id'] == candidate['id']]) == 0:
            names.append(
                {
                    'name': name,
                    'id': candidate['id'],
                    'source': candidate['source'],
                    'jurisdiction': candidate.get('jurisdiction', ''),
                    'start_date': candidate.get('start_date', ''),
                }
            )

    @classmethod
    def get_possible_conflicts(cls, name, start=0, rows=100):
        q_name = cls._name_pre_processing(name)
        q_name = cls._get_name_without_designation(q_name)

        candidates = SolrClient.get_possible_conflicts(q_name, start, rows)

        name_ngrams = cls._get_name_ngrams(q_name)
        synonyms = SolrClient.get_synonyms(name_ngrams)

        return cls._conflicts_post_process(candidates, synonyms, q_name)


    @classmethod
    def _get_name_ngrams(cls, name):
        """
        Given a name string, returns all contiguous word combinations (n-grams).
        Example: 'test name 123' -> ['test', 'test name', 'test name 123', 'name', 'name 123', '123']
        """
        words = name.split()
        ngrams = []
        for i in range(len(words)):
            for j in range(i + 1, len(words) + 1):
                ngram = ' '.join(words[i:j])
                ngrams.append(ngram)
        return ngrams