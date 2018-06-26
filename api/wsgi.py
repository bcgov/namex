# from app import application
from app import create_app
import sys

application = create_app()

if __name__ == "__main__":
    application.run()
