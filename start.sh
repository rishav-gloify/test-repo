#!/usr/bin/env bash
set -o errexit

python manage.py migrate --no-input
gunicorn library_management_system.wsgi:application
