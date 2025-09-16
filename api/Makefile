.PHONY: license
.PHONY: setup
.PHONY: ci cd
.PHONY: db run
.PHONY: flake8 lint

MKFILE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_ABS_DIR:=$(patsubst %/,%,$(dir $(MKFILE_PATH)))

PROJECT_NAME:=namex_api
PROJECT_FOLDER_NAME:=namex
DOCKER_NAME:=namex-api

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
	docker build -f Dockerfile -t namex-api .

ruff: ## ruff linter
	poetry run ruff check

ruff-fix: ## auto fix lint issues with ruff
	poetry run ruff check --fix

test: local-db ## unit testing with local db
	poetry run pytest

#################################################################################
# COMMANDS - Local                                                              #
#################################################################################

run: local-db ## Run the project in local
	. .venv/bin/activate && python3.12 -m flask run -p 5000

local-db:  ## Set up the local development database
	docker compose -f dev-scripts/local-db/docker-compose.yml up -d
	./update_db.sh

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################
.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
