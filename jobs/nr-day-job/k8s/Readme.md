

# buildconfig
oc process -f k8s/templates/bc.yaml -o yaml | oc apply -f - -n f2b77c-tools
# cronjob
oc process -f k8s/templates/cronjob.yaml -p SCHEDULE="0 * * * *" -o yaml | oc apply -f - -n f2b77c-dev
oc process -f k8s/templates/cronjob.yaml -p TAG=test -p SCHEDULE="0 * * * *" -o yaml | oc apply -f - -n f2b77c-test
oc process -f k8s/templates/cronjob.yaml -p TAG=prod -p SCHEDULE="0 * * * *" -o yaml | oc apply -f - -n f2b77c-prod
# manually run job
oc create job --from=cronjob/<cronjob-name> <job-name> -n f2b77c-prod
