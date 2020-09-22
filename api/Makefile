.PHONY: setup

.PHONY: flake8

project_name := namex

SHELL:=/bin/bash
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
current_abs_dir := $(patsubst %/,%,$(dir $(mkfile_path)))

#################################################################################
# COMMANDS                                                                      #
#################################################################################

setup: setup-venv

venv/bin/activate: requirements/prod.txt requirements/dev.txt
	rm -rf venv/
	test -f venv/bin/activate || python3.6 -m venv  $(current_abs_dir)/venv
	. venv/bin/activate ;\
	pip install --upgrade pip ;\
	pip install -Ur requirements/dev.txt ;
	touch venv/bin/activate

setup-venv: requirements/dev.txt
	rm -rf venv/
	test -f venv/bin/activate || python3.6 -m venv  $(current_abs_dir)/venv
	. venv/bin/activate ;\
	pip install --upgrade pip ;
	pip install -Ur requirements/dev.txt;
	touch venv/bin/activate

## run flake8 on the package and tests
flake8:
	flake8 $(project_name) tests
