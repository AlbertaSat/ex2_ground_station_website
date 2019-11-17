#!/bin/sh
export PYTHONPATH=.
nohup python3 ./satellite_simulator/sat_server.py &
nohup python3 ./comm.py &
python3 automation.py
