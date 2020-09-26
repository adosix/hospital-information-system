#!/bin/bash
#activate virtual environment
source ../Environments/Djangoenv/bin/activate
#check for changes and run server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
