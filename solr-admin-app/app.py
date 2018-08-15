
import solr_admin


# Create the application.
application = solr_admin.create_app()

if __name__ == "__main__":
    application.run(port=8080, debug=True)
