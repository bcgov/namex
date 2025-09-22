
import flask_restx

from . import synonyms
from . import name_processing
from . import probes
# from .. import solr-admin-app.solr_admin

__all__ = ["api"]


api = flask_restx.Api(
    version="1.0",
    title="Synonyms API",
    description="Retrieves the sets of synonyms for a given word.",
    prefix="/api/v1",
)

# Remove the default namespace so that it doesn't show up in Swagger.
api.namespaces.clear()

api.add_namespace(probes.api, path="/synonyms/probes")
api.add_namespace(synonyms.api, path="/synonyms")
api.add_namespace(name_processing.api, path="/name-processing")
