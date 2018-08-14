In PyCharm choos enew prject and selected flask (but then mo).

Copied in flask-admin sample, but complained about SQL Alchemy.

File > Settings; Project: [projectname] > Project Interpreter. Clicked + and installed Flask Admin
File > Settings; Project: [projectname] > Project Interpreter. Clicked + and installed Flask-SQLAlchemy
Also: psycopg2
(The above all done in openshift via the requirements.txt file)

Deploy:
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

#### TODO:
* Config for different environments
* SSO
* Reload cores: auto or button
* Stop words?
* Performance
* NAMEX-API build on commit
* Move templates to better place / do jinja properly
* Where to deploy? Test and push to dev/prod?
* Dev DB reconfiguration and reload
* Documentation on data loading, project, DB schemas
* Alembic for migrating database changes
* gunicorn, or something else
* auditing
