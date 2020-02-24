import pytest
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from namex.services.synonyms.synonym import SynonymService


def test_get_synonyms(app, db):
    with app.app_context():
        db.init_app(app)  # this is important!
        db.create_all()

        syn_svc = SynonymService()
        result = syn_svc.get_synonyms()
        print(result)
