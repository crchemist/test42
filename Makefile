MANAGE=django-admin.py

test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=homepage.settings $(MANAGE) test contacts requests

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=homepage.settings $(MANAGE) runserver

syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=homepage.settings $(MANAGE) syncdb --noinput

migrate:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=homepage.settings $(MANAGE) migrate

createsuperuser:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=homepage.settings $(MANAGE) createsuperuser
