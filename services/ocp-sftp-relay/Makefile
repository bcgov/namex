.PHONY: license
.PHONY: setup
.PHONY: ci cd
.PHONY: db run
.PHONY: flake8 lint

MKFILE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_ABS_DIR:=$(patsubst %/,%,$(dir $(MKFILE_PATH)))

PROJECT_NAME:=namex_ocp_sftp_relay_api
PROJECT_FOLDER_NAME:=ocp-sftp-relay
DOCKER_NAME:=ocp-sftp-relay-api

#################################################################################
# COMMANDS -- license                                                           #
#################################################################################
license: ## Verify source code license headers.
	./scripts/verify_license_headers.sh $(CURRENT_ABS_DIR)/src $(CURRENT_ABS_DIR)/tests

#################################################################################
# COMMANDS -- Setup                                                             #
#################################################################################
setup: install activate

install:
	poetry install

activate:
	poetry shell

#################################################################################
# COMMANDS - Local                                                              #
#################################################################################
run:
	flask run

#################################################################################
# COMMANDS - CI                                                                 #
#################################################################################
ci: lint

pylint:
	poetry run pylint .

flake8:
	poetry run flake8

isort: 
	poetry run isort .

black:
	poetry run black .

lint: pylint flake8 isort

#################################################################################
# COMMANDS - CD
# expects the terminal to be openshift login
# expects export OPENSHIFT_DOCKER_REGISTRY=""
# expects export OPENSHIFT_SA_NAME="$(oc whoami)"
# expects export OPENSHIFT_SA_TOKEN="$(oc whoami -t)"
# expects export OPENSHIFT_REPOSITORY=""
# expects export TAG_NAME="dev/test/prod"
# expects export OPS_REPOSITORY=""                                                        #
#################################################################################
cd: ## CD flow
ifeq ($(TAG_NAME), test)
## cd: update-env
cd:
	oc -n "$(OPENSHIFT_REPOSITORY)-tools" tag $(DOCKER_NAME):dev $(DOCKER_NAME):$(TAG_NAME)
else ifeq ($(TAG_NAME), prod)
## cd: update-env
cd:
	oc -n "$(OPENSHIFT_REPOSITORY)-tools" tag $(DOCKER_NAME):$(TAG_NAME) $(DOCKER_NAME):$(TAG_NAME)-$(shell date +%F)
	oc -n "$(OPENSHIFT_REPOSITORY)-tools" tag $(DOCKER_NAME):test $(DOCKER_NAME):$(TAG_NAME)
else
TAG_NAME=dev
## cd: build update-env tag
cd: build tag
endif

build: ## Build the docker container
	docker build . -t $(DOCKER_NAME) \
	    --platform=linux/amd64 \
		--build-arg VCS_REF=$(shell git rev-parse --short HEAD) \
		--build-arg BUILD_DATE=$(shell date -u +"%Y-%m-%dT%H:%M:%SZ") \

build-nc: ## Build the docker container without caching
	docker build --no-cache -t $(DOCKER_NAME) .

REGISTRY_IMAGE=$(OPENSHIFT_DOCKER_REGISTRY)/$(OPENSHIFT_REPOSITORY)-tools/$(DOCKER_NAME)
push: #build ## Push the docker container to the registry & tag latest
	@echo "$(OPENSHIFT_SA_TOKEN)" | docker login $(OPENSHIFT_DOCKER_REGISTRY) -u $(OPENSHIFT_SA_NAME) --password-stdin ;\
    docker tag $(DOCKER_NAME) $(REGISTRY_IMAGE):latest ;\
    docker push $(REGISTRY_IMAGE):latest

# VAULTS=`cat devops/vaults.json`
# update-env: ## Update env from 1pass
#	oc -n "$(OPS_REPOSITORY)-$(TAG_NAME)" exec "dc/vault-service-$(TAG_NAME)" -- ./scripts/1pass.sh \
#		-m "secret" \
#		-e "$(TAG_NAME)" \
#		-a "$(DOCKER_NAME)-$(TAG_NAME)" \
#		-n "$(OPENSHIFT_REPOSITORY)-$(TAG_NAME)" \
#		-v "$(VAULTS)" \
#		-r "true" \
#		-f "false"

tag: push ## tag image
	oc -n "$(OPENSHIFT_REPOSITORY)-tools" tag $(DOCKER_NAME):latest $(DOCKER_NAME):$(TAG_NAME)
