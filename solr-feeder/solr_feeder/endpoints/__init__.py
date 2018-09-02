
import flask_restplus

from . import feeds
from . import probes


__all__ = ['api']


api = flask_restplus.Api(
    version='1.0',
    title='Solr Feeder API',
    description='Feeds changes from legacy databases into Solr cores. Also provides liveness and readiness probes to '
                'be used for operations.',
    prefix='/api/v1',
)

# Remove the default namespace so that it doesn't show up in Swagger.
api.namespaces.clear()

api.add_namespace(feeds.api, path='/feeds')
api.add_namespace(probes.api, path='/probes')
