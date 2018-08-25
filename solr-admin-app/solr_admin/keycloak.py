
import logging
from flask_oidc import OpenIDConnect


# Singleton that allows us to create the OIDC once with the application, but then re-use that OIDC without
# re-instantiating.
class Keycloak(object):
    __oidc = None

    '''
    Initialize the class, but only create the oidc object when it is None (prevent duplicate instantiation) and the
    application is defined (allow import prior to instantiation).
    '''
    def __init__(self, application):
        if not Keycloak.__oidc and application:
            Keycloak.__oidc = OpenIDConnect(application)

    '''
    Determines whether or not the user is authorized to use the application. True if the user is logged in.
    '''
    def has_access(self):
        logged_in = self.__oidc.user_loggedin

        if logged_in:
            logging.info("logged in as %s", self.get_username())

        return logged_in

    '''
    Gets the redirect URL that is used to transfer the browser to the identity provider.
    '''
    def get_redirect_url(self, request_url):
        """

        :rtype: object
        """
        return self.__oidc.redirect_to_auth_server(request_url)

    '''
    Gets the username for the currently logged in user. This will be prefixed with the authentication scheme, such as
    "idir/" or "github/" - no prefix indicates that authentication is performed by the identity provider.
    '''
    def get_username(self):
        return self.__oidc.user_getfield("preferred_username")
