# from app import application
from flask_migrate import Migrate

from namex import create_app, db

app = create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run()
