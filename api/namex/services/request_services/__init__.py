from flask import current_app
from namex.models import State, User
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
            current_app.logger.debug('didnt find user, attempting to create new user from the JWT info')
            user = User.create_from_jwtToken(jwt_oidc_token)

        return user
    except Exception as err:
        current_app.logger.error(err.with_traceback(None))
        raise ServicesError('unable_to_get_or_create_user',
                            '{"code": "unable_to_get_or_create_user",'
                            '"description": "Unable to get or create user from the JWT, ABORT"}'
                            )