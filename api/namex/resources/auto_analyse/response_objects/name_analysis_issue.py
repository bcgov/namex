from . import Serializable


class NameAnalysisIssue(Serializable):
    def __init__(self, **kwargs):
        self.consentingBody = kwargs['consentingBody'] if kwargs.get('') else None  # None <ConsentingBody>[]
        self.designations = kwargs['designations'] if kwargs.get('designations') else None  # <string>[] | None
        self.descriptiveWords = kwargs['descriptiveWords'] if kwargs.get('descriptiveWords') else None  # <DescriptiveWord>[]
        # [add_descriptive | word_to_avoid | excess_words | consent_required | unclassified_word]
        self.issueType = kwargs['issueType'] if kwargs.get('issueType') else None  # <string> | None
        self.word = kwargs['word'] if kwargs.get('word') else None  # <string> | None
        self.wordIndex = kwargs['wordIndex'] if kwargs.get('wordIndex') else None  # <integer> | None
        self.showExaminationButton = kwargs['showExaminationButton'] if kwargs.get('showExaminationButton') else False  # <boolean>
        self.conflicts = kwargs['conflicts'] if kwargs.get('conflicts') else None  # <Conflict>[] | None
        self.options = kwargs['options'] if kwargs.get('options') else None  # TODO: What is this shape?
        self.nameActions = kwargs['nameActions'] if kwargs.get('nameActions') else None  # <NameAction>[] | None
