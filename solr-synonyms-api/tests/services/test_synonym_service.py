
from flask import current_app

from synonyms.services import SynonymService


def test_get_synonyms(app, db):
    with app.app_context():
        db.init_app(app)  # this is important!
        db.create_all()

        syn_svc = SynonymService()
        result = syn_svc.get_synonyms()
        current_app.logger.debug(result)
