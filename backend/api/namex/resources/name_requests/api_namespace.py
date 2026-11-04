from flask_cors import cross_origin
from flask_restx import Namespace

# Register a local namespace for the NR reserve
api = Namespace(
    'Name Request',
    description='Public-facing API for name request creation, search, retrieval, and report generation',
    decorators=[cross_origin()],
)
