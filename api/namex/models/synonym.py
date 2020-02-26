import re
from . import db, ma

import pandas as pd
from sqlalchemy import and_

from namex.constants import AllEntityTypes

from namex.services.name_request.auto_analyse.name_analysis_utils import get_dataframe_list, get_flat_list
from ..services.name_request.auto_analyse import DataFrameFields

from namex.criteria.synonym.query_criteria import SynonymQueryCriteria

"""
- Models NEVER implement business logic, ONLY generic queries belong in here.
- Methods like find, find_one, or find_by_criteria belong in models.
- Methods like get_synonym_list or get_en_designation_end_all_list belong in a Service!
    - They belong in a Service because getting eg. a list of designations or synonyms is a USE case of the model,
      but getting a list of designations is not necessarily something that is inherent to the model; rather, that is
      what a particular user of the model wants to query for.
"""


# The class that corresponds to the database table for synonyms.
class Synonym(db.Model):
    __tablename__ = 'synonym'
    # TODO: What's the deal with this bind key?
    # __bind_key__ = 'synonyms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(100))
    synonyms_text = db.Column(db.String(1000), unique=True, nullable=False)
    stems_text = db.Column(db.String(1000), nullable=False)
    comment = db.Column(db.String(1000))
    enabled = db.Column(db.Boolean(), default=True)

    def json(self):
        return {"id": self.id, "category": self.category, "synonymsText": self.synonyms_text,
                "stemsText": self.stems_text, "comment": self.comment, "enabled": self.enabled}

    # TODO: Does this belong here?
    @classmethod
    def get_designation_by_entity_type(cls, entity_type):
        query = 'SELECT s.category, s.synonyms_text FROM synonym s WHERE lower(s.category) ~ ' + "'" + '^' + entity_type.lower() + '.*(english[_ -]+)+designation[s]?[_-]' + "'"
        df = pd.read_sql_query(query, con=db.engine)

        if not df.empty:
            designation_value_list = {
                re.sub(r'.*(any).*|.*(end).*', r'\1\2', x[0], 0, re.IGNORECASE): ''.join(x[1:]).split(",") for x in
                df.itertuples(index=False)}
            return designation_value_list

        return None

    # TODO: Does this belong here?
    @classmethod
    def get_entity_type_by_value(cls, entity_type_dicts, designation):
        entity_list = list()
        entity__designation_end_list = entity_type_dicts.items()
        print(entity__designation_end_list)
        for entity_designation in entity__designation_end_list:
            if any(designation in value for value in entity_designation[1]):
                entity_list.append(entity_designation[0])
        return entity_list

    '''
    Find a term by column.
    '''
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

    '''
    Query the model collection using an array of filters
    @:param filters An array of query filters eg. 
                    [
                      func.lower(model.category).op('~')(r'\y{}\y'.format('sub')),
                      func.lower(model.category).op('~')(r'\y{}\y'.format('prefix(es)?'))
                    ]
    '''
    @classmethod
    def find_by_criteria(cls, criteria=None):
        SynonymQueryCriteria.is_valid_criteria(criteria)

        query = cls.query.with_entities(*criteria.fields) \
            .filter(and_(*criteria.filters))

        # print(query.statement)
        return query.all()

    @classmethod
    def is_substitution_word(cls, word):
        df = pd.read_sql_query(
            'SELECT s.synonyms_text FROM synonym s where lower(s.category) LIKE ' + "'" + '%% ' + "sub'" + 'and ' + \
            's.synonyms_text ~ ' + "'" + '\y' + word.lower() + '\y' + "'", con=db.engine)
        if not df.empty:
            return True
        return False

    @classmethod
    def get_substitution_list(cls, word=None):
        if word:
            query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) LIKE ' + "'" + '%% ' + "sub'" + ' AND ' + \
                    's.synonyms_text ~ ' + "'" + '\y' + word.lower() + '\y' + "';"
        else:
            query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) LIKE ' + "'" + '%% ' + "sub'"

        df = pd.read_sql_query(query, con=db.engine)
        if not df.empty:
            response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
            response = get_flat_list(response)
            return response
        return None

    @classmethod
    def get_synonym_list(cls, word=None):
        if word:
            return cls.query_category(
                '!~* ' + "'" + '\w*(sub|stop)\s*$' + "'" + ' AND ' + 's.synonyms_text ~ ' + "'" + '\y' + word.lower() + '\y' + "';")

    @classmethod
    def get_stop_word_list(cls):
        return cls.query_category('~ ' + "'" + '^stop[_ -]+word[s]?' + "'")

    @classmethod
    def get_prefix_list(cls):
        return cls.query_category('~ ' + "'" + '^prefix(es)?' + "'")

    @classmethod
    def get_en_designation_any_all_list(cls):
        return cls.query_category('~ ' + "'" + '^(english[_ -]+)?designation[s]?[_-]any' + "'")

    @classmethod
    def get_en_designation_end_all_list(cls):
        return cls.query_category('~ ' + "'" + '^english[_ -]+designation[s]?[_-]+end' + "'")

    @classmethod
    def get_fr_designation_end_list(cls):
        return cls.query_category("'" + '(?=french[/_ -]+designation[s]?[/_-]+end)' + "'")

    @classmethod
    def get_stand_alone_list(cls):
        return cls.query_category('~ ' + "'" + '(?=stand[/_ -]?alone)' + "'")

    @classmethod
    def query_category(cls, category_query):
        if not category_query:
            raise ValueError('Invalid category provided')

        try:
            query = 'SELECT s.synonyms_text FROM synonym s WHERE lower(s.category) ' + category_query
            df = pd.read_sql_query(query, con=db.engine)
        except Exception as error:
            print('SQL error :' + repr(error))
            raise Exception(error)

        if not df.empty:
            response = get_dataframe_list(df, DataFrameFields.FIELD_SYNONYMS.value)
            response = get_flat_list(response)
            return response
        return None


    # TODO: Use real code types and complete this, so we can get rid of all the permutations...
    #  This should be okay with a string like "'" + '^ll.*(english[_ -]+)+designation[s]?[_-]end' + "'"
    #  I haven't worked out the other possibilities that are still in this class...
    @classmethod
    def get_entity_type_designation(cls, entity_type_code, position_code, lang='english'):
        code_str = entity_type_code.value
        position_str = position_code.value
        query = ''

        if code_str == AllEntityTypes.ALL.value:
            query = '~ ' + "'" + '^' + lang.lower() + '[_ -]+designation[s]?[_-]+' + position_str.lower() + "'"
        else:
            query = '~ ' + "'" + '^' + code_str.lower() + '.*(' + lang.lower() + '[_ -]+)+designation[s]?[_-]' + position_str.lower() + "'"

        results = cls.query_category(query)
        return results

    # TODO: Use real code types and complete this, so we can get rid of all the permutations
    @classmethod
    def get_entity_type_designations(cls, entity_type_codes, position_code, lang='english'):
        designations = dict.fromkeys(map(lambda c: c.value, entity_type_codes), [])

        for code in entity_type_codes:
            code_str = code.value
            designations[code_str] = cls.get_entity_type_designation(code, position_code, lang)

        return designations

    '''
    TODO: All these following methods could be refactored into a single method, really...
    '''

    # TODO: Need to move to requests/names model
    @classmethod
    def build_query_distinctive(cls, dist_all_permutations, length):
        query = "select n.name " + \
                "from requests r, names n " + \
                "where r.id = n.nr_id and " + \
                "r.state_cd IN ('APPROVED','CONDITIONAL') and " + \
                "r.request_type_cd IN ('PA','CR','CP','FI','SO', 'UL','CUL','CCR','CFI','CCP','CSO','CCC','CC') and " + \
                "n.state IN ('APPROVED','CONDITION') and " + \
                "lower(n.name) similar to " + "'"
        st = ''
        for s in range(length):
            st += '%s '

        permutations = "|".join(st % tup for tup in dist_all_permutations)
        query += "(" + permutations + ")%%" + "'"

        return query

    # TODO: Need to move to requests/names model
    @classmethod
    def build_query_descriptive(cls, desc_substitution_list, query):
        for element in desc_substitution_list:
            query += " and lower(n.name) similar to "
            substitutions = ' ?| '.join(map(str, element))
            query += "'" + "%%( " + substitutions + " ?)%%" + "'"

        return query

    # TODO: Need to move to requests/names model
    @classmethod
    def get_conflicts(cls, query):
        matches = pd.read_sql_query(query, con=db.engine)
        return matches


class SynonymSchema(ma.ModelSchema):
    class Meta:
        model = Synonym
