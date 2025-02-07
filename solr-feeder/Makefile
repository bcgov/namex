.PHONY: license
.PHONY: setup
.PHONY: ci cd
.PHONY: run

MKFILE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_ABS_DIR:=$(patsubst %/,%,$(dir $(MKFILE_PATH)))

PROJECT_NAME:=solr_feeder
DOCKER_NAME:=solr-feeder

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

install: clean ## Install dependencies
	poetry install

install-dev: ## Install local application
	poetry install

#################################################################################
# COMMANDS - CI                                                                 #
#################################################################################
ci: pylint flake8 test ## CI flow

pylint: ## Linting with pylint
	poetry run pylint --rcfile=setup.cfg $(PROJECT_NAME)

flake8: ## Linting with flake8
	poetry run flake8 $(PROJECT_NAME)

lint: pylint flake8 ## run all lint type scripts

test: ## Unit testing
	poetry run pytest

mac-cov: test ## Run the coverage report and display in a browser window (mac)
	@open -a "Google Chrome" htmlcov/index.html

#################################################################################
# COMMANDS - Local                                                              #
#################################################################################
run: ## Run the project in local
	poetry run python -m flask run -p 8080

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################
.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
