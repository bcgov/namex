from flask_restplus import Api

from .requests import api as nr_api
from .ops import api as nr_ops

api = Api(
    title='Name Request API',
    version='1.0',
    description='The Core API for the Names Examination System',
    prefix='/api/v1',
)

api.add_namespace(nr_api, path='/requests')
api.add_namespace(nr_ops, path='/nr-ops')