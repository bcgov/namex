
"""Endpoints to check and manage the health of the service."""
from flask import current_app, Blueprint


bp = Blueprint('PROBES', __name__, url_prefix='')  # pylint: disable=invalid-name


# If we are reachable, we consider ourselves to be live.
@bp.get('/liveness')
def liveness():
    return {'message': 'Liveness checks passed'}, 200


# If we are reachable, we consider ourselves to be ready.
@bp.get('/readiness')
def readiness():
    return {'message': 'Readiness checks passed'}, 200
