import solr_feeder

# Listen on all interfaces, and the catalog Python container expects the application to be on 8080.
application = solr_feeder.create_application()
if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080, debug=True)
