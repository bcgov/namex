
import flask_restplus

from . import synonyms
from . import probes


__all__ = ['api']


api = flask_restplus.Api(
    version='1.0',
    title='Synonyms API',
    description='Retrieves the sets of synonyms for a given word.',
    prefix='/api/v1',
)

# Remove the default namespace so that it doesn't show up in Swagger.
api.namespaces.clear()

api.add_namespace(probes.api, path='/probes')
api.add_namespace(synonyms.api, path='/synonyms')
