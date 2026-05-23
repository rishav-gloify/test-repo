#!/usr/bin/env bash
set -o errexit

python manage.py migrate --no-input
python manage.py create_admin
gunicorn library_management_system.wsgi:application
