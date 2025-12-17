.PHONY: license
.PHONY: setup
.PHONY: ci cd
.PHONY: run

MKFILE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_ABS_DIR:=$(patsubst %/,%,$(dir $(MKFILE_PATH)))

PROJECT_NAME:=solr_names_updater
DOCKER_NAME:=solr-names-updater

#################################################################################
# COMMANDS -- Setup                                                             #
#################################################################################
setup: install ## Setup the project

clean: clean-build clean-pyc clean-test ## Clean the project
	rm -rf .venv/
	rm -rf poetry.lock

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

update: ## Upgrade lock
	poetry update

install: clean ## Install python virtrual environment
	test -f .venv/bin/activate || python3.12 -m venv  $(CURRENT_ABS_DIR)/.venv ;\
	. .venv/bin/activate ;\
	pipx install poetry
	poetry install

#################################################################################
# COMMANDS - CI                                                                 #
#################################################################################
ci: docker-build-check ruff test ## CI flow

docker-build-check: ## Check if Dockerfile builds successfully
	docker build -f Dockerfile -t namex-emailer .

ruff: ## ruff linter
	poetry run ruff check

ruff-fix: ## auto fix lint issues with ruff
	poetry run ruff check --fix

test: ## unit testing with local db
	poetry run pytest

#################################################################################
# COMMANDS - Local                                                              #
#################################################################################

run: ## Run the project in local
	. .venv/bin/activate && python3.12 run.py

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################
.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
