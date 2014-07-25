# Makefile for cogenda web application

.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo ""
	@echo "  run               to run web server on local env"
	@echo "  alembic-init      to initial SQLite databse file by schema"
	@echo "  alembic-upgrade   to sync and migrate database schema."
	@echo "  alembic-version   to verify database schema version."
	@echo "  alembic-revision  to generate SQL schema changes."
	@echo "  alembic-fixture   to load application initial data into SQLite3."
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
root_dir=cogenda_app
settings_prod=cogenda-prod.ini
settings_dev=cogenda-dev.ini

run:
	@python -m cogenda_app.cogenda_app ${settings_dev}

run-prod:
	@python -m cogenda_app.cogenda_app ${settings_prod}

####################################################################
#  				     Babel I18n Management                         #
####################################################################
# Babel variables
babel_dict_loc=./cogenda_app/i18n/message.pot
babel_domain=cogenda_app
babel_i18n=./cogenda_app/i18n

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
	@grunt build
	@grunt inject

####################################################################
#  				     Production Server Deployment                  #
####################################################################
deploy_dist:
	@fab prepare tarball upload_dist install_app restart_app restart_nginx clean

encrypt-key:
	@./bin/travis_encrypt_key.sh 

encrypt-key-mac:
	@./bin/travis_encrypt_key_mac.sh 


####################################################################
#  				    Code Inspect & Utility                         #
####################################################################
pylint:
	@flake8 cogenda_app fabfile.py

jslint:
	@grunt jslint

clean-pyc:
	@find cogenda_app -name '*.pyc'|xargs rm -f
	@find cogenda_app -name '*.pyo'|xargs rm -f 
	@find cogenda_app -name '*.DS_Store'|xargs rm -f 
	@find cogenda_app -name '~'|xargs rm -f

tarball:
	@
####################################################################
#  				    Run Tests                                      #
####################################################################
BENCHMARK_TARGET= http://localhost:8088
benchmark:
	@siege -c100 -d1 -r100 ${BENCHMARK_TARGET}

test-reset: alembic-init
	@python -m tests.unittest.cogenda_app_test
	@rm -f ${cogenda_db}

test:
	@python -m tests.unittest.cogenda_app_test

####################################################################
#  				     SQLite Management                             #
####################################################################
# SQLite3 variables
cogenda_fixture=alembic/fixture.sql
cogenda_db=alembic/cogenda_app.db

alembic-init:
	@alembic upgrade head
	@sqlite3 ${cogenda_db} < ${cogenda_fixture}

alembic-revision:
	@alembic revision --autogenerate

alembic-upgrade:
	@alembic upgrade head

alembic-version:
	@alembic current

alembic-downgrade:
	@alembic downgrade base

alembic-fixture:
	@sqlite3 ${cogenda_db} < ${cogenda_fixture}

alembic-upgrade-off:
	@alembic upgrade ${version} --sql > alembic/offline/migration.sql

alembic-downgrade-off:
	@alembic downgrade ${version} --sql > alembic/offline/migration.sql
