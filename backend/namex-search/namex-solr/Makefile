.PHONY: build
.PHONY: build-leader
.PHONY: build-follower
.PHONY: setup

DOCKER_NAME_LEADER:=name-request-solr-leader
DOCKER_NAME_FOLLOWER:=name-request-solr-follower
DOCKER_NAME_LOCAL:=name-request-solr-local

LEADER_CORE:=name_request
FOLLOWER_CORE:=name_request_follower

#################################################################################
# COMMANDS -- Setup                                                             #
#################################################################################

#################################################################################
# COMMANDS - CD                                                                 #
#################################################################################
build: build-leader build-follower
build-follower:
	docker build . -t $(DOCKER_NAME_FOLLOWER) \
	    --platform linux/amd64 \
	    --build-arg VCS_REF=$(shell git rev-parse --short HEAD) \
	    --build-arg BUILD_DATE=$(shell date -u +"%Y-%m-%dT%H:%M:%SZ") \
			--build-arg CORE=$(FOLLOWER_CORE) \
			--build-arg FOLLOWER_CORE=$(FOLLOWER_CORE) \
			--build-arg LEADER_CORE=$(LEADER_CORE) \
			--build-arg JVM_MEM=1g

build-leader:
	docker build . -t $(DOCKER_NAME_LEADER) \
	    --platform linux/amd64 \
	    --build-arg VCS_REF=$(shell git rev-parse --short HEAD) \
	    --build-arg BUILD_DATE=$(shell date -u +"%Y-%m-%dT%H:%M:%SZ") \
			--build-arg CORE=$(LEADER_CORE) \
			--build-arg FOLLOWER_CORE=$(FOLLOWER_CORE) \
			--build-arg LEADER_CORE=$(LEADER_CORE) \
			--build-arg JVM_MEM=2g

build-local:
	docker build . -t $(DOCKER_NAME_LOCAL) \
	    --platform linux/amd64 \
	    --build-arg VCS_REF=$(shell git rev-parse --short HEAD) \
	    --build-arg BUILD_DATE=$(shell date -u +"%Y-%m-%dT%H:%M:%SZ") \
			--build-arg CORE=$(LEADER_CORE) \
			--build-arg FOLLOWER_CORE=$(FOLLOWER_CORE) \
			--build-arg LEADER_CORE=$(LEADER_CORE) \
			--build-arg JVM_MEM=256m

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
