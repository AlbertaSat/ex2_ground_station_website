#!/bin/bash

# Setup autoformat hook
git config core.hooksPath .git-hooks/hooks/

# Update pip and install python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment variables
source ./env.sh
source ./keys.sh

# Setup example database
python3 manage.py recreate_db
python3 manage.py seed_db_example

exec "$@"
