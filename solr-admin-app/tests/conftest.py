import os
import time

import pytest
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from sqlalchemy import engine_from_config
from tests.external.support.driver.server_driver import ServerDriver


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

    options = Options()
    options.headless = True
    service = Service(executable_path=gecko_driver())
    browser = WebDriver(options=options, service=service)

    return browser


def gecko_driver():
    import os
    import platform
    gecko = os.path.join(os.path.dirname(__file__), 'external', 'support', 'geckodriver', 'mac', 'geckodriver')
    if platform.system() == 'Linux':
        gecko = os.path.join(os.path.dirname(__file__), 'external', 'support', 'geckodriver', 'linux', 'geckodriver')
    if platform.system() == 'Windows':
        gecko = os.path.join(os.path.dirname(__file__), 'external', 'support', 'geckodriver', 'windows', 'geckodriver.exe')
    return gecko


def chrome_driver():
    import os
    import platform
    gecko = os.path.join(os.path.dirname(__file__), 'external', 'support', 'chromedriver', 'mac', 'chromedriver')
    if platform.system() == 'Linux':
        gecko = os.path.join(os.path.dirname(__file__), 'external', 'support', 'chromedriver', 'linux', 'chromedriver')
    if platform.system() == 'Windows':
        gecko = os.path.join(os.path.dirname(__file__), 'external', 'support', 'chromedriver', 'windows', 'chromedriver.exe')
    return gecko


def connect_with(browser, login):
    username = browser.find_element_by_css_selector('input#username')
    password = browser.find_element_by_css_selector('input#password')
    username.clear()
    password.clear()
    username.send_keys(login)
    password.send_keys('WhatEver1')
    button = browser.find_element_by_css_selector('input#kc-login')
    button.submit()
    time.sleep(1)


@pytest.fixture(scope="session")
def browser(server, base_url):
    browser = get_browser()
    browser.get(base_url + '/admin/synonym')
    connect_with(browser, login='names-with-admin-access')
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

    from tests.external.support.fake_oidc import FakeOidc
    from solr_admin.keycloak import Keycloak

    Keycloak._oidc = FakeOidc()
    app, admin = create_application(run_mode='testing')

    # Use the existing db instance that was initialized in create_application
    db = models.db

    synonyms_db = engine_from_config({'sqlalchemy.url': app.config['SQLALCHEMY_BINDS']['synonyms']})
    #Synonym.metadata.drop_all(bind=synonyms_db)
    #Synonym.metadata.create_all(bind=synonyms_db, tables=[Synonym.metadata.tables['synonym']])
    #SynonymAudit.metadata.create_all(bind=synonyms_db, tables=[SynonymAudit.metadata.tables['synonym_audit']])

    namex_db = engine_from_config({'sqlalchemy.url': app.config['SQLALCHEMY_DATABASE_URI']})
    #RestrictedCondition.metadata.drop_all(bind=namex_db)
    #RestrictedCondition.metadata.create_all(bind=namex_db, tables=[RestrictedCondition.metadata.tables['restricted_condition']])
    #RestrictedWord.metadata.create_all(bind=namex_db, tables=[RestrictedWord.metadata.tables['restricted_word']])
    #RestrictedWordCondition.metadata.create_all(bind=namex_db, tables=[RestrictedWordCondition.metadata.tables['restricted_word_condition']])

    #DecisionReason.metadata.create_all(bind=namex_db, tables=[DecisionReason.metadata.tables['decision_reason']])
    #DecisionReasonAudit.metadata.create_all(bind=namex_db, tables=[DecisionReasonAudit.metadata.tables['decision_reason_audit']])

    #VirtualWordCondition.metadata.create_all(bind=namex_db, tables=[VirtualWordCondition.metadata.tables['virtual_word_condition']])
    #RestrictedConditionAudit.metadata.create_all(bind=namex_db, tables=[RestrictedConditionAudit.metadata.tables['restricted_condition_audit']])

    return db


@pytest.fixture(scope="function")
def db(clean_db):
    yield clean_db
    clean_db.session.close()
