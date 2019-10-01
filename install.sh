#!/bin/sh
pip install -r requirements.txt
export APP_SETTINGS=groundstation.config.DevelopmentConfig
cd groundstation/static
npm install
npm i react react-dom --save-dev