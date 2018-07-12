DATA

This script runs over two CSV files that are stored in the folder:
- restricted_words.csv
- restricted_condition.csv

To replace data, replace these files. Column names must match (case sensitive) but can be
in any order. 

The restricted_word.csv file is simply a list of the restricted words.

The restricted_condition.csv file is a list of conditions including cross-reference to words. 


LOCAL DEV ENVIRONMENT

To run locally (over local postgres database), just make sure your environment variables 
are set, just like when running API environment (ie: steps taken before "run flask"). Then 
just run: 

> python refresh_restricted_words.py

Runs for a few seconds.

DEV / TEST

To run over dev or test database:

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
    
  - Set environment variables:
    - > source .env
    
  - Run script:
    - > python refresh_restricted_words.py
    - runs for a few minutes  
  