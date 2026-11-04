.PHONY: license
.PHONY: setup
.PHONY: ci cd
.PHONY: db run

MKFILE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_ABS_DIR:=$(patsubst %/,%,$(dir $(MKFILE_PATH)))

PROJECT_NAME:=nr-duplicates-report
DOCKER_NAME:=nr-duplicates-report
VENV_DIR:=.venv

#################################################################################
# COMMANDS -- license                                                           #
#################################################################################
license: ## Verify source code license headers.
	./scripts/verify_license_headers.sh $(CURRENT_ABS_DIR)/src $(CURRENT_ABS_DIR)/tests

#################################################################################
# COMMANDS -- Setup                                                             #
#################################################################################
setup: clean install ## Setup the project

clean: clean-build clean-pyc clean-test ## Clean the project
	rm -rf $(VENV_DIR)/

clean-build: ## Clean build files
	rm -fr build/ dist/ .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc: ## Clean Python cache files
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## Clean test files
	find . -name '.pytest_cache' -exec rm -fr {} +
	rm -fr .tox/ .coverage htmlcov/

install: ## Install Python dependencies in a virtual environment
	test -f $(VENV_DIR)/bin/activate || python3.12 -m venv $(VENV_DIR) ;\
	. $(VENV_DIR)/bin/activate ;\
	pip install poetry ;\
	poetry install

#################################################################################
# COMMANDS - CI                                                                 #
#################################################################################
ci: lint test ## CI flow

lint: ## Run linting with pylint
	. $(VENV_DIR)/bin/activate && pylint --rcfile=setup.cfg nr_duplicates_report/**/*.py

test: ## Run unit tests
	. $(VENV_DIR)/bin/activate && pytest ./

#################################################################################
# COMMANDS - Local                                                              #
#################################################################################
run:
	. $(VENV_DIR)/bin/activate && poetry run python notebookreport.py

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################
.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
