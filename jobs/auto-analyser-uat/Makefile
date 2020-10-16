.PHONY: setup

.PHONY: flake8

SHELL:=/bin/bash
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
current_abs_dir := $(patsubst %/,%,$(dir $(mkfile_path)))

#################################################################################
# COMMANDS                                                                      #
#################################################################################

setup: setup-venv

build-req: venv/bin/activate

venv/bin/activate: requirements/prod.txt requirements/dev.txt
	rm -rf venv/
	test -f venv/bin/activate || python3.8 -m venv  $(current_abs_dir)/venv
	. venv/bin/activate ;\
	pip install --upgrade pip ;\
	pip install -Ur requirements/prod.txt ;\
	pip freeze | sort > requirements.txt ;\
	pip install -Ur requirements/dev.txt ;\
	pip install -e .
	touch venv/bin/activate

setup-venv: requirements/dev.txt
	rm -rf venv/
	test -f venv/bin/activate || python3.8 -m venv  $(current_abs_dir)/venv
	. venv/bin/activate ;\
	pip install --upgrade pip ;\
	pip install --upgrade pip ;\
	pip install -Ur requirements.txt ;\
	pip install -Ur requirements/dev.txt ;\
	pip install -e .
	touch venv/bin/activate

## run flake8 on the package and tests
flake8:
	flake8 .
