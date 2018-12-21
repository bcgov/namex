from flask_restplus import Api

from .requests import api as nr_api
from .ops import api as nr_ops
from .document_analysis import api as analysis_api
from .meta import api as meta_api
from .exact_match import api as exact_match_api
from .histories import api as histories_api

# This will add the Authorize button to the swagger docs
# TODO oauth2 & openid may not yet be supported by restplus <- check on this
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    title='Name Request API',
    version='1.0',
    description='The Core API for the Names Examination System',
    prefix='/api/v1',
    security=['apikey'],
    authorizations=authorizations)

api.add_namespace(nr_api, path='/requests')
api.add_namespace(nr_ops, path='/nr-ops')
api.add_namespace(analysis_api, path='/documents')
api.add_namespace(meta_api, path='/meta')
api.add_namespace(exact_match_api, path='/exact-match')
api.add_namespace(histories_api, path='/histories')
