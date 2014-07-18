# Makefile for cogenda web application

.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo ""
	@echo "  run               to run web server on local env"
	@echo "  db-init           to initial SQLite databse file by schema"
	@echo "  db-migrate        to sync and migrate database schema."
	@echo "  db-version        to verify database schema version."
	@echo "  db-schema         to generate database schema change set."
	@echo "  db-script         to generate SQL schema changes."
	@echo "  db-fixture        to load application initial data into SQLite3."
	@echo "  babel-extract     to extract i18n messages from *.py and template files."
	@echo "  babel-update      to update i18n messages from message.pot *.po files."
	@echo "  babel-compile     to update i18n messages from *.po file to *.mo files."
	@echo "  deploy            to deploy application to production evironment."
	@echo "  encrypt-key       to encrypt sensitive data & private keys in travis ci."
	@echo "  encrypt-key-mac   to encrypt sensitive data & private keys in travis ci on Mac OSX."
	@echo "  pylint            to inspect python code defects."
	@echo "  jslint            to inspect javascript code defects."
	@echo "  clean-pyc         to clean project *.pyc files."
	@echo ""

####################################################################
#  				     CherryPy Server Management                    #
####################################################################
# Internal variables.
root_dir=cogenda-app
settings_prod=cogenda-prod.ini
settings_dev=cogenda-dev.ini

run:
	@python ${root_dir}/cogenda-app.py ${settings_dev}

run-prod:
	@python ${root_dir}/cogenda-app.py ${settings_prod}

####################################################################
#  				     SQLite Management                             #
####################################################################
# SQLite2 variables
cogenda_fixture=migration/fixture.sql
cogenda_db=migration/cogenda-app.db

.PHONY: db-setup
db-setup: db-init db-fixture

db-init:
	@python migration/manage.py version_control sqlite:///migration/cogenda-app.db migration
	@python manage.py upgrade

db-migrate:
	@python manage.py upgrade

db-version:
	@python manage.py version

db-script:
	@python manage.py script $(ACTION)

db-fixture:
	@sqlite3 ${cogenda_db} < ${cogenda_fixture}

####################################################################
#  				     Babel I18n Management                         #
####################################################################
# Babel variables
babel_dict_loc=./cogenda-app/i18n/message.pot
babel_domain=cogenda-app
babel_i18n=./cogenda-app/i18n

babel-extract:
	@python setup.py extract_messages -o ${babel_dict_loc}


babel-update:
	@python setup.py update_catalog -i ${babel_dict_loc} -D ${babel_domain} -d ${babel_i18n}


babel-compile:
	@python setup.py compile_catalog -D ${babel_domain} -d ${babel_i18n}


####################################################################
#  				     Web Assets Management                         #
####################################################################
web:
	@npm install
	@sudo npm install -g grunt-cli
	@sudo npm install -g bower
	@bower install
	@grunt build
	@grunt inject

####################################################################
#  				     Production Server Deployment                  #
####################################################################
deploy:
	@fab prepare install_app migrate_db restart_app restart_nginx

encrypt-key:
	@./bin/travis_encrypt_key.sh 

encrypt-key-mac:
	@./bin/travis_encrypt_key_mac.sh 


####################################################################
#  				    Code Inspect & Utility                         #
####################################################################
pylint:
	@flake8 cogenda-app fabfile.py

jslint:
	@grunt jslint

clean-pyc:
	@find cogenda-app -name '*.pyc'|xargs rm -f
	@find cogenda-app -name '*.pyo'|xargs rm -f 
	@find cogenda-app -name '*.DS_Store'|xargs rm -f 
	@find cogenda-app -name '~'|xargs rm -f
