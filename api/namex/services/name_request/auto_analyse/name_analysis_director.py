# TODO: Name pre-processing has been moved to its own service
import pandas as pd

# Import mock API clients
from ..datasources.synonyms_api import SynonymsApi
from ..datasources.solr_api import SolrApi

from .name_analysis_utils import clean_name_words, data_frame_to_list

from namex.services.synonyms.synonym \
    import SynonymService

from namex.services.name_processing.name_processing \
    import NameProcessingService

from namex.services.word_classification.word_classification \
    import WordClassificationService

'''
This is the director for AutoAnalyseService.
'''


class NameAnalysisDirector:
    _builder = None  # Store a reference to the builder

    # Services
    _synonym_service = None
    _solr_conflicts_service = None
    _name_processing_service = None
    _word_classification_service = None

    # Data
    _prefixes = []
    _synonyms = []
    _substitutions = []
    _stop_words = []
    _designated_end_words = []
    _designated_any_words = []

    # Name + tokens
    _entity_type = None
    _name_as_submitted = ''
    _preprocessed_name = ''
    # _unclassifiable_words = []  # TODO: Or do we add these to list_none?
    _list_name_words = []
    _list_dist_words = []
    _list_desc_words = []
    _list_none_words = []

    # Conflicts
    _in_province_conflicts = []
    _all_conflicts = []

    def __init__(self):
        self._synonym_service = SynonymService()
        self._name_processing_service = NameProcessingService()
        self._word_classification_service = WordClassificationService()
        self._solr_conflicts_service = SolrApi()

    # Used by the builder to access the WordClassificationService instance
    def get_word_classification_service(self):
        return self._word_classification_service

    # Used by the builder to access the NameProcessingService instance
    def get_name_processing_service(self):
        return self._name_processing_service

    def use_builder(self, builder):
        self._builder = builder if builder else None
        if self._builder:
            self.prepare_data()

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

    def get_list_name(self):
        return self._list_name_words

    def get_list_dist(self):
        return self._list_dist_words

    def get_list_desc(self):
        return self._list_desc_words

    def get_list_none(self):
        return self._list_none_words

    def get_synonyms(self):
        return self._synonyms

    def get_substitutions(self):
        return self._substitutions

    def get_stop_words(self):
        return self._stop_words

    def get_designated_end_words(self):
        return self._designated_end_words

    def get_designated_any_words(self):
        return self._designated_any_words

    '''
    Split a name string into classifiable tokens. Called internally whenever set_name is invoked.
    @:param string:name
    '''
    def preprocess_name(self):
        wc_svc = self.get_word_classification_service()
        cf = pd.DataFrame(columns=['word', 'word_classification'])

        if not self._name_as_submitted:
            return  # TODO: Should we throw an error or something?

        # Clean the provided name and tokenize the string
        # Identify stop words, any words and end words an store the lists to our director instance
        self._list_name_words = clean_name_words(
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

    '''
    Prepare any data required by the analysis builder.
    '''
    def prepare_data(self):
        # Query database for synonyms, substitutions and designations
        self._synonyms = self._synonym_service.get_synonyms()
        self._substitutions = self._synonym_service.get_substitutions()

        self._stop_words = self._synonym_service.get_stop_words()
        #self._designated_end_words = self._synonym_service.get_designated_end_words()
        #self._designated_any_words = self._synonym_service.get_designated_any_words()
        self._designated_end_words = self._synonym_service.get_designated_end_all_words()
        self._designated_any_words = self._synonym_service.get_designated_end_all_words()

        # Solr calls TODO: Are we still using solr conflict? Clarify...
        self._in_province_conflicts = self._solr_conflicts_service.get_in_province_conflicts()
        self._all_conflicts = self._solr_conflicts_service.get_all_conflicts()

        self.configure_builder()

    def configure_builder(self):
        self._builder.set_entity_type(self._entity_type)
        self._builder.set_dicts(
            synonyms=self._synonyms,
            substitutions=self._substitutions,
            stop_words=self._stop_words,
            designated_end_words=self._designated_end_words,
            designated_any_words=self._designated_any_words,
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

        check_name_is_well_formed = builder.check_name_is_well_formed(
            self.get_list_dist(),
            self.get_list_desc(),
            self.get_list_none(),
            # TODO: We've already split the name in the director (get_list_name) why are we using the string here?
            # self.get_list_name()
            self.get_preprocessed_name()
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
