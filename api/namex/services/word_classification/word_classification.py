from namex.models import WordClassification
from datetime import datetime

from namex.models import User
# from namex.services.name_request.utils import get_or_create_user_by_jwt

from .token_classifier import TokenClassifier


class WordClassificationService:
    def __init__(self):
        pass

    def find_one(self, word=None):
        return WordClassification.find_word_classification(word)

    def find_one_by_class(word=None, classification=None):
        return WordClassification.find_word_by_classification(word, classification)

    @classmethod
    def create(cls, word_classification, user_id):
        entity = WordClassification()
        entity.word = word_classification['word'].upper()
        entity.classification = word_classification['classification'].upper()
        entity.last_name_used = word_classification['name'].upper()
        entity.last_prep_name = word_classification['name'].upper()
        entity.frequency = 1
        entity.approved_by = user_id
        entity.approved_dt = datetime.utcnow()
        entity.start_dt = datetime.utcnow()
        entity.last_updated_by = user_id

        entity.save_to_db()

        return entity

    @classmethod
    def update(cls, entity, word_classification, user_id):
        for word in entity:
            word.frequency = word.frequency + 1
            word.last_name_used = word_classification['name'].upper()
            word.last_prep_name = word_classification['name'].upper()
            word.last_updated_by = user_id

        word.save_to_db()

        return word

    @classmethod
    def create_or_update(cls, word_classification):
        entity = cls.find_one_by_class(word_classification['word'], word_classification['classification']) or None

        # user = get_or_create_user_by_jwt(g.jwt_oidc_token_info)
        user = User.find_by_username(word_classification['examiner'])

        if not entity:
            return cls.create(word_classification, user.id)
        else:
            return cls.update(entity, word_classification, user.id)

    def classify_tokens(self, word_tokens):
        token_classifier = TokenClassifier(self)
        token_classifier.name_tokens = word_tokens
        return token_classifier
