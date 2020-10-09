#!/bin/bash
#activate virtual environment
source ../Environments/hospital_env/bin/activate
#check for changes and run server
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
