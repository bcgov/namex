import os

os.environ.setdefault("SOLR_SYNONYMS_API_FLASK_SECRET_KEY", "test-secret")

import pytest
from sqlalchemy import Boolean, Column, Integer, Sequence, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from synonyms import create_app
from synonyms import db as _db  # your SQLAlchemy instance

Base = declarative_base()

class Synonym(Base):
    __tablename__ = "synonym"
    id = Column(Integer, primary_key=True, autoincrement=True)  # <-- autoincrement instead of Sequence
    category = Column(String, nullable=True)
    synonyms_text = Column(String, nullable=False)
    stems_text = Column(String, nullable=False)
    comment = Column(String, nullable=True)
    enabled = Column(Boolean, nullable=True, server_default=text("TRUE"))


@pytest.fixture(scope="session")
def app():
    """Return a session-wide Flask app in testing mode."""
    _app = create_app("testing")
    return _app

@pytest.fixture(scope="function")
def db(app):
    """Create a fresh database schema and Synonym table for each test function."""
    with app.app_context():
        engine = _db.engine  # use your SQLAlchemy instance directly

        # Drop and recreate schema
        with engine.connect() as conn:
            conn.execute(text("DROP SCHEMA public CASCADE;"))
            conn.execute(text("CREATE SCHEMA public;"))
            conn.execute(text("GRANT ALL ON SCHEMA public TO postgres;"))
            conn.execute(text("GRANT ALL ON SCHEMA public TO public;"))
            conn.commit()

        # Create tables directly
        Base.metadata.create_all(bind=engine)

        # Provide the SQLAlchemy session
        Session = sessionmaker(bind=engine)
        session = Session()

        yield session

        session.rollback()
        session.close()
