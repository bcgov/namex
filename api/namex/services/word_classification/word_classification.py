from namex.models import db, WordClassification, WordClassificationSchema

from .token_classifier import TokenClassifier

from sqlalchemy import create_engine

POSTGRES_ADDRESS = 'localhost'
POSTGRES_PORT = '5432'
POSTGRES_USERNAME = 'postgres'
POSTGRES_PASSWORD = ''
POSTGRES_DBNAME = 'namex-local'
POSTGRES_DBNAME_WC = 'namex-local'

postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME,
                                                                                        password=POSTGRES_PASSWORD,
                                                                                        ipaddress=POSTGRES_ADDRESS,
                                                                                        port=POSTGRES_PORT,
                                                                                        dbname=POSTGRES_DBNAME))

postgres_wc_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME,
                                                                                           password=POSTGRES_PASSWORD,
                                                                                           ipaddress=POSTGRES_ADDRESS,
                                                                                           port=POSTGRES_PORT,
                                                                                           dbname=POSTGRES_DBNAME_WC))

cnx = create_engine(postgres_str)
cnx_wc = create_engine(postgres_wc_str)


class WordClassificationService:
    def __init__(self):
        pass

    def find_one(self, word=None):
        return WordClassification.find_word_classification(word)

    def create(self, word_classification):
        entity = self.find_one(word_classification.word) or None

        if not entity:
            entity = WordClassification()
            entity.word = word_classification['word']
            entity.classification = word_classification['classification']
            entity.lastNameUsed = word_classification['lastNameUsed']
            entity.lastPrepName = word_classification['lastPrepName']
            entity.frequency = word_classification['frequency']
            entity.approvedBy = word_classification['approvedBy']
            entity.approvedDate = word_classification['approvedDate']
            entity.startDate = word_classification['startDate']
            entity.endDate = word_classification['endDate']
            entity.lastUpdatedBy = word_classification['lastUpdatedBy']
            entity.lastUpdatedDate = word_classification['lastUpdatedDate']
            entity.save_to_db()

            return entity

        return None

    def update(self, word_classification):
        entity = self.find_one(word_classification.word) or None

        if entity:
            entity.word = word_classification['word']
            entity.classification = word_classification['classification']
            entity.lastNameUsed = word_classification['lastNameUsed']
            entity.lastPrepName = word_classification['lastPrepName']
            entity.frequency = word_classification['frequency']
            entity.approvedBy = word_classification['approvedBy']
            entity.approvedDate = word_classification['approvedDate']
            entity.startDate = word_classification['startDate']
            entity.endDate = word_classification['endDate']
            entity.lastUpdatedBy = word_classification['lastUpdatedBy']
            entity.lastUpdatedDate = word_classification['lastUpdatedDate']
            entity.save_to_db()

            return entity

        return None

    def create_or_update(self, word_classification):
        entity = self.find_one(word_classification.word) or None

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
