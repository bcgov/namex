#! /bin/sh
set -e

COMMAND=${1:-upgrade}
REVISION=${2:-}
echo starting $COMMAND $REVISION
export DEPLOYMENT_ENV=migration
export PYTHONPATH="$(pwd)/src${PYTHONPATH:+:$PYTHONPATH}"
flask db $COMMAND $REVISION
echo "$COMMAND completed"