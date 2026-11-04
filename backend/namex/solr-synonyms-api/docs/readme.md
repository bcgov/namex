
# Solr Synonyms API

This web service provides a ReST API to the synonyms used by Solr. The initial functionality is limited to querying a
term to determine what synonym lists it appears in.

#### Flask Secret Key

This application requires a Flask `SECRET_KEY` to do secure cookie hashing. Never commit keys to the repository, and
never use a key in more than one namespace. The application deployment will read the key from an OpenShift secret. In a
Python console:

```
>>> import os, binascii

>>> binascii.hexlify(os.urandom(24))
b'[big_long_key_in_hex]'
```

Copy the `big_long_key_in_hex` and create a secret in OpenShift (make sure you're in the right project):

```
C:\> oc create secret generic solr-synonyms-api --from-literal=flask-secret-key=[big_long_key_in_hex]
```

#### Deficiencies - Code

1. Authorization is missing, but it's currently a read-only web service
1. Configure proper logging
1. Set the host in app.py to 0.0.0.0 but link in PyCharm doesn't work (use localhost)
1. Add version numbers to requirements.txt
1. Fix the warning for the dotenv import in config.py
1. Fix desktop to run on port 8080, not 5000
