PYTHON ?= python3

export VIRTUAL_ENV := $(realpath .)/venv
export TOX_DIR := $(realpath .)/.tox
export PATH := $(VIRTUAL_ENV)/bin:$(PATH)
export DJANGO_MANAGE := $(TOX_DIR)/py35-d110/bin/python examples/djangoapp/manage.py
unexport WORKON_HOME PIP_RESPECT_VIRTUALENV PIP_VIRTUALENV_BASE

help:
	@echo
	@echo 'Make targets:'
	@echo '  make install'
	@echo '    -> make install.virtualenv'
	@echo '    -> make install.runtime'
	@echo '  make clean'
	@echo '  make test'
	@echo '  make tdd'


# Top-level phony targets
_install__runtime = $(VIRTUAL_ENV)/bin/django-admin.py
_install__virtualenv = $(VIRTUAL_ENV)/bin/pip

# make should not confuse these commands with files
.PHONY: install install.virtualenv install.runtime
.PHONY: clean

clean:
	rm -rf $(VIRTUAL_ENV)
	find . -type f -name '*.pyc' -print0 | xargs -0 rm -f
	find . -type d -name '__pycache__' -print0 | xargs -0 rm -rf

# Installation
install: install.virtualenv install.runtime
install.runtime:    $(_install__runtime)
install.virtualenv: $(_install__virtualenv)

$(_install__runtime):
	$(_install__virtualenv) install -r requirements/devel.txt
	$(VIRTUAL_ENV)/bin/python setup.py develop
	touch $@

$(_install__virtualenv):
	$(PYTHON) -mvenv $(VIRTUAL_ENV)
	@echo '================================================================'
	@echo 'You can now enable virtualenv with:'
	@echo '  source $(VIRTUAL_ENV)/bin/activate'
	@echo '================================================================'
	touch $@
	$(VIRTUAL_ENV)/bin/pip install -U pip


test:
	$(VIRTUAL_ENV)/bin/py.test ./api

tdd:
	$(VIRTUAL_ENV)/bin/ptw -c -- ./api


django_makemigrations:
	$(DJANGO_MANAGE) makemigrations ses
