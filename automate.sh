#!/bin/sh
export PYTHONPATH=.
python3 ./satellite_simulator/sat_server.py &
python3 ./comm.py &
sleep 1
python3 automation.py
