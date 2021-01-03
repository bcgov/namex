from . import SynonymServiceMixin

"""
Model accessors for the Synonym service.
"""


class SynonymModelMixin(SynonymServiceMixin):
    def get_all_substitutions_synonyms(self, list_d=None, distinctive=True):
        if list_d is None:
            list_d = []

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

        # eg. {'mountain': ['mount', 'mountain', 'mt', 'mtn']} based on list_d
        output = []
        for key in dict_subs:
            output.append({
                'key': key,
                'list': dict_subs[key]
            })

        return output

    def get_all_categories_synonyms(self, list_d=None):
        if list_d is None:
            list_d = []

        aux_list = []
        dict_subs = {}

        for word in list_d:
            aux_list = list(map(lambda d: d.lower(), self.get_synonyms(word, True)))
            if aux_list:
                dict_subs.update({word: aux_list})
            else:
                dict_subs.update({word: None})

        # eg. {'shop': ['beauty', 'store', 'sales', 'reatail'],
        #         'coffee': ['non-alcoholic-beverages','restaurant']} based on list_d
        output = []
        for key in dict_subs:
            output.append({
                'key': key,
                'list': dict_subs[key]
            })

        return output
