#!/bin/bash
source ./env.sh
export PYTHONPATH=.
export LD_LIBRARY_PATH=libcsp/build
# Use the "nohup" command in production on the real server.
# eg. nohup python3 ./satellite_simulator/sat_server.py &
# ps ax | grep sat_server.py
# --------------------
# On real server, replace interface with correct satellite one
python3 ./comm.py -I dummy &
ps ax | grep comm.py

echo Type 'kill PID' to kill server/comm process after
