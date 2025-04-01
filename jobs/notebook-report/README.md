# Notebook Report

Generate notebook report

## Development Environment

Follow the instructions of the [Development Readme](https://github.com/bcgov/entity/blob/master/docs/development.md)
to setup your local development environment.

## Development Setup

1. Follow the [instructions](https://github.com/bcgov/entity/blob/master/docs/setup-forking-workflow.md) to checkout the project from GitHub.
2. Open the notebook-report directory in VS Code to treat it as a project (or WSL projec). To prevent version clashes, set up a virtual environment to install the Python packages used by this project.

## Running Notebook Report
1. Run `make setup` to set up the virtual environment and install libraries.
2. Run `poetry shell` to change to `.venv` environment.
3. Keep .env file under notebook-report directory
3. Run 'cd src'.
4. Run notebook with `poetry run python notebookreport.py` in src directory or './run.sh' in notebook-report directory.

### Important: Please remember to do "git update-index --add --chmod=+x run.sh" before run.sh is commit to github on first time. 
### Build API - can be done in VS Code

1. Login to openshift

   ```sh
   oc login xxxxxxx
   ```

2. switch to tools namespace

   ```sh
   oc project f2b77c-tools
   ```

3. Create build image

   ```sh
   #cd */namex/jobs/notebook-report/openshift/templates
   #oc create imagestream notebook-report
   oc process -f openshift/templates/bc.yaml \
	  -p GIT_REPO_URL=https://github.com/bcgov/namex.git \
	  -p GIT_REF=main \
	  -o yaml \
   | oc apply -f - -n f2b77c-tools     
   ```

4. Checking log for building process at Console => Administrator => Builds => Builds => click image 'notebook-report' => logs

5. Tag image to dev: 'oc tag notebook-report:latest notebook-report:dev'


### Create cron

1. Login to openshift

   ```sh
   oc login xxxxxxx
   ```

2. switch to dev namespace

   ```sh
   oc project f2b77c-dev
   ```

3. Create cron
   ### please remember that SCHEDULE is UTC which is 7 hour ahead of PST
   ```sh
   oc process -f openshift/templates/cronjob.yaml \
     -p TAG=dev \
     -p SCHEDULE="30 14 * * *" \
     -o yaml \
     | oc apply -f - -n f2b77c-dev
   ```
4. Create a job to run and test it: 'oc create job notebook-report-dev-1 --from=cronjob/notebook-report-dev -n f2b77c-dev'
