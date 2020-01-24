from enum import Enum

# Define service variables

# Modes
MODE_SYNS = 'Syns'
MODE_SUBS = 'Subs'
MODE_STOP = 'Stop'

# Categories
dsg_end = 'Designations_end'
dsg_any = 'Designations_any'
stop_w = 'Stop Words'


class AnalysisResultCodes(Enum):
    VALID_NAME = 'auto_approved'
    ADD_DISTINCTIVE_WORD = 'add_distinctive'
    ADD_DESCRIPTIVE_WORD = 'add_descriptive'
    WORD_TO_AVOID = 'word_to_avoid'
    DESIGNATION_MISMATCH = 'designation_mismatch'
    TOO_MANY_WORDS = 'excess_words'
    NAME_REQUIRES_CONSENT = 'consent_required'
    CONTAINS_UNCLASSIFIABLE_WORD = 'unclassified_word'
    CORPORATE_CONFLICT = 'corp_conflict'
