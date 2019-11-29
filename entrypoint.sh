#!/bin/sh
pip install -r requirements.txt
python3 manage.py recreate_db
python3 manage.py seed_db

gunicorn -b 0.0.0.0:5000 manage:app
