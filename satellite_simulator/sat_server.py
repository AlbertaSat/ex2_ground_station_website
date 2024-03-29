"""This file uses the Classes defined in sat_sim.py to simulate a satellite in a controlled environment. At the same time,
it opens a port and lisens for a client to send commands to the satellite. All commands recieved are then parsed and then
passed onto the satellite which attempts to respond.
"""

import socket

import time
import json
from datetime import datetime
from satellite_simulator.sat_sim import Environment, Satellite, SatelliteComponent, Simulator
import signal

def handler(signum, frame):
    exit()

environment = Environment(connection_strength=10, connection_stability=10,
    packet_drop_probability=0)

volt_effect = lambda old_value, time_delta : old_value - (0.01 * time_delta)
temp_effect = lambda old_value, time_delta : [el + (0.01 * time_delta) for el in old_value]
wdog_effect = lambda old_value, time_delta : [el - time_delta for el in old_value]
satellite_components = [
    SatelliteComponent('GPS', 0,
        effects_when_on=[('battery_voltage', volt_effect), ('temps', temp_effect)],
        effects_when_off=[]),
    SatelliteComponent('WATCHDOG_TIMERS', 1,
        effects_when_on=[('watchdogs', wdog_effect)],
        effects_when_off=[])
]
satellite = Satellite(satellite_components)
satellite._turn_on_channel(1)
simulator = Simulator(environment, satellite)
del environment, satellite

signal.signal(signal.SIGALRM, handler)
signal.alarm(60 * 60)

HOST = '127.0.0.1'
PORT = 65432
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected with', addr)
            while True:
                data = conn.recv(1024)
                if data != b'':
                    print('Received:', data)
                if not data:
                    break
                data = json.loads(data.decode('utf-8'))
                is_fs = not isinstance(data, str)
                if not is_fs:
                    data = data.strip().split('.')
                    data = (data[0], data[1:])
                try:
                    if is_fs:
                        resp = simulator.upload_fs_to_sat(data)
                    else:
                        resp = simulator.send_to_sat(data)
                except Exception as e:
                    resp = f'EXCEPTION RAISED IN sat_server.py: {repr(e)}'
                if resp is not None:
                    print('Response:', resp)
                conn.sendall(bytes(json.dumps(resp), 'utf-8'))
