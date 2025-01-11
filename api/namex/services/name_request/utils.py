import re
from flask import current_app

from namex import jwt
from namex.constants import PaymentState, request_type_mapping, reverse_request_type_mapping
from namex.models import State, User
from namex.services.exceptions import ServicesError

from .exceptions import MapRequestTypeError


nr_regex = r'^(NR\ ?L{0,1}|L{0,1})?([\d]{6,8})$'


def normalize_nr_num(nr_num_str):
    matches = re.findall(nr_regex, nr_num_str, flags=re.IGNORECASE)
    # If there's a match and the match has a second capturing group (valid NR digits) then proceed
    if len(matches) == 1 and matches[0][1]:
        # Get the first capturing group if it exists, convert to upper case, and remove any spaces
        nr_type = str(matches[0][0]).upper().replace(' ', '') if matches[0][
            0] else 'NR'  # Default to NR if not supplied
        # Grab the NR digits from the second capturing group
        digits = matches[0][1]

        if nr_type == 'NR':
            return 'NR ' + digits
        if nr_type in ['NRL', 'L']:
            return 'NR L' + digits

    return None


def is_temp_nr_num(nr_num_str):
    matches = re.findall(nr_regex, nr_num_str, flags=re.IGNORECASE)
    # If there's a match and the match has a second capturing group (valid NR digits) then proceed
    if len(matches) == 1 and matches[0][1]:
        # Get the first capturing group if it exists, convert to upper case, and remove any spaces
        nr_type = str(matches[0][0]).upper().replace(' ', '') if matches[0][
            0] else 'NR'  # Default to NR if not supplied

        if nr_type in ['NRL', 'L']:
            return True

    return False


def has_active_payment(nr, payment_id=None):
    payments = nr.payments.all()
    if payments and payment_id:
        return len(list(filter(lambda p: p.id == payment_id, payments))) > 0
    elif payments:
        return len(list(filter(lambda p: p.payment_status_code == PaymentState.CREATED.value, payments))) > 0


def has_complete_payment(nr, payment_id=None):
    payments = nr.payments.all()
    if payments and payment_id:
        return len(list(filter(lambda p: p.id == payment_id, payments))) > 0
    elif payments:
        return len(list(filter(
            lambda p: p.payment_status_code in [PaymentState.COMPLETED.value, PaymentState.APPROVED.value], payments
        ))) > 0


def has_completed_or_refunded_payment(nr, payment_id=None):
    payments = nr.payments.all()
    if payments and payment_id:
        return len(list(filter(lambda p: p.id == payment_id, payments))) > 0
    elif payments:
        return len(list(filter(
            lambda p: p.payment_status_code in [
                PaymentState.COMPLETED.value,
                PaymentState.APPROVED.value,
                PaymentState.REFUND_REQUESTED.value,
                PaymentState.CANCELLED.value
            ], payments
        ))) > 0


def get_active_payment(nr, payment_id):
    payments = nr.payments.all()
    if payments:
        payments = list(filter(lambda p: p.id == payment_id, nr.payments.all()))
        return payments[0] if len(payments) > 0 else None
    return None


def get_mapped_request_type(entity_type, request_action):
    output = None
    for item in request_type_mapping:
        if item[1] == entity_type and item[2] == request_action:
            output = item
            break

    if output:
        request_mapping = list(output)
        return request_mapping


def get_mapped_entity_and_action_code(request_type):
    output = None

    for item in reverse_request_type_mapping:
        if item[0] == request_type:
            output = item
            break

    if output:
        entity_type = output[1]
        request_action = output[2]
        return entity_type, request_action
    else:
        raise MapRequestTypeError(message='Error mapping the requestTypeCd to an entity type and action - no default was found in the request type mappings!')


# TODO: Move these out into auth utils in the main utils module
def check_ownership(nrd, user):
    if nrd.stateCd == State.INPROGRESS and nrd.userId == user.id:
        return True
    return False


def get_or_create_user_by_jwt(jwt_oidc_token):
    # GET existing or CREATE new user based on the JWT info
    try:
        user = User.find_by_jwtToken(jwt_oidc_token)
        current_app.logger.debug('finding user: {}'.format(jwt_oidc_token))
        if not user:
            current_app.logger.debug(
                'didnt find user, attempting to create new user from the JWT info:{}'.format(jwt_oidc_token))
            user = User.create_from_jwtToken(jwt_oidc_token)

        return user
    except Exception as err:
        current_app.logger.error(err.with_traceback(None))
        raise ServicesError('unable_to_get_or_create_user',
                            '{"code": "unable_to_get_or_create_user",'
                            '"description": "Unable to get or create user from the JWT, ABORT"}'
                            )


def valid_state_transition(user, nr, new_state):
    """

    :param user:
    :param nr:
    :param new_state:
    :return: (bool)
    """
    # when the legacy user just created a new NR from legacy side, the user should be allowed to
    # modify and cancel it from the legacy side (while the NR still in DRAFT state).
    current_app.logger.debug('stateCd: {}'.format(nr.stateCd))
    current_app.logger.debug('new_state: {}'.format(new_state))
    current_app.logger.debug(f"inside valid_state_transition")
    if (nr.stateCd == State.DRAFT or nr.stateCd == State.APPROVED  or nr.stateCd == State.CANCELLED)   \
        and (new_state == State.DRAFT or new_state == State.CANCELLED):
        current_app.logger.debug(f"inside valid_state_transition true")
        return True
    current_app.logger.debug(f"inside valid_state_transition continue")
    if (new_state in (State.APPROVED,
                      State.REJECTED,
                      State.CONDITIONAL)) \
            and not jwt.validate_roles([User.APPROVER]):
        return False

    # allow any type of user to CANCEL an NR
    if new_state == State.CANCELLED and nr.stateCd in State.CANCELLABLE_STATES:
        return True

    # NR is in a final state, but maybe the user wants to pull it back for corrections
    if new_state == State.CONSUMED:
        return nr.stateCd == State.APPROVED or (nr.stateCd == State.CONDITIONAL and (nr.consentFlag in ('R', 'N')))
    elif nr.stateCd in State.COMPLETED_STATE:
        if not jwt.validate_roles([User.APPROVER]) and not jwt.validate_roles([User.EDITOR]):
            return False
            # return jsonify({"message": "Only Names Examiners can alter completed Requests"}), 401

        # TODO what are the business rules about editing a finalized name
        # if nr.furnished == Request.REQUEST_FURNISHED:
        # return jsonify({"message": "Request has already been furnished and cannot be altered"}), 409

        # A completed Request can only be moved to editable (INPROGRESS)
        # OR remain in its current state (editing a closed request)
        if new_state != State.INPROGRESS and new_state != nr.stateCd:
            return False

    elif new_state in State.RELEASE_STATES:
        if nr.userId != user.id or nr.stateCd != State.INPROGRESS:
            return False
    elif nr.stateCd == State.INPROGRESS:
        if nr.userId != user.id:
            return False

    return True


def get_item_from_list(items, item_id, item_prop='id'):
    """
    :param items:
    :param item_id:
    :param item_prop:
    :return:
    """
    matches = [i for i in items if i.__getattribute__(item_prop) == item_id]
    if len(matches) == 0:
        return None
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise Exception('More than one match found for a given ID!')
