import os
import time

import pytest
from selenium import webdriver
from sqlalchemy import engine_from_config
from tests.external.support.driver.server_driver import ServerDriver


@pytest.fixture(scope="session", autouse=True)
def skip_auth():
    """Disable authentication for all tests."""
    os.environ['SKIP_AUTH'] = 'true'
    yield
    os.environ.pop('SKIP_AUTH', None)


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
    options = webdriver.FirefoxOptions()
    options.headless = True
    return webdriver.Firefox(options=options)


def chrome_driver():
    import os
    import platform
    gecko = os.path.join(os.path.dirname(__file__), 'external', 'support', 'chromedriver', 'mac', 'chromedriver')
    if platform.system() == 'Linux':
        gecko = os.path.join(os.path.dirname(__file__), 'external', 'support', 'chromedriver', 'linux', 'chromedriver')
    if platform.system() == 'Windows':
        gecko = os.path.join(os.path.dirname(__file__), 'external', 'support', 'chromedriver', 'windows',
                             'chromedriver.exe')
    return gecko



@pytest.fixture(scope="session")
def browser(server, base_url):
    browser = get_browser()
    browser.get(base_url + '/admin/synonym')
    yield browser
    browser.quit()
    server.shutdown()


@pytest.fixture(scope="session")
def base_url(port):
    return 'http://localhost:' + str(port)


@pytest.fixture(scope="function")
def clean_db():
    from solr_admin import create_application
    from solr_admin import models

    from solr_admin.models.synonym import Synonym
    from solr_admin.models.synonym_audit import SynonymAudit

    from solr_admin.models.restricted_condition import RestrictedCondition
    from solr_admin.models.restricted_word import RestrictedWord
    from solr_admin.models.restricted_word_condition import RestrictedWordCondition

    from solr_admin.models.decision_reason import DecisionReason
    from solr_admin.models.decision_reason_audit import DecisionReasonAudit

    from solr_admin.models.virtual_word_condition import VirtualWordCondition
    from solr_admin.models.restricted_condition_audit import RestrictedConditionAudit

    app, admin = create_application(run_mode='testing')
    db = models.db

    synonyms_db = engine_from_config({'sqlalchemy.url': app.config['SQLALCHEMY_BINDS']['synonyms']})
    # Synonym.metadata.drop_all(bind=synonyms_db)
    # Synonym.metadata.create_all(bind=synonyms_db, tables=[Synonym.metadata.tables['synonym']])
    # SynonymAudit.metadata.create_all(bind=synonyms_db, tables=[SynonymAudit.metadata.tables['synonym_audit']])

    namex_db = engine_from_config({'sqlalchemy.url': app.config['SQLALCHEMY_DATABASE_URI']})
    # RestrictedCondition.metadata.drop_all(bind=namex_db)
    # RestrictedCondition.metadata.create_all(bind=namex_db, tables=[RestrictedCondition.metadata.tables['restricted_condition']])
    # RestrictedWord.metadata.create_all(bind=namex_db, tables=[RestrictedWord.metadata.tables['restricted_word']])
    # RestrictedWordCondition.metadata.create_all(bind=namex_db, tables=[RestrictedWordCondition.metadata.tables['restricted_word_condition']])

    # DecisionReason.metadata.create_all(bind=namex_db, tables=[DecisionReason.metadata.tables['decision_reason']])
    # DecisionReasonAudit.metadata.create_all(bind=namex_db, tables=[DecisionReasonAudit.metadata.tables['decision_reason_audit']])

    # VirtualWordCondition.metadata.create_all(bind=namex_db, tables=[VirtualWordCondition.metadata.tables['virtual_word_condition']])
    # RestrictedConditionAudit.metadata.create_all(bind=namex_db, tables=[RestrictedConditionAudit.metadata.tables['restricted_condition_audit']])

    return db


@pytest.fixture(scope="function")
def db(clean_db):
    yield clean_db
    clean_db.session.close()
