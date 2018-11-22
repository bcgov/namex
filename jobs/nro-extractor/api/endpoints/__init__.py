from flask_restplus import Api

from .requests import api as nro_ext_api
from .ops import api as nro_ext_ops

api = Api(
    title='NRO Extract API',
    version='1.0',
    description='Extracts a NR from the legacy system and instantiates it in NAMEX',
    prefix='/api/v1',
)

api.add_namespace(nro_ext_api, path='/nro-extract')
api.add_namespace(nro_ext_ops, path='/nro-extract-ops')
