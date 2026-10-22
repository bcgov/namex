from enum import Enum

from flask import current_app


def classifications_to_lists(classifications):
    """Convert list of classification dictionaries to separate lists by type."""
    list_dist = []
    list_desc = []
    list_none = []

    for item in classifications:
        classification = item['word_classification']
        word = item['word']

        if classification == DataFrameFields.DISTINCTIVE.value:
            list_dist.append(word)
        elif classification == DataFrameFields.DESCRIPTIVE.value:
            list_desc.append(word)
        elif classification == DataFrameFields.UNCLASSIFIED.value:
            list_none.append(word)

    return list_dist, list_desc, list_none


class DataFrameFields(Enum):
    FIELD_SYNONYMS = 'synonyms_text'
    FIELD_SPECIAL_WORDS = 'rc_words'
    DESCRIPTIVE = 'DESC'
    DISTINCTIVE = 'DIST'
    UNCLASSIFIED = 'NONE'


class TokenClassifier:
    @property
    def name_tokens(self):
        return self._name_tokens

    @name_tokens.setter
    def name_tokens(self, val):
        if isinstance(val, list) and val.__len__() > 0:
            self._name_tokens = val
            self._classify_tokens(self._name_tokens)

    @property
    def distinctive_word_tokens(self):
        return self._dist_tokens

    @distinctive_word_tokens.setter
    def distinctive_word_tokens(self, val):
        self._dist_tokens = val

    @property
    def descriptive_word_tokens(self):
        return self._desc_tokens

    @descriptive_word_tokens.setter
    def descriptive_word_tokens(self, val):
        self._desc_tokens = val

    @property
    def unclassified_word_tokens(self):
        return self._uc_tokens

    @unclassified_word_tokens.setter
    def unclassified_word_tokens(self, val):
        self._uc_tokens = val

    @property
    def word_classification_service(self):
        return self._word_classification_service

    @word_classification_service.setter
    def word_classification_service(self, svc):
        self._word_classification_service = svc

    def __init__(self, svc):
        self.word_classification_service = svc

        self.entity_type = None
        self.name_as_submitted = None
        self.processed_name = None
        self.name_tokens = []
        self.distinctive_word_tokens = []
        self.descriptive_word_tokens = []
        self.unclassified_word_tokens = []

    """
    Utility for adding unclassified words to distinctive and descriptive list
    Override the abstract / base class method
    @return list_dist, list_desc
    """

    @staticmethod
    def handle_unclassified_words(list_dist, list_desc, list_none, list_name):
        idx_dist = -1
        idx_desc = -1
        for word in list_name:
            if word in list_none:
                idx_dist += 1
                idx_desc += 1
                list_dist.insert(idx_dist, word)
                list_desc.insert(idx_desc, word)
            else:
                try:
                    idx_dist = list_dist.index(word)
                    idx_desc = list_desc.index(word)
                except ValueError:
                    pass

        return list_dist, list_desc

    def _classify_tokens(self, word_tokens):
        try:
            classifications = []

            wc_svc = self.word_classification_service

            # Get the word classification for each word in the supplied name name
            for word in word_tokens:
                word_classification = wc_svc.find_one(word)
                if not word_classification:
                    current_app.logger.debug('No word classification found for: ' + word)
                    classifications.append(
                        {'word': word.lower().strip(), 'word_classification': DataFrameFields.UNCLASSIFIED.value}
                    )
                else:
                    for row in word_classification:
                        classifications.append(
                            {'word': word.lower().strip(), 'word_classification': row.classification.strip()}
                        )

            self.distinctive_word_tokens, self.descriptive_word_tokens, self.unclassified_word_tokens = (
                classifications_to_lists(classifications)
            )

        except Exception as error:
            current_app.logger.error('Token classification failed! ' + repr(error))
            raise
