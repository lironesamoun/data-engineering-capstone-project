# Makefile
SHELL = /bin/bash

.PHONY: help
help:
	@echo "Commands:"
	@echo "env    : creates a dev virtual environment and install all the required package."
	@echo "install    : Install all packages."
	@echo "clean   : cleans all unnecessary files."
	@echo "test    : execute tests on code, data and models."


# Install
.ONESHELL:
install:
	python3 -m pip install --upgrade pip setuptools wheel && \
	python3 -m pip install -e ".[dev]" #&& \
	pre-commit install && \
	touch .pre-commit-config.yaml && \
	pre-commit autoupdate

# Cleaning
.PHONY: clean
clean: style
	find . -type f -name "*.DS_Store" -ls -delete
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	find . | grep -E ".trash" | xargs rm -rf
	rm -f .coverage
