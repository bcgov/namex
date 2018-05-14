"""Manage the database and some other items required to run the API
"""
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import db, application
from app import models
import logging

migrate = Migrate(application, db)
manager = Manager(application)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    logging.log(logging.INFO, 'Running the Manager')
    manager.run()
