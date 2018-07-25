"""Manage the database and some other items required to run the API
"""
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from namex import create_app
from namex.models import db
from namex import models
import logging

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    logging.log(logging.INFO, 'Running the Manager')
    manager.run()
