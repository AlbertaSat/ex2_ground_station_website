import socket

import time
import json
from datetime import datetime
from groundstation.satellite_simulator.sat_sim import Environment, Satellite, SatelliteComponent, Simulator
from groundstation.backend_api.housekeeping import HousekeepingLogList
from groundstation.tests.utils import fakeHousekeepingAsDict

environment = Environment(connection_strength=7, connection_stability=7, packet_drop_probability=0.05)
def effect_of_gps_on(old_value):
    new_value = old_value - 0.01
    return new_value
satellite_components = [SatelliteComponent('gps', [('battery_voltage', effect_of_gps_on)], []),]
satellite = Satellite(satellite_components, 'Passive', 16, 0.3, 0.3, 0, int(time.time()))
simulator = Simulator(environment, satellite)
del environment, satellite

HOST = '127.0.0.1'
PORT = 65432
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                data = data.decode('utf-8')
                data = data.split()
                data = (data[0], data[1:])
                try:
                    resp = simulator.send_to_sat(data)
                    simulator.step()
                except Exception as e:
                    resp = f'EXCEPTION RAISED IN sat_server.py: {repr(e)}'
                conn.sendall(bytes(resp, 'utf-8'))
