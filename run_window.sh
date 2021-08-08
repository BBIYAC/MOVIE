#!/bin/bash

if [ -d "venv" ]
then
    . venv/Scripts/activate
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
else
    python -m venv venv
    . venv/Scripts/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    python manage.py makemigrations
    python mamage.py migrate
    python manage.py runserver
fi