#!/bin/bash
# This script is for the entrypoint when the app is deployed on a server

# Update pip and install python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment variables
export FLASK_APP=groundstation/__init__.py
export FLASK_ENV=production
export APP_SETTINGS=groundstation.config.ProductionConfig
source ./keys.sh

# Build frontend
cd groundstation/static
npm install
npm run build
cd ../..

# Upgrade database schema
flask db upgrade

# Run web app
gunicorn -b 0.0.0.0:5000 --workers=3 --threads=3 manage:app
