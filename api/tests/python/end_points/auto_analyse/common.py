import pytest
import datetime

from namex.constants import EntityTypes

CORP_CONFLICT_MESSAGE = 'Too similar to an existing name.'
QUEUE_CONFLICT_MESSAGE = 'Too similar to an existing name in the queue.'


@pytest.mark.skip
def assert_issues_count_is(count, issues):
    if issues.__len__() > count:
        print('\n' + 'Issue types:' + '\n')
        for issue in issues:
            print('- ' + issue.issueType.value + '\n')
    assert issues.__len__() == count


@pytest.mark.skip
def assert_issues_count_is_gt(count, issues):
    print('\n' + 'Issue types:' + '\n')
    for issue in issues:
        print('- ' + issue.get('issue_type') + '\n')
    assert issues.__len__() > count


@pytest.mark.skip
def assert_issue_type_is_one_of(types, issue):
    assert issue.get('issue_type') in types


@pytest.mark.skip
def assert_has_issue_type(issue_type, issues):
    has_issue = False
    for issue in issues:
        if issue.get('issue_type') == issue_type.value:
            has_issue = True

    assert has_issue is True


@pytest.mark.skip
def assert_has_no_issue_type(issue_type, issues):
    has_issue = False
    for issue in issues:
        if issue.get('issue_type') == issue_type.value:
            has_issue = True

    assert has_issue is False


@pytest.mark.skip
def assert_has_designations_upper(issue_type, issues):
    has_upper = False
    for issue in issues:
        if issue.get('issue_type') == issue_type.value:
            has_upper = (
                all(designation.isupper() for designation in issue.get('designations'))
                if issue.get('designations')
                else True
            )

    assert has_upper is True


@pytest.mark.skip
def assert_has_word_upper(issue_type, issues):
    has_upper = False
    for issue in issues:
        if issue.get('issue_type') == issue_type.value:
            has_upper = all(name_action.get('word').isupper() for name_action in issue.get('name_actions'))

    assert has_upper is True


@pytest.mark.skip
def assert_correct_conflict(issue_type, issues, expected):
    is_correct = False
    for issue in issues:
        if (
            issue.get('issue_type') == issue_type.value
            and ' '.join(value['name'] for value in issue.get('conflicts')) == expected
        ):
            is_correct = True

    assert is_correct is True


@pytest.mark.skip
def assert_additional_conflict_parameters(issue_type, issues):
    is_correct = False
    for issue in issues:
        if issue.get('issue_type') == issue_type.value and (
            value['id'] and value['start_date'] and value['source'] for value in issue.get('conflicts')
        ):
            is_correct = True

    assert is_correct is True


def assert_conflict_message(issue_type, issues, queue=False):
    is_correct = False
    for issue in issues:
        if queue:
            if issue.get('issue_type') == issue_type.value and (
                value['line1'] == QUEUE_CONFLICT_MESSAGE for value in issue.get('conflicts')
            ):
                is_correct = True
        else:
            if issue.get('issue_type') == issue_type.value and (
                value['line1'] == CORP_CONFLICT_MESSAGE for value in issue.get('conflicts')
            ):
                is_correct = True
    assert is_correct is True


@pytest.mark.skip
def assert_is_number(issue_type, issues):
    is_number = False
    for issue in issues:
        if issue.get('issue_type') == issue_type.value:
            is_number = all(name_action.get('word').isnumeric() for name_action in issue.get('name_actions'))

    assert is_number is True


def save_words_list_classification(words_list):
    from namex.models import WordClassification as WordClassificationDAO

    for record in words_list:
        wc = WordClassificationDAO()
        wc.classification = record['classification']
        wc.word = record['word']
        wc.start_dt = datetime.date.today()
        wc.approved_dt = datetime.date.today()
        wc.save_to_db()


def save_words_list_virtual_word_condition(words_list):
    from namex.models import VirtualWordCondition as VirtualWordConditionDAO

    for record in words_list:
        vwc = VirtualWordConditionDAO()
        vwc.rc_words = record['words']
        vwc.rc_consent_required = record['consent_required']
        vwc.rc_allow_use = record['allow_use']
        vwc.save_to_db()


def save_words_list_name(words_list, queue=False):
    from namex.models import Request as RequestDAO, State, Name as NameDAO

    num = 0
    req = 1460775
    for record in words_list:
        nr_num_label = 'NR 00000'
        num += 1
        req += 1
        nr_num = nr_num_label + str(num)

        nr = RequestDAO()
        nr.nrNum = nr_num
        if queue:
            nr.stateCd = State.DRAFT
            nr.expirationDate = datetime.date.today() + datetime.timedelta(days=1)
        else:
            nr.stateCd = State.APPROVED
        nr.requestId = req
        nr.requestTypeCd = EntityTypes.CORPORATION.value
        nr._source = 'NAMEREQUEST'

        name = NameDAO()
        name.choice = 1
        name.name = record
        name.state = State.APPROVED
        name.corpNum = '0652480'
        nr.names = [name]
        nr.save_to_db()
