"""Create and run an instance of this service."""
from synonyms import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
