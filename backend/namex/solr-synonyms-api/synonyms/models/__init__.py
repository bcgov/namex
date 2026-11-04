
import flask_sqlalchemy


# Provides the database connection to anything in the package that needs it.
db = flask_sqlalchemy.SQLAlchemy()
from flask_marshmallow import Marshmallow

ma = Marshmallow()
