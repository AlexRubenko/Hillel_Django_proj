#!/bin/bash

echo "Starting migrations"
python src/manage.py migrate

echo "Starting the development server"
python src/manage.py runserver 0:8008
