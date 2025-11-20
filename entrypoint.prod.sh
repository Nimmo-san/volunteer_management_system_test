#!/usr/bin/env bash

# CARE: doesnt always catch the error
set -e

cd /app/backend

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Starting gunicorn..."
python -m gunicorn config.wsgi:application \
    --preload --bind 0.0.0.0:8000 \
    --workers 3
