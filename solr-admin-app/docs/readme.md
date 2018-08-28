
#### SSO Admin Setup:

Create client "namex-solr-admin" with client protocol openid-connect and Access Type confidential. Add valid
redirect URI "http://localhost:8080/oidc_callback" for desktop development.

#### TODO:
* NICE TO HAVE: Inline editing of synonyms alphabetizes but is not displayed properly
* NICE TO HAVE: Determine if there is a way to highlight search matches
* NICE TO HAVE: Inline edit box for synonyms needs to be wider
* Automate build of image for latest
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
* Add error reporting for Solr core reloading
* Don't reload solr cores if only the category or comment change
* Edit page should use a text area for large varchar strings
* If you're on page 2 when less than 100 items, switch to 1000 per page fails
* SynonymView has commented out code for embedded spaces - remove if not needed

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
* Ensure that singleton values in synonyms are disallowed
* Ensure that synonyms do not have embedded spaces
* Ensure that duplicate values in synonyms are disallowed
