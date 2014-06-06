# Makefile for cogenda web 

.PHONY: help

# Internal variables.
root_dir=cogenda-app
# Babel variables
babel_dict_loc=./cogenda-app/i18n/message.pot
babel_domain=cogenda-app
babel_i18n=./cogenda-app/i18n

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo ""
	@echo "  run           to run web server on local env"
	@echo "  db-init       to initial SQLite databse file."
	@echo "  db-migrate    to sync and migrate database schema."
	@echo "  db-version    to verify database schema version."
	@echo "  db-schema     to generate database schema change set."
	@echo "  db-script     to generate SQL schema changes."
	@echo "  babel-extract to extract i18n messages from *.py and template files."
	@echo "  babel-update  to update i18n messages from message.pot *.po files."
	@echo "  babel-compile to update i18n messages from *.po file to *.mo files."
	@echo "  deploy        to deploy application to production evironment."
	@echo "  clean-pyc     to clean project *.pyc files."
	@echo ""

####################################################################
#  				     CherryPy Server Management                    #
####################################################################
run:
	@python ${root_dir}/cogenda-app.py

####################################################################
#  				     SQLite Management                             #
####################################################################
init-db:
	@python migration/manage.py version_control sqlite:///migration/cogenda-app.db migration
	@python manage.py upgrade

db-migrate:
	@python manage.py upgrade

db-version:
	@python manage.py version

db-script:
	@python manage.py script

####################################################################
#  				     Babel I18n Management                         #
####################################################################
babel-extract:
	@pybabel extract -F babel.cfg -o ${babel_dict_loc} ./

babel-update:
	@pybabel update -i ${babel_dict_loc} -D ${babel_domain} -d ${babel_i18n}

babel-compile:
	@pybabel compile -D ${babel_domain} -d ${babel_i18n}

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*.DS_Store' -exec rm -f {} +
	@find . -name '~' -exec rm -f {} +

####################################################################
#  				     Production Server Deployment                  #
####################################################################
deploy:
	@fab setup:$(PROD_SERVER_SECRET),$(PROD_SERVER)
