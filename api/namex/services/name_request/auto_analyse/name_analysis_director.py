import os

from swagger_client import SynonymsApi as SynonymService

from namex.constants import BCUnprotectedNameEntityTypes
from namex.services.name_processing.mixins.get_synonym_lists import GetSynonymListsMixin
from namex.services.name_processing.name_processing \
    import NameProcessingService
from namex.services.virtual_word_condition.virtual_word_condition \
    import VirtualWordConditionService
from namex.services.word_classification.token_classifier \
    import TokenClassifier
from namex.services.word_classification.word_classification \
    import WordClassificationService
from . import AnalysisIssueCodes
from .mixins.get_designations_lists import GetDesignationsListsMixin
from .mixins.get_word_classification_lists import GetWordClassificationListsMixin
from ..auto_analyse.name_analysis_utils import get_classification

'''
This is the director for AutoAnalyseService.
'''

auto_analyze_config = os.getenv('AUTO_ANALYZE_CONFIG')


class NameAnalysisDirector(GetSynonymListsMixin, GetDesignationsListsMixin, GetWordClassificationListsMixin):
    @property
    def word_classification_service(self):
        return self._word_classification_service

    @word_classification_service.setter
    def word_classification_service(self, svc):
        self._word_classification_service = svc

    @property
    def word_condition_service(self):
        return self._word_condition_service

    @word_condition_service.setter
    def word_condition_service(self, svc):
        self._word_condition_service = svc

    @property
    def synonym_service(self):
        return self._synonym_service

    @synonym_service.setter
    def synonym_service(self, svc):
        self._synonym_service = svc

    @property
    def name_processing_service(self):
        return self._name_processing_service

    @name_processing_service.setter
    def name_processing_service(self, svc):
        self._name_processing_service = svc

    @property
    def token_classifier_service(self):
        return self._token_classifier_service

    @token_classifier_service.setter
    def token_classifier_service(self, svc):
        self._token_classifier_service = svc

    @property
    def builder(self):
        return self._builder

    @builder.setter
    def builder(self, builder):
        self._builder = builder

    #    @property
    #    def model(self):
    #        return Synonym

    @property
    def entity_type(self):
        return self._entity_type

    @entity_type.setter
    def entity_type(self, entity_type):
        self._entity_type = entity_type

    @property
    def name_tokens(self):
        np_svc = self.name_processing_service
        return self.name_processing_service.name_tokens if np_svc else ''

    @property
    def compound_descriptive_name_tokens(self):
        np_svc = self.name_processing_service
        return self.name_processing_service.compound_descriptive_name_tokens if np_svc else ''

    @property
    def name_tokens_search_conflict(self):
        np_svc = self.name_processing_service
        return self.name_processing_service.name_tokens_search_conflict if np_svc else ''

    @property
    def name_original_tokens(self):
        np_svc = self.name_processing_service
        return self.name_processing_service.name_original_tokens if np_svc else ''

    @property
    def token_classifier(self):
        return self._token_classifier

    @token_classifier.setter
    def token_classifier(self, token_classifier):
        self._token_classifier = token_classifier

    @property
    def skip_search_conflicts(self):
        return self._skip_search_conflicts

    @skip_search_conflicts.setter
    def skip_search_conflicts(self, skip_search_conflicts):
        self._skip_search_conflicts = skip_search_conflicts

    @property
    def word_classification_tokens(self):
        return \
            self.token_classifier.distinctive_word_tokens, \
            self.token_classifier.descriptive_word_tokens, \
            self.token_classifier.unclassified_word_tokens

    @property
    def processed_name(self):
        np_svc = self.name_processing_service
        return self.name_processing_service.processed_name if np_svc else ''

    @property
    def name_as_submitted(self):
        np_svc = self.name_processing_service
        return self.name_processing_service.name_as_submitted if np_svc else ''

    @property
    def name_as_submitted_tokenized(self):
        """
        name_as_submitted_tokenized tokenize the original name and when there is a compound designation made of more than one
        word, the term is counted as token. For instance, designations such as limited liability company is counted as one token.
        """
        np_svc = self.name_processing_service
        return self.name_processing_service.name_as_submitted_tokenized if np_svc else ''

    @property
    def original_name(self):
        """
        Just an alias for name_as_submitted
        """
        return self.name_as_submitted

    @property
    def original_name_tokenized(self):
        return self.name_as_submitted_tokenized

    def __init__(self):
        # TODO: Swap this out for the actual service we don't want to call service via API, it's too slow
        self.synonym_service = SynonymService()
        self.word_classification_service = WordClassificationService()
        self.word_condition_service = VirtualWordConditionService()
        self.name_processing_service = NameProcessingService()
        self.token_classifier_service = TokenClassifier(self.synonym_service)

        self.builder = None
        self.token_classifier = None

        self.entity_type = None
        self.skip_search_conflicts = False

    # Call this method from whatever is using this director
    def use_builder(self, builder):
        self.builder = builder if builder else None

    # Convenience method for extending implementations
    def get_entity_type(self):
        return self.entity_type

    # Convenience method for extending implementations
    def set_entity_type(self, entity_type):
        self.entity_type = entity_type

    # Convenience method for extending implementations
    def get_skip_search_conflicts(self):
        return self._skip_search_conflicts

    # Convenience method for extending implementations
    def set_skip_search_conflicts(self, skip_search_conflicts):
        self.skip_search_conflicts = skip_search_conflicts

    # API for extending implementations
    def get_name_tokens(self):
        return self.name_tokens

    # API for extending implementations
    def set_name_tokens(self, name_tokens):
        self.name_processing_service.name_tokens = name_tokens

    # API for extending implementations
    def get_compound_descriptive_name_tokens(self):
        return self.compound_descriptive_name_tokens

    # API for extending implementations
    def set_compound_descriptive_name_tokens(self, name_tokens):
        self.name_processing_service.compound_descriptive_name_tokens = name_tokens

    # API for extending implementations
    def get_name_tokens_search_conflict(self):
        return self.name_tokens_search_conflict

    # API for extending implementations
    def set_name_tokens_search_conflict(self, name_tokens_search_conflict):
        self.name_processing_service.name_tokens_search_conflict = name_tokens_search_conflict

    # API for extending implementations
    # TODO: Just for backward compat. et rid of this when we are done refactoring!
    def get_name(self):
        return self.name_tokens

    # API for extending implementations
    def get_original_name(self):
        return self.original_name

    # API for extending implementations
    def get_processed_name(self):
        return self.processed_name

    def get_original_name_tokenized(self):
        return self.original_name_tokenized

    def set_name(self, name, np_svc_prep_data):
        """
        Set and preprocess a submitted name string.
        Setting the name using np_svc.set_name will clean the name and set the following properties:
        @:prop name_as_submitted The original name string
        @:prop processed_name The cleaned name
        @:prop name_tokens Word tokens generated from the cleaned name
        """
        np_svc = self.name_processing_service
        # Lucas - this is just in here for reference while I merge
        # np_svc_prep_data = self.name_processing_service
        wc_svc = self.word_classification_service

        # Lucas - this is just in here for reference while I merge
        # np_svc_prep_data.prepare_data()
        np_svc.set_name(name, np_svc_prep_data)
        np_svc.set_name_tokenized(np_svc.name_first_part)

        self._list_name_words = np_svc.name_tokens

        # Classify the tokens that were created by NameProcessingService
        self.token_classifier = wc_svc.classify_tokens(np_svc.name_tokens)

    def set_synonym_dictionaries(self):
        np_svc = self.name_processing_service
        np_svc.set_compound_synonyms_dictionary(self._list_name_words)
        np_svc.set_synonyms_dictionary(np_svc.compound_descriptive_name_tokens)

    def execute_analysis(self):
        """
        This is the main execution call that wraps name analysis checks.
        - Perform checks to ensure the name is well formed.
        - If the name is well formed, proceed with our analysis by calling do_analysis.
        - If you don't want to check to see if a name is well formed first, override check_name_is_well_formed in the supplied builder.
        @:return ProcedureResult[]
        """
        try:
            builder = self.builder
            syn_svc = self.synonym_service
            wc_svc = self.word_classification_service
            token_svc = self.token_classifier_service
            np_svc = self.name_processing_service
            stand_alone_words = np_svc.get_stand_alone_words()

            analysis = []

            # Configure the analysis for the supplied builder
            get_classification(self, self.name_tokens, wc_svc, token_svc, np_svc.get_compound_synonyms(),
                               np_svc.get_synonyms())

            check_name_is_well_formed = None  # PEP8 Make sure it exists before assignment
            analysis_issues_sort_order = []  # PEP8 Make sure it exists before assignment

            # Get substitutions for distinctives:
            self._substitutions = builder.get_substitutions_distinctive(self.get_list_dist())
            self._dict_dist_words = self._substitutions

            check_name_is_well_formed = None  # Make sure it exists before assignment
            analysis_issues_sort_order = []  # Make sure it exists before assignment

            if auto_analyze_config in ('WELL_FORMED_NAME', 'EXACT_MATCH', 'SEARCH_CONFLICTS'):
                check_words_to_avoid = builder.check_words_to_avoid(self.name_tokens, self.processed_name)
                if not check_words_to_avoid.is_valid:
                    analysis.append(check_words_to_avoid)
                    return analysis

                self.set_skip_search_conflicts(True)
                check_name_is_well_formed = builder.check_name_is_well_formed(
                    self._dict_name_words,
                    self._list_dist_words,
                    self._list_desc_words,
                    self.compound_descriptive_name_tokens,
                    self.processed_name,
                    self.name_original_tokens
                )
                if check_name_is_well_formed.result_code in (
                        AnalysisIssueCodes.ADD_DISTINCTIVE_WORD, AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD) and \
                        self.entity_type not in (BCUnprotectedNameEntityTypes.list()) and \
                        not check_name_is_well_formed.is_valid:
                    analysis.append(check_name_is_well_formed)
                elif check_name_is_well_formed.result_code == AnalysisIssueCodes.CORPORATE_CONFLICT:
                    self.set_skip_search_conflicts(True)
                else:
                    self.set_skip_search_conflicts(False)

                check_name_has_valid_number = builder.is_valid_year(self.name_original_tokens)
                if not check_name_has_valid_number.is_valid:
                    analysis.append(check_name_has_valid_number)
                    return analysis

                if analysis:
                    return analysis

                check_word_limit = builder.check_word_limit(self.name_tokens)
                if not check_word_limit.is_valid:
                    analysis.append(check_word_limit)
                    return analysis

                check_word_unclassified = builder.check_unclassified_words(self.name_tokens, self.get_list_none())
                if not check_word_unclassified.is_valid:
                    analysis.append(check_word_unclassified)

                # If the error coming back is that a name is not well formed
                # OR if the error coming back has words to avoid...
                # eg. result.result_code = AnalysisIssueCodes.CONTAINS_UNCLASSIFIABLE_WORD
                # don't return the result yet, the name is well formed, we just have an unclassified
                # word in the result.

                issues_that_must_be_fixed = [
                    AnalysisIssueCodes.ADD_DISTINCTIVE_WORD,
                    AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD,
                    AnalysisIssueCodes.INCORRECT_YEAR,
                    AnalysisIssueCodes.WORDS_TO_AVOID,
                    AnalysisIssueCodes.TOO_MANY_WORDS
                ]

                issue_must_be_fixed = False
                result_codes = list(map(lambda r: r.result_code, analysis))

                for code in result_codes:
                    if code in issues_that_must_be_fixed:
                        issue_must_be_fixed = True
                        break

                if issue_must_be_fixed:
                    return analysis
                    #  Name is not well formed - do not continue

                # If the WORD_TO_AVOID check failed, the UNCLASSIFIED_WORD check
                # will have failed too because words to avoid are never classified.
                # Strip out the unclassified words errors involving the same name words.
                list_avoid = []

                has_words_to_avoid = self._has_analysis_issue_type(analysis, AnalysisIssueCodes.WORDS_TO_AVOID)
                if has_words_to_avoid:
                    matched_words_to_avoid = \
                        self._get_analysis_issue_type_issues(analysis, AnalysisIssueCodes.WORDS_TO_AVOID)

                    for procedure_result in matched_words_to_avoid:
                        list_avoid = list_avoid + procedure_result.values.get('list_avoid', [])

                    def remove_words_to_avoid(result):
                        if result.result_code == AnalysisIssueCodes.CONTAINS_UNCLASSIFIABLE_WORD:
                            for word in list_avoid:
                                result.values['list_none'].remove(word)
                        return result

                    analysis = list(map(remove_words_to_avoid, analysis))

                analysis_issues_sort_order = [
                    AnalysisIssueCodes.ADD_DISTINCTIVE_WORD,
                    AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD,
                    AnalysisIssueCodes.INCORRECT_YEAR,
                    AnalysisIssueCodes.WORDS_TO_AVOID,
                    AnalysisIssueCodes.TOO_MANY_WORDS,
                    AnalysisIssueCodes.CONTAINS_UNCLASSIFIABLE_WORD,
                    AnalysisIssueCodes.WORD_SPECIAL_USE,
                    AnalysisIssueCodes.NAME_REQUIRES_CONSENT,
                    AnalysisIssueCodes.QUEUE_CONFLICT,
                    AnalysisIssueCodes.CORPORATE_CONFLICT,
                    AnalysisIssueCodes.DESIGNATION_NON_EXISTENT,
                    AnalysisIssueCodes.END_DESIGNATION_MORE_THAN_ONCE,
                    AnalysisIssueCodes.DESIGNATION_MISPLACED,
                    AnalysisIssueCodes.DESIGNATION_MISMATCH,
                    AnalysisIssueCodes.DESIGNATION_REMOVAL
                ]

            analysis = analysis + self.do_analysis()
            if self.skip_search_conflicts:
                analysis.append(check_name_is_well_formed)

            analysis = self.sort_analysis_issues(analysis, analysis_issues_sort_order)

            return analysis

        except Exception as error:
            print('Error executing name analysis: ' + repr(error))
            raise

    def sort_analysis_issues(self, analysis_issues, sort_order):
        sorted_analysis_issues = []

        while True:
            # Lucas - this is just in here for reference while I merge
            # while True and len(sort_order) > 0:
            issue_type = sort_order.pop(0)

            # Serve unclassified words first if there are words that require consent in the name
            matched_issues = self._has_analysis_issue_type(analysis_issues, issue_type)
            if matched_issues:
                consent_issues = self._extract_analysis_issues_by_type(analysis_issues, issue_type)
                sorted_analysis_issues += consent_issues

            if sort_order.__len__() == 0:
                break

        return sorted_analysis_issues

    @classmethod
    def _extract_analysis_issues_by_type(cls, analysis, issue_code):
        word_issue_indexes = []
        word_issues = []
        for idx, issue in enumerate(analysis):
            if issue.result_code == issue_code:
                word_issue_indexes.append(idx)

        for idx in word_issue_indexes:
            issue = analysis.pop(idx)
            word_issues.append(issue)

        return word_issues

    @classmethod
    def _has_analysis_issue_type(cls, analysis, issue_code):
        return cls._get_analysis_issue_type_issues(analysis, issue_code).__len__() > 0

    @classmethod
    def _get_analysis_issue_type_issues(cls, analysis, issue_code):
        issues = list(
            filter(lambda i: i.result_code == issue_code, analysis)
        )

        return issues

    def do_analysis(self):
        """
        This is the main execution call for running name analysis checks.
        do_analysis is an abstract method and must be implemented in extending classes.
        @:return ProcedureResult[]
        """
        raise NotImplementedError('do_analysis must be implemented in extending classes')
