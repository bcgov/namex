
"""Endpoints to check and manage the health of the service."""
from flask import Blueprint


bp = Blueprint('PROBES', __name__, url_prefix='/probes')  # pylint: disable=invalid-name


@bp.get('/liveness')
def liveness():
    """Returns if the api is live."""
    # TODO: test colin / bor / reg-search and namex connections
    return {'message': 'Liveness checks passed'}, 200


@bp.get('/readiness')
def readiness():
    """Returns if the api is ready."""
    return {'message': 'Readiness checks passed'}, 200
