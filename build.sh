#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip first
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate 