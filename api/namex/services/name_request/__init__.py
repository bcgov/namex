from flask import current_app, jsonify
from namex import jwt
from namex.models import State, User, Request
from namex.services import ServicesError


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
            current_app.logger.debug('didnt find user, attempting to create new user from the JWT info:{}'.format(jwt_oidc_token))
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
    if (new_state in (State.APPROVED,
                      State.REJECTED,
                      State.CONDITIONAL)) \
            and not jwt.validate_roles([User.APPROVER]):
        return False

    # allow any type of user to CANCEL an NR
    if new_state == State.CANCELLED and nr.stateCd in State.CANCELLABLE_STATES:
        return True

    # NR is in a final state, but maybe the user wants to pull it back for corrections
    if nr.stateCd in State.COMPLETED_STATE:
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
    return True


def convert_to_ascii(value):
    try:
        return value.encode("ascii","ignore").decode('ascii')
    except:
        return value