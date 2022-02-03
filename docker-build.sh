#!/bin/bash
docker build -f user.Dockerfile --tag albertasatdocker/ground-station-website:user-latest .
docker build -f dev.Dockerfile --tag albertasatdocker/ground-station-website:dev-latest .
