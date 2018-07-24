from flask import jsonify, current_app
from sqlalchemy import text, exc
from namex.models import db


class RestrictedWords(object):

    RESTRICTED_WORDS = 'restricted_words'
    VALID_QUERIES = [RESTRICTED_WORDS]

    @staticmethod
    def get_restricted_words_conditions(content):
        """ 1. put all possible restricted words/phrases in a list
                          - used later to compare against sql fn
                       parse corp_name from snake_case into sql format
        """
        word_list = content.upper().split()

        # this adds in all possible phrases that are two or more words to word_list
        phrases = []
        phrase = ''
        for indx, word in enumerate(word_list):
            for possible_phrase in word_list[indx:]:
                if phrase != '':
                    phrase += possible_phrase
                    phrases.append(phrase)
                else:
                    phrase += possible_phrase
                if indx < len(word_list):
                    phrase += ' '
            phrase = ''

        word_list = word_list + phrases
        """------------------------------------------------------"""

        """ 2. get words/phrases in corp_name that are restricted
                - query for list of all restricted words
                    - compare these words to word_list
        """

        get_all_restricted_words_sql = text("select * from restricted_word;")
        try:
            restricted_words_obj = db.engine.execute(get_all_restricted_words_sql)

        except exc.SQLAlchemyError as err:
            current_app.logger.debug(err.with_traceback(None))
            return None, 'An error occurred accessing the restricted words.', 500
        except AttributeError:
            return None, 'Could not find any restricted words.', 404
        restricted_words_dict = []
        for row in restricted_words_obj:
            for word in word_list:
                if row[1] == word:
                    restricted_words_dict.append({'id' :row[0] ,'phrase' :row[1]})
        """-----------------------------------------------------------------"""

        """ 3. get condition info based on word_id for each restricted word """

        restricted_words_conditions = []
        for word in restricted_words_dict:
            get_cnd_id_sql = text("select cnd_id from restricted_word_condition where word_id = {}".format(word['id']))
            try:
                cnd_id_obj = db.engine.execute(get_cnd_id_sql)
                cnd_ids = cnd_id_obj.fetchall()

                cnd_obj_list = []
                for id in cnd_ids:
                    cnd_id = id[0]
                    get_cnd_sql = text("select * from restricted_condition where cnd_id = {}".format(cnd_id))
                    cnd_obj_list.append(db.engine.execute(get_cnd_sql))

                cnd_info = []
                for obj in cnd_obj_list:
                    obj_tuple = obj.fetchall()[0]
                    cnd_text = obj_tuple[1]
                    cnd_allow_use = obj_tuple[2]
                    cnd_consent_req = obj_tuple[3]
                    cnd_consent_body = obj_tuple[4]
                    cnd_instr = obj_tuple[5]

                    cnd_info.append({'id': cnd_id,
                                     'text': cnd_text,
                                     'allow_use': cnd_allow_use,
                                     'consent_required': cnd_consent_req,
                                     'consenting_body': cnd_consent_body,
                                     'instructions': cnd_instr})
                restricted_words_conditions.append({'word_info': word, 'cnd_info': cnd_info})
            except exc.SQLAlchemyError as sql_err:
                current_app.logger.debug(sql_err.with_traceback(None))
                return None, 'An error occurred accessing the condition for {}.'.format(word['id']), 500
            except AttributeError:
                return None, 'Could not find any condition info for {}.'.format(word['id']), 404
            except Exception as err:
                current_app.logger.debug(err.with_traceback(None))
                cnd_info = 'Not Available'
                restricted_words_conditions.append({'word_info': word, 'cnd_info': cnd_info})
        """------------------------------------------------------------------------------------"""

        return {"restricted_words_conditions": restricted_words_conditions}, None, None
