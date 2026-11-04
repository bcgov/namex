
# Solr Admin App

This Flask-Admin application allows viewing and editing the Solr synonyms that are stored in a PostgreSQL table. In the
'testing' environment the synonyms are editable, but in all other environments they are read-only. The synonyms audit
data is read-only in all environments. 

##### SSO Admin Setup:

Create client "namex-solr-admin-app" with a Client Protocol of `openid-connect` and Access Type `confidential`. For the
development environment only, add an additional Valid Redirect URI of `http://localhost:8080/oidc_callback` for doing
desktop development.

##### User Interface Defects
1. Export of synonym_audit loses date and time information
1. Edit page should use a text area for large varchar strings
1. Inline edit box for synonyms needs to be larger
1. Inline editing of synonyms alphabetizes but is not displayed properly
1. Determine why menu items are sometimes missing on first load
1. Can't inline edit booleans (github.com/flask-admin/flask-admin/issues/1604)
1. If you're on page 2 when less than 1000 items, switching to 1000 per page fails

##### Deficiencies - Application
1. Push data from test to dev and prod
1. Make the Category column non-null after all rows have values defined 
1. SSO authorization based on group
1. Display username and add logout button
1. Add DB-based Stop Words to Solr
1. Determine if there is a way to highlight search matches
1. Configure logging

##### Deficiencies - Code
1. Add version numbers to requirements.txt
1. Globals: explore use of `__all__`
1. Determine if bootstrap files, etc, should be in repo
1. Document the local development setup
1. Determine if the Keycloak singleton is pythonic enough
1. Fix the warning for the dotenv import in config.py
1. Move templates to better place / do jinja properly
1. Fix desktop to run on port 8080, not 5000
1. Use gunicorn or something else to get rid of WSGI warning
1. Make the audit action an enum in the model
1. Implement test suite
1. Move the Solr core names to somewhere easily configurable
1. Add error reporting for Solr core reloading
1. Don't reload Solr cores if only the category or comment change

##### Deficiencies - OpenShift
1. Make route not visible from internet, much like solr is done
1. Automate build of image for latest
1. Magic stuff for PostgreSQL volumes
1. Turn off debug in OpenShift
1. Handle changes to PostgreSQL credentials
1. Add health checks
