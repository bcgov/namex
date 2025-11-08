
from flask import current_app

from synonyms.models.synonym import Synonym
from synonyms.services import SynonymService


def test_get_synonyms(app, db):
    with app.app_context():
        foo_synonym = Synonym(
            category="test",
            synonyms_text="foo",  # matches the search
            stems_text="foo_stem",
            comment=None,
            enabled=True
        )
        db.add(foo_synonym)
        db.commit()

        result = SynonymService().get_synonyms("foo")
        assert set(result) == {'foo', 'foo_stem'}
