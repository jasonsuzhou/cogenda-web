# Makefile for cogenda web 

# Internal variables.
root_dir=cogenda-app

run:
	@python ${root_dir}/cogenda-app.py

upgrade:
	@python manage.py upgrade

version:
	@python manage.py version

script:
	@python manage.py script
