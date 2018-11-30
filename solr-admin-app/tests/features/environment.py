from tests import conftest


def before_all(context):
    context.db = conftest.db()
    context.server_port = conftest.port()
    context.server = conftest.server(conftest.port())
    context.base_url = conftest.base_url(context.server_port, context.server)
    context.browser = conftest.get_browser()


def after_all(context):
    context.browser.quit()
    context.server.shutdown()
