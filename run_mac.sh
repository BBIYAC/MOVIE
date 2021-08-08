#!/bin/bash

if [ -d "venv" ]
then
    . venv/bin/activate
    pip install -r requirements.txt
    python manage.py makemigrations
    python mamage.py migrate
    python manage.py runserver
else
    python3 -m venv venv
    . venv/bin/activate
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
    python manage.py makemigrations
    python mamage.py migrate
    python manage.py runserver
fi