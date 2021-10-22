# .SILENT:

ifeq ($(OS),Windows_NT)
	OPEN := start
else
	UNAME := $(shell uname -s)
	ifeq ($(UNAME),Linux)
		OPEN := xdg-open
	endif
	ifeq ($(UNAME),Darwin)
		OPEN := open
	endif
endif

.PHONY: help

help: ## Show this help message
	@echo "Makefile commands help.\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Create docker image 
	docker-compose build;

up: ## Runs the image
	docker-compose up;
	
codegen: ## Generate flask base code from openAPI YAML specifications
	mv README.md BCK.README.md
	docker run --rm -v $(PWD)/:/local openapitools/openapi-generator-cli generate -i /local/drm_appointment/drm_appointment.yaml -g python-flask -o /local/ --minimal-update --package-name drm_appointment
	rm requirements.txt setup.py test-requirements.txt tox.ini git_push.sh Dockerfile .travis.yml	
	docker run --rm -v $(PWD)/:/local openapitools/openapi-generator-cli generate -i /local/drm_financial/drm_financial.yaml -g python-flask -o /local/ --minimal-update --package-name drm_financial
	rm requirements.txt setup.py test-requirements.txt tox.ini git_push.sh Dockerfile .travis.yml	
	mv BCK.README.md README.md 

migrate_db: ## start the db migration tasks
	@PGPASSWORD=sOmE_sEcUrE_pAsS psql -h localhost -p 5032 -U postgres postgres < ddl/auto_migration.sql

configure_devel: ## Delete/create virtual environment and install all requirements
	if [ -d "venv" ]; then \
		rm -rf venv; \
    fi;
	python3 -m venv venv;
	bash -c "source venv/bin/activate && pip install -r requirements/base.txt && pip install -r requirements/develop.txt"
	pre-commit install

init_test: ## Runs all project test suite, recording all test converage data
	if [ -d "coverage-reports" ]; then \
		rm -rf coverage-reports; \
    fi;
	if [ -d "htmlcov" ]; then \
		rm -rf htmlcov; \
    fi;	
	if [ -a "coverage.xml" ]; then \
		rm coverage.xml; \
    fi;	
	
	-pytest; 
	-coverage xml;
	-coverage3 html;
