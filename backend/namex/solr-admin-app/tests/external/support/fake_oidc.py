class FakeOidc:
    user_loggedin = True

    def user_getfield(self, key):
        return 'Joe'

    def user_role(self):
        return

    def has_access(self):
        return True

    def get_access_token(self):
        return 'any'

    def _get_token_info(self, token):
        return {'realm_access': {'roles': 'names_manager'}}

    def get_redirect_url(self, url):
        return '/login'
