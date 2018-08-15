In PyCharm choose new project and selected flask (but then mo).


#### Deploy:
* Catalog: Python.
* Screen 1
  * Click `Next`.
* Screen 2
  * Add to Project: `names examination (dev)`.
  * Application Name: `solr-admin`.
  * Git Repository: repo.
  * Advanced options
    * set context-dir to `solr-admin-app`
    * Routing/Security: Secure route; insecure traffic: Redirect
    * Create


#### TODO:
* SSO
* Reload cores: auto or button
* Stop words?
* Performance
* NAMEX-API build on commit
* Move templates to better place / do jinja properly
* Where to deploy? Test and push to dev/prod?
* Dev DB reconfiguration and reload
* Documentation on data loading, project, DB schemas
* Alembic for migrating database changes?
* gunicorn, or something else
* auditing


#### DONE:
* SQLAlchemy secret key
* Better duplicate error message
* DB Configuration
* Singularize table name
* Sorting warning on create box
* Notice of version for template files plus documentation
* Put into NAMEX
* Redeploy Solr with new config files ("enabled")
* What container? Python
* Config for different environments
