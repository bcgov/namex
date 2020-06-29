from namex.models import db, WordClassification, WordClassificationSchema
from datetime import datetime
from .token_classifier import TokenClassifier


class WordClassificationService:
    def __init__(self):
        pass

    def find_one(self, word=None):
        return WordClassification.find_word_classification(word)

    def find_one_by_class(self, word=None, classification=None):
        return WordClassification.find_word_by_classification(word, classification)

    def create(self, word_classification):

            entity = WordClassification()
            entity.word = word_classification['word']
            entity.classification = word_classification['classification']
            entity.lastNameUsed = word_classification['name']
            entity.lastPrepName = word_classification['name']
            entity.frequency = 1
            entity.approvedBy = word_classification['examiner']
            entity.approvedDate = datetime.utcnow
            entity.startDate = datetime.utcnow

            entity.lastUpdatedBy = word_classification['examiner']
            entity.lastUpdatedDate = datetime.utcnow
            entity.save_to_db()

            return entity



    def update(self, word_classification,entity):


        entity.lastNameUsed = word_classification['name']
        entity.lastPrepName = word_classification['name']
        entity.frequency = entity.frequency + 1

        entity.lastUpdatedBy = word_classification['examiner']
        entity.lastUpdatedDate = datetime.utcnow
        entity.save_to_db()

        return entity


    def create_or_update(self, word_classification):
        entity = self.find_one_by_class(word_classification.word,word_classification.classification) or None

        if not entity:
            return self.create(word_classification)
        else:
            return self.update(word_classification)

    def delete(self, word_classification):
        entity = self.find_one(word_classification.word) or None

        if entity:
            pass

    def validate(self):
        return True

    def classify_tokens(self, word_tokens):
        token_classifier = TokenClassifier(self)
        token_classifier.name_tokens = word_tokens
        return token_classifier
