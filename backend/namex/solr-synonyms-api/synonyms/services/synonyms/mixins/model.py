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

    def get_all_categories_synonyms(self, list_d):
        aux_list = []
        dict_subs = {}

        for word in list_d:
            aux_list = [d.lower() for d in self.get_synonyms(word, True)]
            if aux_list:
                dict_subs.update({word: aux_list})
            else:
                dict_subs.update({word: None})

        # Return {'shop': ['beauty', 'store', 'sales', 'reatail'],
        #         'coffee': ['non-alcoholic-beverages','restaurant']} based on list_d
        return dict_subs
