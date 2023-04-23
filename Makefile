# Makefile
SHELL = /bin/bash

.PHONY: help
help:
	@echo "Commands:"
	@echo "install    :  creates a dev virtual environment and install all the required package."
	@echo "uninstall    : Delete the environment "
	@echo "export-env    : Export all the env variables "
	@echo "init-infrastructure    : Init the GCP infrastructure"
	@echo "destroy-infrastructure    : Destroy the GCP infrastructure"
	@echo "prefect-start    : Run Prefect server"
	@echo "pyenv    :  creates a pyenv environment"
	@echo "clean   : cleans all unnecessary files."
	@echo "test    : execute tests on code, data and models."


.ONESHELL:
pyenv:
	pyenv install 3.11.2
	pyenv virtualenv 3.11.2 captstone-project
	pyenv activate captstone-project

# Install
.ONESHELL:
install:
	python3 -m venv venv && \
	source venv/bin/activate && \
	python3 -m pip install --upgrade pip setuptools wheel && \
	python3 -m pip install -e ".[dev]" #&& \
	pre-commit install && \
	pre-commit autoupdate && \
	mv .env.dist .env

# Install
.ONESHELL:
uninstall:
	source deactivate && \
	rm -rf venv

# Cleaning
.PHONY: clean
clean: style
	find . -type f -name "*.DS_Store" -ls -delete
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	find . | grep -E ".trash" | xargs rm -rf
	rm -f .coverage


.ONESHELL:
init-infrastructure:
	make export-env  && \
	cd terraform && \
	terraform fmt && \
	terraform init && \
	terraform validate && \
	terraform apply && \
	cd ..

.ONESHELL:
destroy-infrastructure:
	make export-env  && \
	cd terraform && \
	terraform destroy && \
	cd ..


.ONESHELL:
prefect-init:
	 prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api

.ONESHELL:
prefect-start:
	prefect server start

.ONESHELL:
prefect-init-blocks:
	 python3 src/blocks/init_prefect_blocks.py

.ONESHELL:
export-env:
	set -o allexport && source .env && set +o allexport
