from . import db, ma

from enum import Enum

import pandas as pd
from sqlalchemy import create_engine

from namex.services.name_request.auto_analyse import field_synonyms, field_special_words
from namex.services.name_request.auto_analyse.name_analysis_utils import get_list_of_lists

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




# The class that corresponds to the database table for synonyms.
class Synonym(db.Model):
    __tablename__ = 'synonym'
    __bind_key__ = 'synonyms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(100))
    synonyms_text = db.Column(db.String(1000), unique=True, nullable=False)
    stems_text = db.Column(db.String(1000),nullable=False)
    comment = db.Column(db.String(1000))
    enabled = db.Column(db.Boolean(), default=True)

    def json(self):
        return {"id": self.id, "category": self.category, "synonymsText": self.synonyms_text,
                "stemsText": self.stems_text, "comment":self.comment, "enabled": self.enabled}

    @classmethod
    def find(cls, term, col):
        print('finding {} for {}'.format(col, term))
        synonyms_list = []
        term = term.lower()
        if col == 'synonyms_text':
            rows = cls.query.filter(Synonym.synonyms_text.ilike('%' + term + '%')).all()
            for row in rows:
                synonyms = [synonym.strip().lower() for synonym in row.synonyms_text.split(',')]
                if term in synonyms:
                    synonyms_list.append(row)
        # col == stems_text
        else:
            rows = cls.query.filter(Synonym.stems_text.ilike('%' + term + '%')).all()
            for row in rows:
                synonyms = [synonym.strip().lower() for synonym in row.stems_text.split(',')]
                if term in synonyms:
                    synonyms_list.append(row)

        return synonyms_list

    @classmethod
    def is_substitution_word(cls, word):
        df = pd.read_sql_query(
            'SELECT s.synonyms_text FROM synonym s where lower(s.category) LIKE ' + "'" + '%% ' + "sub'" + 'and ' + \
            's.synonyms_text ~ ' + "'" + '\\y' + word.lower() + '\\y' + "'", cnx)
        if not df.empty:
            return True
        return False

    @classmethod
    def get_substitution_list(cls, word=None):
        if word:
            query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) LIKE ' + "'" + '%% ' + "sub'" + ' AND ' + \
                's.synonyms_text ~ ' + "'" + '\\y' + word.lower() + '\\y' + "';"
        else:
            query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) LIKE ' + "'" + '%% ' + "sub'"

        df = pd.read_sql_query(query, cnx)
        if not df.empty:
            return get_list_of_lists(df, field_synonyms)
        return None

    @classmethod
    def get_synonym_list(cls, word=None):
        # TODO: That semi colon doesn't look right in there... confirm!
        if word:
            return cls.query_category("'" + '(?!(sub|stop)$)' + "'" + ' AND ' + \
                's.synonyms_text ~ ' + "'" + '\\y' + word.lower() + '\\y' + "';")

        return cls.query_category("'" + '(?!(sub|stop)$)' + "'")

    @classmethod
    def get_stop_word_list(cls):
        return cls.query_category("'" + '^stop[_ -]+word[s]?' + "'")

    @classmethod
    def get_prefix_list(cls):
        return cls.query_category("'" + '^prefix(es)?' + "'")

    @classmethod
    def get_en_designation_any_all_list(cls):
        return cls.query_category("'" + '^(english[_ -]+)?designation[s]?[_-]any' + "'")

    @classmethod
    def get_en_designation_end_all_list(cls):
        return cls.query_category("'" + '^english[_ -]+designation[s]?[_-]+end' + "'")

    @classmethod
    def get_fr_designation_end_list(cls):
        return cls.query_category("'" + '(?=french[/_ -]+designation[s]?[/_-]+end)' + "'")

    @classmethod
    def get_stand_alone_list(cls):
        return cls.query_category("'" + '(?=stand[/_ -]?alone)' + "'")

    @classmethod
    def query_category(cls, category_query):
        # TODO: Raise error if category not provided or None or empty
        query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + category_query
        df = pd.read_sql_query(query, cnx)

        if not df.empty:
            return get_list_of_lists(df, field_synonyms)
        return None

    # TODO: Use real code types
    #  This should be okay with a string like "'" + '^ll.*(english[_ -]+)+designation[s]?[_-]end' + "'"
    #  I haven't worked out the other possibilities that are still in this class...
    @classmethod
    def get_entity_type_designation(cls, entity_type_code, position_code, lang='english'):
        code_str = entity_type_code.value
        position_str = position_code.value

        query = "'" + '^' + code_str.lower() + '.*(' + lang.lower() + '[_ -]+)+designation[s]?[_-]' + position_str.lower() + "'"
        results = cls.query_category(query)
        return results

    # TODO: Use real code types and complete this
    @classmethod
    def get_entity_type_designations(cls, entity_type_codes, position_code, lang='english'):
        designations = dict.fromkeys(map(lambda c: c.value, entity_type_codes), [])

        for code in entity_type_codes:
            code_str = code.value
            designations[code_str] = cls.get_entity_type_designation(code, position_code, lang)

        return designations


class SynonymSchema(ma.ModelSchema):
    class Meta:
        model = Synonym
