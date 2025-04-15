
# The httplib2 library used by Flask-OIDC uses its own root CA list, and the list does not include the certificate we
# need for the Red Hat SSO servers. The library also does not currently provide a way of changing the root CA list,
# although this functionality may be coming. In the meantime check to see if the certificate is in the list, and if not
# then add it. Ensure that when doing local development that the file is not repeatedly patched.
#
# This is fragile and not pretty.

from flask import current_app
from os import path

import httplib2
import pathlib


_CA_CERTS_FILE = 'cacerts.txt'

_CERTIFICATE = '''
# Issuer: CN=Entrust Root Certification Authority - G2 O=Entrust.net OU=(c) 2009 Entrust, Inc. - for authorized use \
only/See www.entrust.net/legal-terms
# Subject: CN=Entrust Root Certification Authority - G2 O=Entrust.net OU=(c) 2009 Entrust, Inc. - for authorized use \
only/See www.entrust.net/legal-terms
# Serial: 4a:53:8c:28
# SHA1 Fingerprint: 8c:f4:27:fd:79:0c:3a:d1:66:06:8d:e8:1e:57:ef:bb:93:22:72:d4
# Added by the solr-admin-app as a monkeypatch for the identity provider's root cert.
-----BEGIN CERTIFICATE-----
MIIEPjCCAyagAwIBAgIESlOMKDANBgkqhkiG9w0BAQsFADCBvjELMAkGA1UEBhMC
VVMxFjAUBgNVBAoTDUVudHJ1c3QsIEluYy4xKDAmBgNVBAsTH1NlZSB3d3cuZW50
cnVzdC5uZXQvbGVnYWwtdGVybXMxOTA3BgNVBAsTMChjKSAyMDA5IEVudHJ1c3Qs
IEluYy4gLSBmb3IgYXV0aG9yaXplZCB1c2Ugb25seTEyMDAGA1UEAxMpRW50cnVz
dCBSb290IENlcnRpZmljYXRpb24gQXV0aG9yaXR5IC0gRzIwHhcNMDkwNzA3MTcy
NTU0WhcNMzAxMjA3MTc1NTU0WjCBvjELMAkGA1UEBhMCVVMxFjAUBgNVBAoTDUVu
dHJ1c3QsIEluYy4xKDAmBgNVBAsTH1NlZSB3d3cuZW50cnVzdC5uZXQvbGVnYWwt
dGVybXMxOTA3BgNVBAsTMChjKSAyMDA5IEVudHJ1c3QsIEluYy4gLSBmb3IgYXV0
aG9yaXplZCB1c2Ugb25seTEyMDAGA1UEAxMpRW50cnVzdCBSb290IENlcnRpZmlj
YXRpb24gQXV0aG9yaXR5IC0gRzIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEK
AoIBAQC6hLZy254Ma+KZ6TABp3bqMriVQRrJ2mFOWHLP/vaCeb9zYQYKpSfYs1/T
RU4cctZOMvJyig/3gxnQaoCAAEUesMfnmr8SVycco2gvCoe9amsOXmXzHHfV1IWN
cCG0szLni6LVhjkCsbjSR87kyUnEO6fe+1R9V77w6G7CebI6C1XiUJgWMhNcL3hW
wcKUs/Ja5CeanyTXxuzQmyWC48zCxEXFjJd6BmsqEZ+pCm5IO2/b1BEZQvePB7/1
U1+cPvQXLOZprE4yTGJ36rfo5bs0vBmLrpxR57d+tVOxMyLlbc9wPBr64ptntoP0
jaWvYkxN4FisZDQSA/i2jZRjJKRxAgMBAAGjQjBAMA4GA1UdDwEB/wQEAwIBBjAP
BgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBRqciZ60B7vfec7aVHUbI2fkBJmqzAN
BgkqhkiG9w0BAQsFAAOCAQEAeZ8dlsa2eT8ijYfThwMEYGprmi5ZiXMRrEPR9RP/
jTkrwPK9T3CMqS/qF8QLVJ7UG5aYMzyorWKiAHarWWluBh1+xLlEjZivEtRh2woZ
Rkfz6/djwUAFQKXSt/S1mja/qYh2iARVBCuch38aNzx+LaUa2NSJXsq9rD1s2G2v
1fN2D807iDginWyTmsQ9v4IbZT+mD12q/OWyFcq1rca8PdCE6OoGcrBNOTJ4vz4R
nAuknZoh8/CbCzB428Hch0P+vGOaysXCHMnHjf87ElgI5rY97HosTvuDls4MPGmH
VHOkc8KT/1EQrBVUAdj8BbGJoX90g5pJ19xOe4pIb4tF9g==
-----END CERTIFICATE-----

'''


def patch_ca_certs() -> None:
    ca_certs_directory = path.dirname(httplib2.__file__)
    ca_certs_already_monkeyed = path.join(ca_certs_directory, _CA_CERTS_FILE + '.monkeyed')
    ca_certs_filename = path.join(ca_certs_directory, _CA_CERTS_FILE)

    # Use an indicator file so that we don't repeatedly patch.
    if path.isfile(ca_certs_already_monkeyed):
        current_app.logger.debug('monkeypatch: previously done for httplib2 CA certificates file in "%s"', ca_certs_filename)
    else:
        try:
            # Read and prepend the certificate.
            with open(ca_certs_filename, 'rb') as file:
                text = file.read()
                text = _CERTIFICATE.replace('\n', '\r\n').encode('utf-8') + text

            # Write the new file.
            with open(ca_certs_filename, 'wb') as file:
                file.write(text)

            # Touch our indicator so we don't add the certificate again.
            pathlib.Path(ca_certs_already_monkeyed).touch()
        except FileNotFoundError:
            current_app.logger.warning(
                'monkeypatch: httplib2 CA certificates file expected in "%s" but not found', ca_certs_filename)
        else:
            current_app.logger.debug('monkeypatch: httplib2 CA certificates file in "%s"', ca_certs_filename)
