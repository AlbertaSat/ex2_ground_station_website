#!/bin/sh
# This script is for the entrypoint when the app is deployed on a server
pip install -r requirements.txt
export FLASK_APP=groundstation/__init__.py
export FLASK_ENV=production
export APP_SETTINGS=groundstation.config.ProductionConfig
cd groundstation/static
npm install
npm run build
cd ../..
flask db upgrade
gunicorn -b 0.0.0.0:5000 --workers=3 --threads=3 manage:app
