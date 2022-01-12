#!/bin/bash
docker build -f user.Dockerfile --tag albertasat/ground-station-website:user-latest .
docker build -f dev.Dockerfile --tag albertasat/ground-station-website:dev-latest .
