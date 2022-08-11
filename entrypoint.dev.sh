#!/bin/bash

# Setup autoformat hook
git config core.hooksPath .git-hooks/hooks/

pip install -r requirements.txt
source ./env.sh
source ./keys.sh
python3 manage.py recreate_db
python3 manage.py seed_db_example
exec "$@"
