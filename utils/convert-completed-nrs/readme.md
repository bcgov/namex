DATA

This script converts NRs with status COMPLETED to APPROVED, CONDITIONAL or REJECTED, based on the
name states. This functionality is in the extractor, but this script is meant to be run once to
find and fix data that had not been converted by the extractor.


LOCAL DEV ENVIRONMENT

To run locally (over local postgres database), just make sure your environment variables 
are set, just like when running API environment (ie: steps taken before "run flask"). Then 
just run: 

> python convert_completed_nrs.py

Runs for a few seconds.

DEV / TEST / PROD

To run over dev, test, or prod database:

- set up port forwarding via openshift to point to dev postgres database:

  - log into Open Shift and find login string. Run in cmd line. Looks something like this:
    - > oc login https://console.pathfinder.gov.bc.ca:8443 --token=xxx
  - In Open Shift console (dev or test) go to Applications > Pods and find the postgres db pod name 
  (the one that doesn't refer to Oracle). In below example, it is "postgresql-2-8b7hj".
  
  - Set up port forwarding to access that pod from your machine. If you are running postgres locally, 
  you have to pick a different port as well, such as 1111.
    - > oc port-forward postgresql-2-8b7hj 1111:5432  
  
  - set up the stub environment file (.env in this folder) to point to the dev or test database:
    - Username and password are found in OpenShift, under the "Environment" tab 
    - Port is what you set up in port forwarding step above.
    - Everything else you leave as is.
    
  - Run script:
    > python convert_completed_nrs.py
    - runs for a few minutes  
  