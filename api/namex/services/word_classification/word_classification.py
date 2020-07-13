from namex.models import WordClassification
from datetime import datetime
from .token_classifier import TokenClassifier


class WordClassificationService:
    def __init__(self):
        pass

    @classmethod
    def find_one(cls, word=None):
        results = WordClassification.find_one(word)
        return results[0] if len(results) > 0 else None

    @classmethod
    def create(cls, word_classification):
        entity = WordClassification()
        entity.word = word_classification['word'].upper()
        entity.classification = word_classification['classification'].upper()
        entity.last_name_used = word_classification['name'].upper()
        entity.last_prep_name = word_classification['name'].upper()
        entity.frequency = 1
        # Note that this is NOT a string value, we require an FK ID
        # entity.approved_by = word_classification['examiner']  # TODO: Where does this ID come from?
        entity.approved_dt = str(datetime.utcnow())
        entity.start_dt = str(datetime.utcnow())
        # Note that this is NOT a string value, we require an FK I
        # entity.last_updated_by = word_classification['examiner']  # TODO: Where does this ID come from?
        entity.last_updated_dt = str(datetime.utcnow())
        entity.save_to_db()

        return entity

    @classmethod
    def update(cls, entity, word_classification):
        entity.word = word_classification['word'].upper()
        entity.classification = word_classification['classification'].upper()
        entity.last_name_used = word_classification['name'].upper()
        entity.last_prep_name = word_classification['name'].upper()
        entity.frequency = entity.frequency + 1
        # Note that this is NOT a string value, we require an FK ID
        # entity.approved_by = word_classification['examiner']  # TODO: Where does this ID come from?
        # entity.approved_dt = str(datetime.utcnow())
        # entity.start_dt = str(datetime.utcnow())
        # Note that this is NOT a string value, we require an FK I
        # entity.last_updated_by = word_classification['examiner']  # TODO: Where does this ID come from?
        entity.last_updated_dt = str(datetime.utcnow())
        entity.save_to_db()

        return entity

    @classmethod
    def create_or_update(cls, word_classification):
        entity = WordClassification.find_one_by_class(
            word_classification['word'],
            word_classification['classification']
        ) or None

        if not entity:
            return cls.create(word_classification)
        else:
            return cls.update(entity, word_classification)

    @classmethod
    def delete(cls, word):
        entity = WordClassification.find_one(word) or None

        if entity:
            entity.delete_from_db()

    @classmethod
    def validate(cls):
        return True

    def classify_tokens(self, word_tokens):
        token_classifier = TokenClassifier(self)
        token_classifier.name_tokens = word_tokens
        return token_classifier
