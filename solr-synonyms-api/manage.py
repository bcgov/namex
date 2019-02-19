"""Manage the database and some other items required to run the API
"""
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from synonyms import create_application
from synonyms.models import db
from synonyms import models
import logging

app = create_application()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    logging.log(logging.INFO, 'Running the Manager')
    manager.run()
