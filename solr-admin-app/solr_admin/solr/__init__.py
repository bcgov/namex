
import logging
import os
import re
from requests_futures.sessions import FuturesSession


SOLR_CORE_NAMES = ["names", "possible.conflicts", "trademarks"]
SOLR_ADMIN_APP_SOLR_INSTANCE = os.getenv("SOLR_ADMIN_APP_SOLR_INSTANCE", "http://localhost:8393/solr")
SOLR_RELOAD_URL = SOLR_ADMIN_APP_SOLR_INSTANCE + "/admin/cores?action=RELOAD&core={}&wt=json"


# Reload all the cores.
def reload_solr_cores():
    for core_name in SOLR_CORE_NAMES:
        FuturesSession().get(SOLR_RELOAD_URL.format(core_name), background_callback=core_reload_callback)


# Called when the core finishes reloading.
def core_reload_callback(session, response):
    # Try to display just the core name, but if it fails then use the URL.
    match = re.search("core=(.+?)&wt", response.url)
    if match:
        core_name = match.group(1)
    else:
        core_name = response.url

    query_time = response.json()["responseHeader"]["QTime"]

    # Provide some debugging info on how long it takes for a core reload.
    logging.debug("Reloaded %s in %sms", core_name, query_time)
