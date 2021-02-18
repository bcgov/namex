.PHONY: license
.PHONY: setup
.PHONY: ci cd
.PHONY: run

MKFILE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_ABS_DIR:=$(patsubst %/,%,$(dir $(MKFILE_PATH)))

PROJECT_NAME:=namex_pay

#################################################################################
# COMMANDS -- Setup                                                             #
#################################################################################
setup: install install-dev ## Setup the project

clean: clean-build clean-pyc clean-test ## Clean the project
	rm -rf venv/

clean-build: ## Clean build files
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc: ## Clean cache files
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## clean test files
	find . -name '.pytest_cache' -exec rm -fr {} +
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

build-req: clean ## Upgrade requirements
	test -f venv/bin/activate || python3.8 -m venv  $(CURRENT_ABS_DIR)/venv ;\
	. venv/bin/activate ;\
	pip install pip==20.1.1 ;\
	pip install -Ur requirements/prod.txt ;\
	pip freeze | sort > requirements.txt ;\
	cat requirements/bcregistry-libraries.txt >> requirements.txt ;\
	pip install -Ur requirements/bcregistry-libraries.txt

install: clean ## Install python virtrual environment
	test -f venv/bin/activate || python3.8 -m venv  $(CURRENT_ABS_DIR)/venv ;\
	. venv/bin/activate ;\
	pip install pip==20.1.1 ;\
	pip install -Ur requirements.txt

install-dev: ## Install local application
	. venv/bin/activate ; \
	pip install -Ur requirements/dev.txt; \
	pip install -e .

#################################################################################
# COMMANDS - CI                                                                 #
#################################################################################
ci: lint flake8 test ## CI flow

lint: ## Linting with pylint
	. venv/bin/activate && pylint --rcfile=setup.cfg src/$(PROJECT_NAME)

flake8: ## Linting with flake8 ## tests
	. venv/bin/activate && flake8 src/$(PROJECT_NAME)

test: ## Unit testing
	. venv/bin/activate && pytest

mac-cov: test ## Run the coverage report and display in a browser window (mac)
	@open -a "Google Chrome" htmlcov/index.html

#################################################################################
# COMMANDS - CD                                                               #
#################################################################################
cd: build ## CD flow

build: ## Build the docker container
	docker build -t $(PROJECT_NAME) \
	--build-arg VCS_REF=$(shell git rev-parse --short HEAD) \
	--build-arg BUILD_DATE=$(shell date -u +"%Y-%m-%dT%H:%M:%SZ") \
	.

build-nc: ## Build the docker container without caching
	docker build --no-cache -t $(PROJECT_NAME) .

# expects the terminal to be oc login
# expects export OPENSHIFT_REGISTRY_ADDRESS=""
# expects export OPENSHIFT_NAMESPACE=""
registry-push: build ## Push the docker container to the registry & tag dev
	docker login $(OPENSHIFT_REGISTRY_ADDRESS) -u $(oc whoami) -p $(oc whoami -t) ; \
	docker image tag $(PROJECT_NAME):latest $(OPENSHIFT_REGISTRY_ADDRESS)/$(OPENSHIFT_NAMESPACE)/$(PROJECT_NAME):latest ; \
	docker image push $(OPENSHIFT_REGISTRY_ADDRESS)/$(OPENSHIFT_NAMESPACE)/$(PROJECT_NAME):latest

oc-tag: registry-push
	oc tag $(OPENSHIFT_NAMESPACE)/$(PROJECT_NAME):latest  $(OPENSHIFT_NAMESPACE)/$(PROJECT_NAME):dev

#################################################################################
# COMMANDS - Local                                                              #
#################################################################################

run: ## Run the project in local
	. venv/bin/activate && python run.py

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################
.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
