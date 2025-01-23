
import logging

import solr_feeder


# Leave this as DEBUG for now.
format='%(asctime)s - %(name)s - %(levelname)s in %(module)s:%(filename)s:%(lineno)d - %(funcName)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=format)

# Listen on all interfaces, and the catalog Python container expects the application to be on 8080.
app = solr_feeder.create_application()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
