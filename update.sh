#!/bin/sh
pip install -r requirements.txt
export APP_SETTINGS=groundstation.config.DevelopmentConfig
python3 manage.py recreate_db
python3 manage.py seed_db
cd groundstation/static
npm install
npm run build
