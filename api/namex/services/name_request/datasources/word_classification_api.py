from namex.models import WordClassification, WordClassificationSchema


class WordClassificationApi:
    @staticmethod
    def get_word_classification(word):
        # df = pd.read_sql_query('select word,classification,counter from word_classification where word=' + "'" + \
        #                       word + "'", cnx)
        # return df
        pass

    @staticmethod
    def update_word_classification(word, classification):
        # stmt = word_classification.update(). \
        #    where(and_(word_classification.c.word == word,
        #               word_classification.c.classification == classification)). \
        #    values(counter=word_classification.c.counter + 1)
        # result = cnx.execute(stmt)

        # return result
        pass
