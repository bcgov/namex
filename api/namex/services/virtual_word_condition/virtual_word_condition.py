from namex.models import VirtualWordCondition


class VirtualWordConditionService:
    _model = None

    def __init__(self):
        self._model = VirtualWordCondition

    def get_model(self):
        return self._model

    def get_words_to_avoid(self):
        words_to_avoid = self._model.get_words_to_avoid()
        return words_to_avoid

    def get_words_requiring_consent(self):
        words_requiring_consent = self._model.get_words_requiring_consent()
        return words_requiring_consent

    def get_word_special_use(self):
        word_special_use = self._model.get_word_special_use()
        return word_special_use
