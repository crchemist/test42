#!/bin/bash

FILENAME=`date --rfc-3339="date"`.dat
PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=homepage.settings django-admin.py printmodels 2>> $FILENAME
