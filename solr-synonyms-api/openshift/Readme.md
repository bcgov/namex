
# buildconfig
oc process -f openshift/templates/bc.yaml -o yaml | oc apply -f - -n f2b77c-tools
# deploymentconfig, service and route
oc process -f openshift/templates/dc.yaml -o yaml | oc apply -f - -n f2b77c-dev
oc process -f openshift/templates/dc.yaml -p TAG=test -o yaml | oc apply -f - -n f2b77c-test
oc process -f openshift/templates/dc.yaml -p TAG=prod -o yaml | oc apply -f - -n f2b77c-prod

