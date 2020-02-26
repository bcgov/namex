# TODO: Name pre-processing has been moved to its own service
import collections
import warnings

import pandas as pd

from .name_analysis_utils import data_frame_to_list, remove_french

from namex.models import Synonym

from .mixins.get_synonyms_lists import GetSynonymsListsMixin
from .mixins.get_word_classification_lists import GetWordClassificationListsMixin

from namex.services.synonyms.synonym \
    import SynonymService

# from namex.services.name_processing.name_processing \
#    import NameProcessingService

from namex.services.word_classification.word_classification \
    import WordClassificationService

from namex.services.virtual_word_condition.virtual_word_condition \
    import VirtualWordConditionService

'''
This is the director for AutoAnalyseService.
'''


class NameAnalysisDirector(GetSynonymsListsMixin, GetWordClassificationListsMixin):
    _builder = None  # Store a reference to the builder
    _model = None

    # Services
    _synonym_service = None
    _solr_conflicts_service = None
    _name_processing_service = None
    _word_classification_service = None
    _virtual_word_condition_service = None

    # Data
    _prefixes = []
    _synonyms = []
    _substitutions = []
    _stop_words = []

    _designated_end_words = []  # Check if this is used
    _designated_any_words = []  # Check if this is used

    # Designations
    # Designation_any_list_user and designation_end_list_user based on entity type typed by user:
    _designation_any_list_user = []
    _designation_end_list_user = []
    _all_designations_user = []
    # All designations for entity type typed bu user
    designations_entity_type_user = []
    # Designation_any_list and designation_end_list based on company name typed by user
    _designation_any_list = []
    _designation_end_list = []
    _all_designations = []
    # Wrong any_list and end_list based on company name typed by user
    _wrong_designation_any_list = []
    _wrong_designation_end_list = []
    _wrong_designation_place = []
    # Entity type(s) for designations related to company name typed by user:
    _entity_type_any_designation = []
    _entity_type_end_designation = []
    # All possible entity types found related to company name.
    _all_entity_type = []

    _entity_end_designation_dict = {}
    _entity_any_designation_dict = {}

    # Name + tokens
    _entity_type = None
    _name_as_submitted = ''
    _preprocessed_name = ''
    # _unclassifiable_words = []  # TODO: Or do we add these to list_none?

    # Conflicts
    _in_province_conflicts = []
    _all_conflicts = []

    def __init__(self):
        self._synonym_service = SynonymService()
        # TODO: Finish moving name processing out into its own service!
        # self._name_processing_service = NameProcessingService()
        self._word_classification_service = WordClassificationService()
        self._virtual_word_condition_service = VirtualWordConditionService()
        self._model = Synonym
        # self._solr_conflicts_service = SolrApi()

    # Used by the builder to access the WordClassificationService instance
    def get_word_classification_service(self):
        return self._word_classification_service

    # Used by the builder to access the SynonymService instance
    def get_synonym_service(self):
        return self._synonym_service

    # Used by the builder to access the NameProcessingService instance
    def get_name_processing_service(self):
        return self._name_processing_service

    # Used by the builder to access the VirtualWordConditionService instance
    def get_virtual_word_condition_service(self):
        return self._virtual_word_condition_service

    def use_builder(self, builder):
        self.builder = builder if builder else None

    # TODO: Raise an exception if entity type is not set!!!
    # TODO: Validate entity types against valid types
    def get_entity_type(self):
        return self._entity_type

    def set_entity_type(self, entity_type):
        self._entity_type = entity_type

    '''
    Set and preprocess a submitted name string using the preprocess_name class method.
    '''

    def set_name(self, name):
        # Process the name
        self._name_as_submitted = name  # Store the user's submitted name string
        self.preprocess_name()

    # API for extending implementations
    def get_name(self):
        return self._name_as_submitted

    def set_preprocessed_name(self, name):
        # Process the name
        self._preprocessed_name = name  # Store the user's submitted name string

    # API for extending implementations
    def get_preprocessed_name(self):
        return self._preprocessed_name

    '''
    Split a name string into classifiable tokens. Called internally whenever set_name is invoked.
    @:param string:name
    '''

    def preprocess_name(self):
        try:
            syn_svc = self.get_synonym_service()
            wc_svc = self.get_word_classification_service()
            cf = pd.DataFrame(columns=['word', 'word_classification'])

            if not self._name_as_submitted:
                return  # TODO: Should we throw an error or something?

            # Clean the provided name and tokenize the string
            # Identify stop words, any words and end words an store the lists to our director instance
            # self._list_name_words = syn_svc.clean_name_words  # TODO: Use this one!
            self._list_name_words = self.clean_name_words(
                self._name_as_submitted,
                self._stop_words,
                self._designated_any_words,
                self._designated_end_words,
                [],
                self._prefixes
            )

            # Get the word classification for each word in the supplied name name
            for word in self._list_name_words:
                word_classification = wc_svc.find_one(word)
                if not word_classification:
                    print('No word classification found for: ' + word)
                    new_row = {'word': word.lower().strip(), 'word_classification': 'none'}
                else:
                    for row in word_classification:
                        new_row = {'word': word.lower().strip(),
                                   'word_classification': row.classification.strip()}
                        cf = cf.append(new_row, ignore_index=True)

            # TODO: If we don't find a classification, we should be adding a record and return the unclassified word issue
            # TODO: Related to the above, we will need to pre-populate a list of classified words

            # Store results to instance
            # self._list_name_words, # TODO: data_frame_to_list used to return _list_name words... why did we move away from that?
            self._list_dist_words, self._list_desc_words, self._list_none_words = data_frame_to_list(cf)

            # Store clean, preprocessed name to instance
            self.set_preprocessed_name(' '.join(map(str, self.get_list_name())))
            self.configure_builder()  # Update builder dicts
        except Exception:
            print('Pre-processing name failed')

    # TODO: Isn't there another version of this already?
    def clean_name_words(self, text, stop_words=[], designation_any=[], designation_end=[], fr_designation_end_list=[],
                         prefix_list=[]):
        if not text or not stop_words or not designation_any or not designation_end or not prefix_list:
            warnings.warn(
                "Parameters in clean_name_words function are not set.",
                Warning
            )
        words = text.lower()
        words = ' '.join([word for x, word in enumerate(words.split(" ")) if x == 0 or word not in stop_words])
        words = remove_french(words, fr_designation_end_list)
        tokens = self._synonym_service.regex_transform(words, designation_any, designation_end, prefix_list)
        tokens = tokens.split()

        return [x.lower() for x in tokens if x]

    '''
    Prepare any data required by the analysis builder.
    '''

    def prepare_data(self):
        # Query database for synonyms, substitutions and designations
        self._synonyms = self._synonym_service.get_synonyms()
        self._substitutions = self._synonym_service.get_substitutions()
        self._prefixes = self._synonym_service.get_prefixes()

        self._stop_words = self._synonym_service.get_stop_words()
        self._designated_end_words = self._synonym_service.get_designated_end_all_words()
        self._designated_any_words = self._synonym_service.get_designated_any_all_words()

        self.configure_builder()

    def configure_builder(self):
        self._builder.set_entity_type(self._entity_type)
        self._builder.set_dicts(
            synonyms=self._synonyms,
            substitutions=self._substitutions,
            stop_words=self._stop_words,
            designated_end_words=self._designated_end_words,
            designated_any_words=self._designated_any_words,
            designation_end_list_user=self._designation_end_list_user,
            designation_any_list_user=self._designation_any_list_user,
            entity_end_designation_dict=self._entity_end_designation_dict,
            entity_any_designation_dict=self._entity_any_designation_dict,
            in_province_conflicts=self._in_province_conflicts,
            all_conflicts=self._all_conflicts
        )

    '''
    This is the main execution call for the class. Perform checks to ensure the name is well formed. 
    If the name is well formed, proceed with our analysis by calling do_analysis.
    
    if you don't want to check to see if a name is well formed first, override check_name_is_well_formed in
    the supplied builder.
    @:return ProcedureResult[]
    '''

    def execute_analysis(self):
        builder = self._builder

        results = []
        if self.get_list_none():
            self._list_dist_words, self._list_desc_words = builder.handle_unclassified_words(self.get_list_dist(),
                                                                                             self.get_list_desc(),
                                                                                             self.get_list_none(),
                                                                                             self.get_list_name())

        check_name_is_well_formed = builder.check_name_is_well_formed(
            self.get_list_dist(),
            self.get_list_desc(),
            self.get_list_name()
        )

        if not check_name_is_well_formed.is_valid:
            results.append(check_name_is_well_formed)
            return results
            #  Do not continue

        # TODO: Persist preprocessed name here?
        return results + self.do_analysis()

    # This is the main execution call for the class
    def do_analysis(self):
        raise NotImplementedError('do_analysis must be implemented in extending classes')

    # Get the company's designation if it's in the name
    def get_name_designation(self):
        pass

    def set_designations_by_entity_type_user(self, entity_type_user):
        designations_entity_type_user = self._model.get_designation_by_entity_type(entity_type_user)

        for k, v in designations_entity_type_user.items():
            if k.lower() == 'any':
                self._designation_any_list_user.extend(v)
            else:
                self._designation_end_list_user.extend(v)

    def set_designations_by_input_name(self, name):
        self._designation_any_list = self.get_synonym_service().get_designation_any_in_name(name)
        self._designation_end_list = self.get_synonym_service().get_designation_end_in_name(name)

    def set_wrong_designation_by_input_name(self, name):
        self._wrong_designation_any_list = self.get_synonym_service().get_wrong_place_any_designations(name)
        self._wrong_designation_end_list = self.get_synonym_service().get_wrong_place_end_designations(name)

        self._wrong_designation_place = self._wrong_designation_any_list + self._wrong_designation_end_list

    def get_wrong_designation_by_input_name(self):
        return self._wrong_designation_place

    def set_entity_type_any_designation(self, entity_any_designation_dict, designation_any_list):
        self._entity_type_any_designation = self.get_synonym_service().get_entity_type_any_designation(
            self.get_synonym_service().get_all_end_designations(),
            designation_any_list)

    def get_entity_type_any_designation(self):
        return self._entity_type_any_designation

    def set_entity_type_end_designation(self, entity_end_designation_dict, designation_end_list):
        self._entity_type_end_designation = self.get_synonym_service().get_entity_type_end_designation(
            self.get_synonym_service().get_all_any_designations(),
            designation_end_list)

    def get_entity_type_end_designation(self):
        return self._entity_type_end_designation

    def set_all_entity_types(self):
        self._all_entity_types = [item for item, count in
                                  collections.Counter(
                                      self._entity_type_any_designation + self._entity_type_end_designation).items()
                                  if
                                  count > 1]
        if not self._all_entity_types:
            self._all_entity_types = self._entity_type_any_designation + self._entity_type_end_designation

    def get_all_entity_types(self):
        return self._all_entity_types

    def set_all_designations_user(self):
        self._all_designations_user = self._designation_any_list_user + self._designation_end_list_user

    def get_all_designations_user(self):
        return self._all_designations_user

    def set_all_designations(self):
        self._all_designations = self._designation_any_list + self._designation_end_list

    def get_all_designations(self):
        return self._all_designations
