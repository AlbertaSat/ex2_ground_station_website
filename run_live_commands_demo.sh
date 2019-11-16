source env.sh
export PYTHONPATH=.
nohup python3 ./satellite_simulator/sat_server.py &
ps ax | grep sat_server.py
nohup python3 ./comm.py &
ps ax | grep comm.py


echo Type 'kill PID' to kill server/comm process after
