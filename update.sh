#!/bin/sh
pip install -r requirements.txt
source env.sh
python3 manage.py recreate_db
python3 manage.py seed_db
cd groundstation/static
npm install
npm run build
cd ../..
