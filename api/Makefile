.PHONY: setup build-req clean clean-build clean-pyc clean-test

.PHONY: flake8 lint

PROJECT_NAME := namex

SHELL:=/bin/bash
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
current_abs_dir := $(patsubst %/,%,$(dir $(mkfile_path)))

#################################################################################
# COMMANDS                                                                      #
#################################################################################
clean: clean-build clean-pyc clean-test
	rm -rf venv/

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	find . -name '.pytest_cache' -exec rm -fr {} +
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	
setup: setup-venv

venv/bin/activate: requirements/prod.txt requirements/dev.txt
	rm -rf venv/
	test -f venv/bin/activate || python3 -m venv  $(current_abs_dir)/venv
	. venv/bin/activate ;\
	pip install --upgrade pip ;\
	pip install -Ur requirements/dev.txt ;
	touch venv/bin/activate

setup-venv: requirements/dev.txt
	rm -rf venv/
	test -f venv/bin/activate || python3 -m venv  $(current_abs_dir)/venv
	. venv/bin/activate ;\
	pip install --upgrade pip ;
	pip install -Ur requirements.txt;
	touch venv/bin/activate

## run flake8 on the package and tests
flake8:
	flake8 $(project_name) tests

lint: ## Linting with pylint
	. venv/bin/activate && pylint --rcfile=setup.cfg $(PROJECT_NAME)

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