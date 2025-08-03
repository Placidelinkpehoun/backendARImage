#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip first
pip install --upgrade pip

# Install requirements with fallback for psycopg2
pip install -r requirements.txt || {
    echo "Failed to install psycopg2-binary, trying psycopg2..."
    pip install psycopg2==2.9.9
    pip install -r requirements.txt
}

python manage.py collectstatic --no-input
python manage.py migrate 