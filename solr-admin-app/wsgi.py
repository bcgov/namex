import logging
import sys
import dotenv

import monkeypatch
from solr_admin import create_application

# Load all the environment variables from a .env file located in the nearest directory above.
dotenv.load_dotenv(dotenv.find_dotenv(), override=True)
# Leave this as DEBUG for now.
logging.basicConfig(level=logging.DEBUG)
# Do the unpleasant but necessary library monkeypatching.
# monkeypatch.patch_ca_certs()

# Listen on all interfaces, and the catalog Python container expects the application to be on 8080.
app, admin = create_application()
if __name__ == '__main__':
    port = '8080'
    if len(sys.argv) > 1:
        port = sys.argv[1]
    app.run(host='0.0.0.0', port=int(port), debug=True)