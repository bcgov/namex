.PHONY: setup

MKFILE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_ABS_DIR:=$(patsubst %/,%,$(dir $(MKFILE_PATH)))

#################################################################################
# COMMANDS -- Setup                                                             #
#################################################################################
setup: clean install install-dev ## Setup the project

clean: clean-build clean-pyc ## Clean the project
	rm -rf venv/

clean-pyc: ## Clean cache files
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-build: ## Clean build files
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

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
	pip install -Ur requirements/dev.txt;

#################################################################################
# COMMANDS - CI                                                                 #
#################################################################################

pylint: ## Linting with pylint
	. venv/bin/activate && pylint --rcfile=setup.cfg  inprogress_update.py

flake8: ## Linting with flake8
	. venv/bin/activate && flake8 inprogress_update.py

lint: pylint flake8 ## run all lint type scripts

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################
.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
