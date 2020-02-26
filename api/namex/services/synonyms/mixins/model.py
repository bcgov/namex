from . import SynonymServiceMixin

"""
Model accessors for the Synonym service.
"""


class SynonymModelMixin(SynonymServiceMixin):
    def get_all_substitutions_synonyms(self, list_d, distinctive=True):
        aux_list = []
        dict_subs = {}

        for word in list_d:
            if distinctive:
                aux_list = self.get_substitutions(word)
            else:
                aux_list = self.get_synonyms(word)
            if aux_list:
                dict_subs.update({word: aux_list})
            else:
                dict_subs.update({word: [word.lower()]})

        # Return {'mountain': ['mount', 'mountain', 'mt', 'mtn']} based on list_d
        return dict_subs

    # TODO: Replace this method... use the models!
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

    # TODO: Replace this method... use the models!
    @classmethod
    def build_query_descriptive(cls, desc_substitution_list, query):
        for element in desc_substitution_list:
            query += " and lower(n.name) similar to "
            substitutions = ' ?| '.join(map(str, element))
            query += "'" + "%%( " + substitutions + " ?)%%" + "'"

        return query



