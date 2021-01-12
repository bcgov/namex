class GetSynonymListsMixin(object):
    _prefixes = []
    _synonyms = {}
    _compound_synonyms ={}
    _substitutions = {}
    _stop_words = []
    _number_words = []
    _stand_alone_words = []

    def get_prefixes(self):
        return self._prefixes

    def get_synonyms(self):
        return self._synonyms

    def get_compound_synonyms(self):
        return self._compound_synonyms

    def get_substitutions(self):
        return self._substitutions

    def get_stop_words(self):
        return self._stop_words

    def get_number_words(self):
        return self._number_words

    def get_stand_alone_words(self):
        return self._stand_alone_words
