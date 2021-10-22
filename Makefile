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
	@echo "LAM Makefile help.\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: aws-login ## Create docker image 
	docker compose build;

up: ## Runs the image
	docker compose up;

configure_devel: ## Delete/create virtual environment and install all requirements
	if [ -d "venv" ]; then \
		rm -rf venv; \
    fi;
	python3 -m venv venv;
	bash -c "source venv/bin/activate && pip install -r requirements.txt && pip install -r requirements/develop.txt"
	pre-commit install

aws-login: ## Login using AWS cli on ECR to pull images
	aws ecr get-login-password --region us-east-2 --profile diogo  | docker login --username AWS --password-stdin 018008741390.dkr.ecr.us-east-2.amazonaws.com

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
