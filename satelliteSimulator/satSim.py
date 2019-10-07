import datetime

class SatelliteState:

    sat_modes = ['DORMANT', 'ACTIVE', 'SLEEPING']

    def __init__(self, satelliteMode=sat_modes[0], batteryVoltage=4,
        currentIn=0.3, currentOut=0.3, noMCUResets=0,
        lastBeaconTime=datetime.datetime.utcnow()):

        self.satelliteMode = satelliteMode
        self.batteryVoltage = batteryVoltage
        self.currentIn = currentIn
        self.currentOut = currentOut
        self.noMCUResets = noMCUResets
        self.lastBeaconTime = lastBeaconTime

    def set_random_state(self):
        pass



class Satellite:

    def __init__(self):
        self.state = SatelliteState()

    def send(self, data):
        pass
