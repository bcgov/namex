import os
import pytest
from selenium import webdriver
from tests.support.driver.server_driver import ServerDriver
from sqlalchemy.schema import MetaData, DropConstraint


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


@pytest.fixture(scope="function")
def clean_db():
    from flask_sqlalchemy import SQLAlchemy
    from solr_admin import create_application
    from solr_admin.models.synonym import Synonym
    from solr_admin.models.restricted_condition import RestrictedCondition2
    from solr_admin.models.restricted_word_table import RestrictedWordTable

    app = create_application(run_mode='testing')
    db = SQLAlchemy(app)
    metadata = MetaData(db.engine)
    metadata.reflect()
    for table in metadata.tables.values():
        for fk in table.foreign_keys:
            db.engine.execute(DropConstraint(fk.constraint))
    metadata.drop_all()
    db.drop_all()

    Synonym.metadata.create_all(bind=db.engine)
    RestrictedCondition2.metadata.create_all(bind=db.engine)
    RestrictedWordTable.metadata.create_all(bind=db.engine)

    return db


@pytest.fixture(scope="function")
def db(clean_db):
    yield clean_db
    clean_db.session.close()
