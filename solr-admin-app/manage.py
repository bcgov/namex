"""Manage the database and some other items required to run the API
"""
from flask import current_app
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from solr_admin import create_application
from solr_admin.models import db
from solr_admin import models

app, admin = create_application()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    current_app.logger.debug('Running the Manager')
    manager.run()
