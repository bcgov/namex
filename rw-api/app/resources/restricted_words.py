from flask import jsonify, g
from flask_restplus import Resource, cors
from app import api, db, oidc, app
from app.auth_services import required_scope
from app.utils.util import cors_preflight
from sqlalchemy import text, exc
import re
from itertools import filterfalse
import logging


@cors_preflight("GET")
@api.route('/echo', methods=['GET', 'OPTIONS'])
class Echo(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    @oidc.accept_token(require_token=True)
    def get (*args, **kwargs):
        try:
            return jsonify(g.oidc_token_info), 200
        except Exception as err:
            return jsonify({"error": "{}".format(err)}), 500

@cors_preflight("GET")
@api.route('/restricted_words/<string:corp_name>', methods=['GET','OPTIONS'])
class RequestRestrictedWords(Resource):
    """this checks each word in the given name against the restricted words in the db
        - returns all words that are restricted with their reason/conditions
    """

    @staticmethod
    @cors.crossdomain(origin='*')
    @oidc.accept_token(require_token=True)
    def get(corp_name):

        if not (required_scope("names_viewer")):  # User.VIEWONLY
            return {"message": "Error: You are not authorized to view corporate details."}, 403

        """ 1. put all possible restricted words/phrases in a list
                  - used later to compare against sql fn
               parse corp_name from snake_case into sql format
        """
        word_list = []
        corp_name_sql = ''
        word_count = -1
        new_word = True
        for letter in corp_name:
            if new_word:
                word_list.append(letter.upper())
                corp_name_sql += letter
                word_count += 1
                new_word = False
            elif letter != '_':
                word_list[word_count] += letter.upper()
                corp_name_sql += letter
            else:
                corp_name_sql += ' '
                new_word = True

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
        # print(word_list)
        """------------------------------------------------------"""

        """ 2. get words/phrases in corp_name that are restricted
                - these are compared to word_list because: 
                    i.e (the fn will return KIA if kial is in the corp_name)
        """

        get_restricted_words_sql = text("select get_restricted_words(\'{}\')".format(corp_name_sql))
        try:
            restricted_words_obj = db.engine.execute(get_restricted_words_sql)
        except exc.SQLAlchemyError:
            print(exc.SQLAlchemyError)
            return jsonify({"message": "An error occurred accessing the restricted words."}), 500
        except AttributeError:
            return jsonify({"message": "Could not find any restricted words."}), 404

        # insert try statement here
        restricted_word_ids = []
        regex_list = []
        try:
            restricted_words_str = restricted_words_obj.fetchall()[0][0]
            # print(restricted_words_str)
            restricted_word_ids = re.findall(r'word_id:(.*?)word_phrase:', restricted_words_str)
            regex_list = re.findall(r'word_phrase:(.*?)(\,|$)', restricted_words_str)
        except:
            pass
        restricted_words = [word[0] for word in regex_list]
        # print(restricted_words)
        restricted_words_dict = [{'id': id, 'phrase': phrase} for id, phrase in zip(restricted_word_ids, restricted_words)]
        # print(restricted_words_dict)

        # make sure all words in restricted_words_dict are in word_list
        restricted_words_dict[:] = [word for word in restricted_words_dict if word['phrase'] in word_list]

        # print(restricted_words_dict)
        """-----------------------------------------------------------------"""

        """ 3. get condition info based on word_id for each restricted word """

        restricted_words_conditions = []
        for word in restricted_words_dict:
            get_cnd_id_sql = text("select cnd_id from restricted_word_condition where word_id = {}".format(word['id']))
            try:
                cnd_id_obj = db.engine.execute(get_cnd_id_sql)
                # print(cnd_id_obj.fetchall())

                cnd_id = cnd_id_obj.fetchall()[0][0]
                # print(cnd_id)
                get_cnd_sql = text("select * from restricted_condition where cnd_id = {}".format(cnd_id))
                cnd_obj = db.engine.execute(get_cnd_sql)

                # print(cnd_obj.fetchall())
                cnd_info = cnd_obj.fetchall()[0]
                cnd_text = cnd_info[1]
                cnd_allow_use = cnd_info[2]
                cnd_consent_req = cnd_info[3]
                cnd_consent_body = cnd_info[4]
                cnd_instr = cnd_info[5]

                cnd_info = {'id': cnd_id,
                            'text': cnd_text,
                            'allow_use': cnd_allow_use,
                            'consent_required': cnd_consent_req,
                            'consenting_body': cnd_consent_body,
                            'instructions': cnd_instr}
                restricted_words_conditions.append({'word_info': word, 'cnd_info': cnd_info})
            except exc.SQLAlchemyError:
                print(exc.SQLAlchemyError)
                return jsonify(
                    {"message": "An error occurred accessing the condition for {}.".format(word['id'])}), 500
            except AttributeError:
                return jsonify({"message": "Could not find any condition info for {}.".format(word['id'])}), 404
            except:
                # print('error')
                cnd_info = 'Not Available'
                restricted_words_conditions.append({'word_info': word, 'cnd_info': cnd_info})
        """------------------------------------------------------------------------------------"""

        return jsonify({"restricted_words_conditions": restricted_words_conditions}), 200
