#! /bin/sh
echo 'starting upgrade'
export FLASK_ENV=migration
flask db upgrade