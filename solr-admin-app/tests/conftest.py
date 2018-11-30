import os
import pytest
from selenium import webdriver
from tests.support.driver.server_driver import ServerDriver


@pytest.fixture(scope="session")
def port():
    return 8080


@pytest.fixture(scope="session")
def server(port):
    app = os.path.join(os.path.dirname(__file__), '..', 'app.py')
    server = ServerDriver(name='MyServer', port=port)
    server.start(cmd=['python', app])
    return server


def get_browser():
    import os
    import platform
    gecko = os.path.join(os.path.dirname(__file__), 'support', 'geckodriver', 'mac', 'geckodriver')
    if platform.system() == 'Linux':
        gecko = os.path.join(os.path.dirname(__file__), 'support', 'geckodriver', 'linux', 'geckodriver')
    if platform.system() == 'Windows':
        gecko = os.path.join(os.path.dirname(__file__), 'support', 'geckodriver', 'windows', 'geckodriver.exe')

    return webdriver.Firefox(executable_path=gecko)


@pytest.fixture(scope="session")
def browser(server):
    browser = get_browser()
    yield browser
    browser.quit()
    server.shutdown()


@pytest.fixture(scope="session")
def base_url(port, server):
    return 'http://localhost:' + str(port)


@pytest.fixture()
def db():
    from flask_sqlalchemy import SQLAlchemy
    from solr_admin import create_application
    from solr_admin.models.synonym import Synonym
    from solr_admin.models.restricted_condition import RestrictedCondition2

    app = create_application(run_mode='testing')
    db = SQLAlchemy(app)
    db.engine.execute('drop table if exists ' + Synonym.__tablename__ + ' cascade;')
    db.engine.execute('drop table if exists ' + RestrictedCondition2.__tablename__ + ' cascade;')

    Synonym.metadata.create_all(bind=db.engine)
    RestrictedCondition2.metadata.create_all(bind=db.engine)

    return db
