.PHONY: clean clean-test clean-pyc help start stop remove invoke
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"
MODULE := {{ cookiecutter.project_slug }}
STAGE := dev
STAGE_LOWER := $(shell echo "${STAGE}" | tr '[:upper:]' '[:lower:]')
OFFLINE_PROCESS := serverless offline start
KEEPALIVE := false
# DATA := 
ifeq ($(DATA),)
DATA_PARAM := $(something else)
endif

BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD=\033[1m

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

new_repo:
	git init
	git add .
	git commit -m "initial commit"
	hub create -o -p {{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}

clean: clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -f .coverage
	rm -f coverage.xml
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: ## check style with flake8
	@echo "${BLUE}Running Pylint against source and test files...${NC}"
	@pylint --rcfile=setup.cfg **/*.py
	@echo "${BLUE}Running Flake8 against source and test files...${NC}"
	@flake8 ${MODULE}
	@echo "${BLUE}Running Bandit against source files...${NC}"
	@bandit -r --ini setup.cfg

test: ## run tests quickly with the default Python
{%- if cookiecutter.use_pytest == 'y' %}
	@py.test
{%- else %}
	@python setup.py test
{%- endif %}

coverage: ## check code coverage quickly with the default Python
{%- if cookiecutter.use_pytest == 'y' %}
	@coverage run --source {{ cookiecutter.project_slug }} -m pytest
{%- else %}
	@coverage run --source {{ cookiecutter.project_slug }} setup.py test
{%- endif %}
	@coverage report -m
	@coverage html
	@$(BROWSER) htmlcov/index.html

install: clean ## install the package to the active Python's site-packages
	@pipenv install

invoke: ## invoke function deployed to stage: STAGE (dev)
	@echo "${BLUE}Invoking ${MODULE} to ${STAGE_LOWER}...${NC}"
	npx serverless invoke -f {{ cookiecutter.project_slug }} --stage ${STAGE_LOWER} ${DATA_PARAM}

run_local: clean test ## invoke function locally
	@$(MAKE) _invoke_local || $(MAKE) _stop_serverless_offline

deploy: _package _deploy_package ## deploy function to stage: STAGE (dev)

remove: ## remove function deployed to stage: STAGE (dev)
	@echo "${BLUE}Removing ${STAGE_LOWER} for service: ${MODULE}...${NC}"
	npx serverless remove --stage ${STAGE_LOWER}

############# 
#  Helpers  #
############# 

_start_serverless_offline: _stop_serverless_offline
	@${OFFLINE_PROCESS} & echo $$! > /dev/null
	@sleep 10
	@exit

_stop_serverless_offline:
	@if pgrep -f '${OFFLINE_PROCESS}' > /dev/null; then pkill -f '${OFFLINE_PROCESS}' & pkill java;	fi & echo $$! > /dev/null
	@sleep 2

_invoke_local: _start_serverless_offline
	@sleep 5
	@npx serverless invoke local -f {{ cookiecutter.project_slug }} --stage ${STAGE_LOWER} ${DATA_PARAM}
	@if [ $(KEEPALIVE) = false ]; then $(MAKE) _stop_serverless_offline;	fi

_package:
	@npx serverless package --stage ${STAGE_LOWER} --package artifacts

_deploy_package:
	@echo "${BLUE}Deploying ${MODULE} to ${STAGE_LOWER}...${NC}"
	@npx serverless deploy --stage ${STAGE_LOWER} --package artifacts