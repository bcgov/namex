# buildconfig
oc process -f openshift/templates/bc.yaml -o yaml | oc apply -f - -n f2b77c-tools
# cronjob
oc process -f openshift/templates/cronjob.yaml -o yaml | oc apply -f - -n f2b77c-dev
oc process -f openshift/templates/cronjob.yaml -p TAG=test -o yaml | oc apply -f - -n f2b77c-test
oc process -f openshift/templates/cronjob.yaml -p TAG=prod -o yaml | oc apply -f - -n f2b77c-prod

