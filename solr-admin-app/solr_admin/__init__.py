
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

from solr_admin.models.synonym import Synonym
from solr_admin.views.synonym_view import SynonymView


# Create application
app = Flask(__name__)

# Create secret key so we can use sessions.
app.config["SECRET_KEY"] = os.urandom(24)

# Turn this off to get rid of warning messages. In future versions of SQLAlchemy, false will be the default and this
# can be removed.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Get the environment variables that define the database connection.
DB_USER = os.getenv("DATABASE_USER", "")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
DB_HOST = os.getenv("DATABASE_HOST", "")
DB_PORT = os.getenv("DATABASE_PORT", "5432")
DB_NAME = os.getenv("DATABASE_NAME", "")
SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{password}@{host}:{port}/{name}".format(
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    name=DB_NAME,
)

# For testing.
SQLALCHEMY_DATABASE_URI = "postgres://wamoar:postpass@localhost:5432/namex"

# Create the connection to the database.
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)


# Flask views
@app.route("/")
def index():
    return "<a href=\"/admin/synonym\">Click me to get to Synonyms!</a>"


# Create admin
def create_app():
    solr_admin = Admin(app, name="Solr Configuration", template_mode="bootstrap3")
    solr_admin.add_view(SynonymView(Synonym, db.session))

    return app
