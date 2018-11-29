import pytest
from selenium import webdriver
from tests.support.driver.server_driver import ServerDriver


@pytest.fixture(scope="session")
def port():
    return 8080


@pytest.fixture(scope="session")
def server(port):
    server = ServerDriver(name='MyServer', port=port)
    server.start(cmd=['gunicorn', 'app', '-w', '1', '-b', '0.0.0.0:{0}'.format(port)])
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


@pytest.fixture(scope="session")
def db():
    from flask_sqlalchemy import SQLAlchemy
    from solr_admin import create_application
    app = create_application(run_mode='testing')
    db = SQLAlchemy(app)
    sqls = [
        'DROP TABLE IF EXISTS public.synonym CASCADE;',
        'DROP SEQUENCE IF EXISTS public.synonym_id_seq;',
        'CREATE SEQUENCE public.synonym_id_seq;',
        """
        CREATE TABLE public.synonym
        (
            id integer NOT NULL DEFAULT nextval('synonym_id_seq'::regclass),
            category character varying(100) COLLATE pg_catalog."default" DEFAULT ''::character varying,
            synonyms_text character varying(1000) COLLATE pg_catalog."default",
            comment character varying(1000) COLLATE pg_catalog."default" DEFAULT ''::character varying,
            enabled boolean DEFAULT true,
            CONSTRAINT synonym_pkey PRIMARY KEY (id),
            CONSTRAINT synonyms_text_unique UNIQUE (synonyms_text),
            CONSTRAINT synonyms_text_not_null CHECK (synonyms_text IS NOT NULL) NOT VALID
        )
        """
    ]
    for sql in sqls:
        db.engine.execute(sql)

    return db
