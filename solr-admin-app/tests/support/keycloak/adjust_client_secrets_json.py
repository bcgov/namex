import os
import json
import dotenv
import sys

client_info = ''
client_info_file = os.path.join(os.path.dirname(__file__), 'keycloak_client_info')
with open(client_info_file, 'r') as info_file:
    client_info = info_file.read()

print(client_info)
client_info_json = json.loads(client_info)
secret = client_info_json['credentials']['secret']
print('secret=' + secret)

dotenv.load_dotenv(dotenv.find_dotenv())
secrets_json_file = os.getenv('SOLR_ADMIN_APP_OIDC_CLIENT_SECRETS', 'solr-admin-app/keycloak_client_secrets/secrets.json')
print(secrets_json_file)
assert secrets_json_file is not None

value = {
    "web": {
        "auth_uri": "http://localhost:8081/auth/realms/master/protocol/openid-connect/auth",
        "client_id": "namex-solr-admin-app",
        "client_secret": secret,
        "userinfo_uri": "http://localhost:8081/auth/realms/master/protocol/openid-connect/userinfo",
        "token_uri": "http://localhost:8081/auth/realms/master/protocol/openid-connect/token",
        "token_introspection_uri": "http://localhost:8081/auth/realms/master/protocol/openid-connect/token/introspect"
    }
}
value_as_string = json.dumps(value, indent=2, separators=(',', ': '))
print(value_as_string)

os.makedirs(os.path.dirname(secrets_json_file), exist_ok=True)
with open(secrets_json_file, 'w') as secrets_file:
    secrets_file.write(value_as_string)
