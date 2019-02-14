
import logging

import synonyms


# Leave this as DEBUG for now.
logging.basicConfig(level=logging.DEBUG)

# Listen on all interfaces, and the catalog Python container expects the application to be on 8080.
application = synonyms.create_application()
if __name__ == '__main__':
    application.run(host='localhost', port=8081, debug=True)
