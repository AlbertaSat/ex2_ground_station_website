#!/bin/sh
# This script is for the entrypoint when the app is deployed on a server
pip install -r requirements.txt
python3 manage.py recreate_db
python3 manage.py seed_db

gunicorn -b 0.0.0.0:5000 manage:app
