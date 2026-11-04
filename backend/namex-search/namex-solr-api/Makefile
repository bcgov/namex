.PHONY: lint
.PHONY: build

MKFILE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_ABS_DIR:=$(patsubst %/,%,$(dir $(MKFILE_PATH)))

PROJECT_NAME:=namex_solr_api
DOCKER_NAME:=namex-solr-api

#################################################################################
# COMMANDS -- Setup                                                             #
#################################################################################

#################################################################################
# COMMANDS - CI                                                                 #
#################################################################################
pylint: ## Linting with pylint
	pylint --rcfile=setup.cfg src/$(PROJECT_NAME)

flake8: ## Linting with flake8 ## tests
	flake8 src/$(PROJECT_NAME)

lint: pylint flake8 ## run all lint type scripts

test: ## Unit testing
	pytest

build: ## Build the docker container
	docker build . -t $(DOCKER_NAME) \
	    --platform linux/amd64 \
	    --build-arg VCS_REF=$(shell git rev-parse --short HEAD) \
	    --build-arg BUILD_DATE=$(shell date -u +"%Y-%m-%dT%H:%M:%SZ")

build-nc: ## Build the docker container without caching
	docker build --no-cache -t $(DOCKER_NAME) .

#################################################################################
# COMMANDS - Local                                                              #
#################################################################################

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################
.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
