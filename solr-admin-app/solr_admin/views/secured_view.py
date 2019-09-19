from flask_admin.contrib import sqla
from flask import request
from solr_admin import keycloak


class SecuredView(sqla.ModelView):

    def __init__(self, model, session,
                 name=None, category=None, endpoint=None, url=None, static_folder=None,
                 menu_class_name=None, menu_icon_type=None, menu_icon_value=None):
        super().__init__(model, session,
                 name, category, endpoint, url, static_folder,
                 menu_class_name, menu_icon_type, menu_icon_value)
        self.connected = False

    # At runtime determine whether or not the user has access to functionality of the view.
    def is_accessible(self):
        kc = keycloak.Keycloak(None)

        if not kc.is_logged_in():
            self.connected = False
            return False

        return kc.has_access()

    # At runtime determine what to do if the view is not accessible.
    def inaccessible_callback(self, name, **kwargs):
        if not self.connected:
            self.connected = True
            kc = keycloak.Keycloak(None)
            return kc.get_redirect_url(request.url)
        else:
            return 'not authorized'
