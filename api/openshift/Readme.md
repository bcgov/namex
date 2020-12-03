
# buildconfig
oc process -f openshift/templates/bc.yaml -o yaml | oc apply -f - -n f2b77c-tools
# deploymentconfig, service and route
oc process -f openshift/templates/dc.yaml -o yaml | oc apply -f - -n f2b77c-dev
oc process -f openshift/templates/dc.yaml -p TAG=test -p APPLICATION_DOMAIN=namex-api-test.apps.silver.devops.gov.bc.ca -o yaml | oc apply -f - -n f2b77c-test
oc process -f openshift/templates/dc.yaml -p TAG=prod -p APPLICATION_DOMAIN=namex-api.apps.silver.devops.gov.bc.ca -o yaml | oc apply -f - -n f2b77c-prod

