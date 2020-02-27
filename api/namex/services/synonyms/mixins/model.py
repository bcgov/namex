from . import SynonymServiceMixin

"""
Model accessors for the Synonym service.
"""


class SynonymModelMixin(SynonymServiceMixin):
    def get_query_distinctive(self, dist_all_permutations, length):
        query = self._model.build_query_distinctive(dist_all_permutations, length)
        return query

    def get_query_descriptive(self, desc_substitution_list, query):
        query = self._model.build_query_descriptive(desc_substitution_list, query)
        return query

    def get_synonym_list(self, word):
        synonym_list = self._model.get_synonym_list(word)
        return synonym_list

    def get_substitution_list(self, word):
        substitution_list = self._model.get_substitution_list(word)
        return substitution_list

    def get_all_substitutions_synonyms(self, list_d, distinctive=True):
        aux_list = []
        dict_subs = {}

        for word in list_d:
            if distinctive:
                aux_list = self.get_substitution_list(word)
            else:
                aux_list = self.get_synonym_list(word)
            if aux_list:
                dict_subs.update({word: aux_list})
            else:
                dict_subs.update({word: [word.lower()]})

        # Return {'mountain': ['mount', 'mountain', 'mt', 'mtn']} based on list_d
        return dict_subs

    def get_conflicts(self, query):
        conflicts = self._model.get_conflicts(query)
        return conflicts
