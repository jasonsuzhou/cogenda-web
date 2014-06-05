# Makefile for cogenda web 

.PHONY: help

# Internal variables.
root_dir=cogenda-app

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo ""
	@echo "  run           to run web server on local env"
	@echo "  sync          to sync and migrate database schema."
	@echo "  version       to verify database schema version."
	@echo "  schema        to generate database schema change set."
	@echo "  clean-pyc     to clean project *.pyc files."
	@echo "  script        to generate SQL schema changes."
	@echo ""

run:
	@python ${root_dir}/cogenda-app.py

sync:
	@python manage.py upgrade

version:
	@python manage.py version

script:
	@python manage.py script

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '~' -exec rm -f {} +
