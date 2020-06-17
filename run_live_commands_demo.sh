#!/bin/bash
source ./env.sh
export PYTHONPATH=.
export LD_LIBRARY_PATH=libcsp/build
# use the "nohup" command in production on the real server
# eg. nohup python3 ./satellite_simulator/sat_server.py &
# ps ax | grep sat_server.py
python3 ./comm.py &
ps ax | grep comm.py

echo Type 'kill PID' to kill server/comm process after
