"""Manage the database and some other items required to run the API
"""
from synonyms import create_app
from synonyms.models import db
from flask_migrate import Migrate
import logging

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    logging.info('Running the Manager')
    app.run()