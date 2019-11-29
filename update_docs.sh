#!/bin/sh
cd docs
pip install -r requirements.txt
make html
cp -r build/html/* .
echo "Copied the built html to /docs"
cd ..