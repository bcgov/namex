from flask_admin.contrib.sqla import ModelView
from flask import request, redirect
from solr_admin.keycloak import Keycloak

class SecuredView(ModelView):

    # At runtime determine whether or not the user has access to functionality of the view.
    def is_accessible(self):
        # Returns true only if the user has a valid token and the right role
        return Keycloak().has_access()

    # At runtime determine what to do if the view is not accessible.
    def inaccessible_callback(self, name, **kwargs):
        # Redirect the browser into Keycloak’s OIDC flow when not logged in
        return redirect(Keycloak().get_redirect_url(request.url))
