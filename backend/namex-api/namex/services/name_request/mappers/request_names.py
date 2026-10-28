from flask import current_app

from namex.constants import NameState
from namex.models import DecisionReason, Name, State
from namex.services.name_request.exceptions import MapRequestNamesError
from namex.utils.common import convert_to_ascii

# from namex.services.virtual_word_condition.virtual_word_condition import VirtualWordConditionService
# virtual_wc_svc = VirtualWordConditionService()


def map_submitted_name(submitted_name: Name, request_name: dict, **kwargs):
    """
    Used internally by map_request_names.
    :param submitted_name: Name
    :param request_name: dict
    :key nr_id: int
    :key new_state_code: str
    :key request_entity: str
    :key request_action: str
    :return:
    """
    nr_id = kwargs.get('nr_id')
    new_state_code = kwargs.get('new_state_code')
    request_entity = kwargs.get('request_entity')
    request_action = kwargs.get('request_action')

    # Common name attributes
    submitted_name = _map_submitted_name_attrs(submitted_name, request_name, nr_id=nr_id, new_state_code=new_state_code)
    test_conflict = request_name.get('conflict1')
    if len(test_conflict) > 0:
        conflict_flag = 'Y'
    else:
        conflict_flag = 'N'

    if new_state_code in [State.COND_RESERVE] and conflict_flag == 'Y':
        submitted_name = _map_submitted_name_conflicts(submitted_name, request_name)

    consent_words_list = request_name.get('consent_words', None)
    if consent_words_list and len(consent_words_list) > 0:
        submitted_name = _map_submitted_name_consent_words(submitted_name, consent_words_list)

    # Add macros for specific entities and actions
    if new_state_code in [State.COND_RESERVE, State.RESERVED]:
        macro_list = []
        if request_action == 'MVE' and request_entity != 'UL':
            macro_list.append('Continuation')
        if request_action == 'MVE' and request_entity == 'UL':
            macro_list.append('Ulc Cont In')
        if len(macro_list) > 0:
            submitted_name = _map_submitted_name_macros(submitted_name, macro_list)

    return submitted_name


def _map_submitted_name_attrs(submitted_name: Name, request_name: dict, **kwargs):
    """
    Used internally by map_submitted_name.
    :param submitted_name: Name
    :param request_name: dict
    :key nr_id: int
    :key new_state_code: str
    :return:
    """
    nr_id = kwargs.get('nr_id')
    new_state_code = kwargs.get('new_state_code')

    try:
        submitted_name.nrId = nr_id
        submitted_name.choice = request_name.get('choice', 1)
        submitted_name.name_type_cd = request_name.get('name_type_cd', 'CO')
        submitted_name.name = convert_to_ascii(request_name.get('name', ''))
        submitted_name.designation = request_name.get('designation', '')
        # For existing businesses
        if isinstance(request_name.get('corpNum'), str):
            # To clear the corpNum use an empty string in the data payload
            submitted_name.corpNum = convert_to_ascii(request_name.get('corpNum'))

        if new_state_code == State.DRAFT:
            submitted_name.state = NameState.NOT_EXAMINED.value

        elif new_state_code == State.COND_RESERVE:
            submitted_name.state = NameState.COND_RESERVE.value

        elif new_state_code == State.RESERVED:
            submitted_name.state = NameState.RESERVED.value

        elif new_state_code == State.CONDITIONAL:
            submitted_name.state = NameState.CONDITION.value

        elif new_state_code == State.APPROVED:
            submitted_name.state = NameState.APPROVED.value

    except Exception as err:
        raise MapRequestNamesError(err, 'Error setting common name attributes.')

    return submitted_name


def _map_submitted_name_conflicts(submitted_name: Name, request_name: dict):
    """
    Used internally by map_submitted_name.
    :param submitted_name: Name
    :param request_name: dict
    :return:
    """
    try:
        # Only capturing one conflict
        if request_name.get('conflict1_num'):
            submitted_name.conflict1_num = request_name.get('conflict1_num')
        if request_name.get('conflict1'):
            submitted_name.conflict1 = request_name.get('conflict1')
        # Conflict text same as Namex
        submitted_name.decision_text = 'Consent is required from ' + request_name.get('conflict1') + '\n' + '\n'
    except Exception as err:
        raise MapRequestNamesError(err, 'Error on reserved conflict info.')

    return submitted_name


def _map_submitted_name_macros(submitted_name: Name, macro_list: list):
    """
    Used internally by map_submitted_name.
    :param submitted_name: Name
    :param macro_list: list
    :return:
    """
    for macro in macro_list:
        try:
            macro_text = None
            if macro != '' or len(macro) > 0:
                macro_text = DecisionReason.find_by_name(macro)
        except Exception as err:
            current_app.logger.error('Error on get decision reason word. Macro Word[0]', err)
            raise MapRequestNamesError('Error mapping macro words.')

        try:
            if submitted_name.decision_text is None:
                submitted_name.decision_text = macro + '- ' + macro_text.reason + '\n' + '\n'
            else:
                submitted_name.decision_text += macro + '- ' + macro_text.reason + '\n' + '\n'

        except Exception as err:
            raise MapRequestNamesError(err, 'Error adding macro words to decision.')

    return submitted_name


def _map_submitted_name_consent_words(submitted_name: Name, consent_list: list):
    """
    Used internally by map_submitted_name.
    :param submitted_name: Name
    :param consent_list: list
    :return:
    """
    decision_text = submitted_name.decision_text
    for consent in consent_list:
        try:
            cnd_instructions = None
            if consent != '' or len(consent) > 0:
                # cnd_instructions = virtual_wc_svc.get_word_condition_instructions(consent)
                pass
        except Exception as err:
            current_app.logger.error('Error on get consent word. Consent Word[0]', err)
            raise MapRequestNamesError('Error mapping consent words.')

        try:
            if decision_text is None:
                decision_text = consent + '- ' + cnd_instructions + '\n' + '\n'
            else:
                decision_text += consent + '- ' + cnd_instructions + '\n' + '\n'

            submitted_name.decision_text = decision_text
        except Exception as err:
            raise MapRequestNamesError(err, 'Error adding consent words to decision.')

    return submitted_name
