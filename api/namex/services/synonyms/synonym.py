from namex.models import Synonym


class SynonymService:
    _model = None

    def __init(self):
        # TODO: Not sure if we'll need this later once Model is done
        self._model = Synonym()

    @classmethod
    def get_synonyms(cls):
        return cls._model.get_synonym_list()

    @classmethod
    def get_substitutions(cls):
        return cls._model.get_substitution_list()

    @classmethod
    def get_stop_words(cls):
        return cls._model.get_stop_word_list()

    @classmethod
    def get_designated_start_words(cls):
        return []  # TODO: What is going on here?

    @classmethod
    def get_designated_end_words(cls):
        return cls._model.get_en_designation_end_list()

    @classmethod
    def get_designated_any_words(cls):
        return cls._model.get_en_designation_all_list()
