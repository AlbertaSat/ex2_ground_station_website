#!/bin/sh
echo "Setting Flask environment variables..."
export FLASK_APP=groundstation/__init__.py
export FLASK_ENV=development
export APP_SETTINGS=groundstation.config.DevelopmentConfig
export LD_LIBRARY_PATH="libcsp/build"
export PYTHONPATH="."
