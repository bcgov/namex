from flask import current_app
from sqlalchemy import exc, text

from namex.models import db


class RestrictedWords(object):
    RESTRICTED_WORDS = 'restricted_words'
    VALID_QUERIES = [RESTRICTED_WORDS]

    @staticmethod
    def get_restricted_words_conditions(content):
        """Finds all restricted words and their conditions of the given string
        1. strips special chars + spaces
        2. finds all restricted words that are substrings of 'content'
        3. finds condition info with the 'word id' for each restricted word in 'content'
                - pairs each word with its condition info in a dict
        4. returns json containing the list of word/condition dicts
        """

        stripped_content = RestrictedWords.strip_content(content)

        try:
            restricted_words_dict = RestrictedWords.find_restricted_words(stripped_content)

        except exc.SQLAlchemyError as err:
            current_app.logger.debug(err.with_traceback(None))
            return None, 'An error occurred accessing the restricted words.', 500
        except AttributeError:
            return None, 'Could not find any restricted words.', 404

        # Get condition info based on each word_id and pair each word with its cnd_info in a dict
        restricted_words_conditions = []
        for word in restricted_words_dict:
            try:
                restricted_words_conditions.append(
                    {'word_info': word, 'cnd_info': RestrictedWords.find_cnd_info(word['id'])}
                )

            except exc.SQLAlchemyError as sql_err:
                current_app.logger.debug(sql_err.with_traceback(None))
                return None, 'An error occurred accessing the condition for {}.'.format(word['phrase']), 500
            except AttributeError:
                return None, 'Could not find any condition info for {}.'.format(word['id']), 404
            except Exception as err:
                current_app.logger.debug(err.with_traceback(None))
                cnd_info = 'Not Available'
                restricted_words_conditions.append({'word_info': word, 'cnd_info': cnd_info})

        return {'restricted_words_conditions': restricted_words_conditions}, None, None

    @staticmethod
    def strip_content(content):
        """Strip all special characters and spaces of given string
        - this will be compared against all restricted words/phrases in the db
        """
        return (
            ' '
            + content.upper()
            .replace('+', '')
            .replace('"', '')
            .replace('@', '')
            .replace('-', '')
            .replace('?', '')
            .replace('*', '')
            .replace('.', '')
            + ' '
        )

    @staticmethod
    def find_restricted_words(content):
        """Get words/phrases in 'content' that are restricted
        - query for list of all restricted words
            - strip each word/phrase of spaces and check if they are a substring of 'stripped_content'
        """
        restricted_words_obj = db.engine.execute('select * from restricted_word;')
        restricted_words_dict = []
        for row in restricted_words_obj:
            if ' ' + row[1].upper().strip() + ' ' in content:
                restricted_words_dict.append({'id': row[0], 'phrase': row[1].upper()})

        return restricted_words_dict

    @staticmethod
    def find_cnd_info(word_id):
        """Get the condition info corresponding to the given word id"""
        get_cnd_id_sql = text('select cnd_id from restricted_word_condition where word_id = {}'.format(word_id))
        cnd_id_obj = db.engine.execute(get_cnd_id_sql)
        cnd_ids = cnd_id_obj.fetchall()

        cnd_obj_list = []
        for id in cnd_ids:
            cnd_id = id[0]
            get_cnd_sql = text('select * from restricted_condition where cnd_id = {}'.format(cnd_id))
            cnd_obj_list.append(db.engine.execute(get_cnd_sql))

        cnd_info = []
        for obj in cnd_obj_list:
            obj_tuple = obj.fetchall()[0]
            cnd_text = obj_tuple[1]
            cnd_allow_use = obj_tuple[2]
            cnd_consent_req = obj_tuple[3]
            cnd_consent_body = obj_tuple[4]
            cnd_instr = obj_tuple[5]

            cnd_info.append(
                {
                    'id': cnd_id,
                    'text': cnd_text,
                    'allow_use': cnd_allow_use,
                    'consent_required': cnd_consent_req,
                    'consenting_body': cnd_consent_body,
                    'instructions': cnd_instr,
                }
            )

        return cnd_info
