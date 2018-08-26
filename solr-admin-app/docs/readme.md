
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
    * Routing: path to /admin
    * Routing/Security: Secure route; insecure traffic: Redirect
    * Build Configuration / environment variables
      * SOLR_ADMIN_APP_DATABASE_HOST: postgresql-solr.servicebc-ne-dev.svc
      * (Secret) SOLR_ADMIN_APP_DATABASE_USERNAME: postgresql-solr database-user
      * (Secret) SOLR_ADMIN_APP_DATABASE_PASSWORD: postgresql-solr database-password
      * (Secret) SOLR_ADMIN_APP_DATABASE_NAME: postgresql-solr database-name
    * Create

#### SSO Admin Setup:
Create client "namex-solr-admin" with client protocol openid-connect and Access Type confidential. Add valid
redirect URI "http://localhost:8080/oidc_callback"

#### TODO:
* Monkeypatch the Verisign G2 root certificate
* SSO authorization based on group
* Display username and add logout button
* Add "category" column to the database, plus searching or filtering
* auditing
* Reload cores: auto or button
* Magic stuff for PostgreSQL volumes
* Stop words
* Indexing synonyms - provide sanity checking tools
* Performance
* NAMEX-API build on commit
* Move templates to better place / do jinja properly
* Alembic for migrating database changes?
* gunicorn, or something else?
* changes to postgres credentials
* insert commas after spaces in the view (data too wide for page)
* highlight searches?
* Fix desktop to run on port 8080, not 5000
* Sort out what the Flask SECRET_KEY is used for
* Fix the warning for the dotenv import in config.py
* Is the Keycloak singleton pythony enough?
* Document the local development setup.
* Learn and embrace PEP 8 and 257

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
