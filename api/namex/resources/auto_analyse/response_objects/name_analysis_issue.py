from . import Serializable


class NameAnalysisIssue(Serializable):
    def __init__(self, **kwargs):
        self.line1 = kwargs['line1'] if kwargs.get('line1') else None
        self.line2 = kwargs['line2'] if kwargs.get('line2') else None
        self.consentingBody = kwargs['consentingBody'] if kwargs.get('consentingBody') else None  # None <ConsentingBody>[]
        self.designations = kwargs['designations'] if kwargs.get('designations') else None  # <string>[] | None
        # [add_descriptive | word_to_avoid | excess_words | consent_required | unclassified_word]
        self.issueType = kwargs['issueType'] if kwargs.get('issueType') else None  # <string> | None
        # TODO: Remove word and wordIndex and descriptiveWords
        # self.word = kwargs['word'] if kwargs.get('word') else None  # <string> | None
        # self.wordIndex = kwargs['wordIndex'] if kwargs.get('wordIndex') else None  # <integer> | None
        # self.descriptiveWords = kwargs['descriptiveWords'] if kwargs.get('descriptiveWords') else None  # <DescriptiveWord>[]
        self.showReserveButton = kwargs['showReserveButton'] if kwargs.get('showReserveButton') else False  # <boolean>
        self.showExaminationButton = kwargs['showExaminationButton'] if kwargs.get('showExaminationButton') else False  # <boolean>
        self.conflicts = kwargs['conflicts'] if kwargs.get('conflicts') else None  # <Conflict>[] | None
        # TODO: Get rid of options
        self.setup = kwargs['setup'] if kwargs.get('setup') else None
        # options: number, header: text, text1: text, text2: text, checkbox: obj, button: obj
        # self.options = kwargs['options'] if kwargs.get('options') else None  # TODO: What is this shape?
        self.nameActions = kwargs['nameActions'] if kwargs.get('nameActions') else None  # <NameAction>[] | None
