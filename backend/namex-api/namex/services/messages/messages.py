from flask import g


class MessageServices(object):
    """Provides services to change the legacy NRO Database
    For ease of use, following the style of a Flask Extension
    """

    CTX_NAMEX_MESSAGES = 'namex_messages'

    ERROR = 'error'
    WARN = 'warn'
    VALID_MSG_TYPES = [ERROR, WARN]

    def __init__(self, app=None):
        """initializer, supports setting the app context on instantiation"""
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """setup for the extension
        :param app: Flask app
        :return: naked
        """
        self.app = app
        app.teardown_appcontext(self._teardown)

    def _teardown(self, exception):
        g.pop('namex_messages')

    @staticmethod
    def _get_msg_stack():
        return g.setdefault('namex_messages', [])

    @staticmethod
    def add_message(msg_type, code, msg):
        """Adds a message as a dict to the stack
        Does not change the logic-flow if an error occurs

        :msg_type: (str) ERROR or WARN are supported message types
        :code: (str) a code that can be used to lookup more on the error
        :msg: (str) human readable message that acts as the default message that could be displayed to a user

        :returns: (bool) True == Success, False == Didn't add message
        """

        if msg_type not in MessageServices.VALID_MSG_TYPES:
            return False

        msgs = MessageServices._get_msg_stack()
        msgs.append({'code': code, 'type': msg_type, 'message': msg})

    @staticmethod
    def get_all_messages():
        return MessageServices._get_msg_stack()
