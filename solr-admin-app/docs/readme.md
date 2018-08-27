
In PyCharm choose new project and selected flask (but then mo).

#### Deploy:
* Catalog: Python
* Screen 1
  * Click `Next`
* Screen 2
  * Add to Project: `names examination (dev)`
  * Application Name: `solr-admin`
  * Git Repository: repo
  * Advanced options
    * set context-dir to `solr-admin-app`
    * Routing/Security: Secure route; insecure traffic: Redirect
    * Build Configuration / environment variables
      * SOLR_ADMIN_APP_DATABASE_HOST: postgresql-solr.servicebc-ne-dev.svc
      * (Secret) SOLR_ADMIN_APP_DATABASE_USERNAME: postgresql-solr database-user
      * (Secret) SOLR_ADMIN_APP_DATABASE_PASSWORD: postgresql-solr database-password
      * (Secret) SOLR_ADMIN_APP_DATABASE_NAME: postgresql-solr database-name
      * Also the Keycloak params
    * Create

Set up configmap and reconfigure build (?) to use it.

#### SSO Admin Setup:
Create client "namex-solr-admin" with client protocol openid-connect and Access Type confidential. Add valid
redirect URI "http://localhost:8080/oidc_callback"

#### TODO:
* SHOULD HAVE: Ensure that synonyms do not have embedded spaces
* SHOULD HAVE: Ensure that duplicate values in synonyms are disallowed
* NICE TO HAVE: Inline editing of synonyms alphabetizes but is not displayed properly
* NICE TO HAVE: Determine if there is a way to highlight search matches
* NICE TO HAVE: Inline edit box for synonyms needs to be wider
* SSO authorization based on group
* Display username and add logout button
* Magic stuff for PostgreSQL volumes
* Stop words
* Indexing synonyms - provide sanity checking tools
* Performance
* NAMEX-API build on commit
* Move templates to better place / do jinja properly
* Determine if Alembic should be used for migrating database changes
* Use gunicorn or something else to get rid of WSGI warning
* Turn off debug in openshift
* Handle changes to postgres credentials
* Fix desktop to run on port 8080, not 5000
* Sort out what the Flask SECRET_KEY is used for
* Fix the warning for the dotenv import in config.py (and others)
* Determine if the Keycloak singleton is pythony enough
* Document the local development setup.
* Learn and embrace PEP 8 and 257
* Determine if bootstrap files, etc, should be in repo
* Add version numbers to requirements.txt
* Determine why menu items are sometimes missing on first load
* Remove root URL from Keycloak client
* Can't inline edit booleans (github.com/flask-admin/flask-admin/issues/1604)
* Make route not visible from internet, much like solr is done
* Make the audit action an enum in the model
* Implement test suite
* Export of synonym_audit loses date and time information
* Move the solr core names to somewhere easily configurable

#### DONE:
* Better duplicate error message
* DB Configuration
* Singularize table name
* Sorting warning on create box
* Notice of version for template files plus documentation
* Put into NAMEX
* Redeploy Solr with new config files ("enabled")
* What container? Python
* Config for different environments
* Dev DB reconfiguration and reload
* Documentation on data loading, project, DB schemas
* Where to deploy? Test and push to dev/prod
* SSO authentication
* Dev DB reconfiguration and reload
* Documentation on data loading, project, DB schemas
* Where to deploy? Test and push to dev/prod
* SSO authentication
* Monkeypatch the Verisign G2 root certificate
* Add "category" column to the database, plus searching or filtering
* Auditing
* Insert commas after spaces in the view (data too wide for page)
* Figure out why OIDC redirect is not working for HTTPS
* Reload cores automatically
