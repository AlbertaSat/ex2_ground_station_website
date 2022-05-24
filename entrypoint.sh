#!/bin/sh
# This script is for the entrypoint when the app is deployed on a server
pip install -r requirements.txt
export FLASK_ENV=production
export APP_SETTINGS=groundstation.config.ProductionConfig
cd groundstation/static
npm install
npm run build
cd ../..
# python3 manage.py recreate_db
# python3 manage.py seed_db

gunicorn -b 0.0.0.0:5000 manage:app
