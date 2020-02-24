class GetSynonymsListsMixin(object):
    _prefixes = []
    _synonyms = []
    _substitutions = []
    _stop_words = []
    _designated_end_words = []
    _designated_any_words = []

    def get_prefixes(self):
        return self._prefixes

    def get_synonyms(self):
        return self._synonyms

    def get_substitutions(self):
        return self._substitutions

    def get_stop_words(self):
        return self._stop_words

    def get_designated_end_words(self):
        return self._designated_end_words

    def get_designated_any_words(self):
        return self._designated_any_words
