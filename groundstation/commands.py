# These classes go with the ground station API.


# Every command will extend this. It contains a basic initialization and functions 
# to get and set names and data as well as return the command in a tuple of the 
# form (command type, [relevant data]) 
# At the moment, most of these are stubs as we don't know the actual formatting
class Command:

    def __init__ (self, name):
        self.name = name    # TODO: What is this for?
        self.type = 'NONE'
        self.data = []

    def getTuple(self):
        return (self.type, self.data) # Get the final tuple

    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data

# This is the class for pinging the satellite. The data for this will be [ping id, timoeout, size]
# TODO: consider having unique ping IDs. This might be handled in the api instead
class Ping(Command):

    def __init__(self, name, timeout, size):
        self.name = name    # "id" is a keyword apparently
        self.type = 'PING'
        self.timeout = timeout
        self.size = size
        self.data = [name, timeout, size]


# This is the simplest command, just sending the hk type with no data necessary
class GetHK(Command):

    def __init__(self, name):
        self.name = name
        self.type = 'GET-HK'
        self.data = []

    def setHK(self, hk_file):
        self.hk_file = hk_file

    def processData(self):
        #TODO read self.data and process relevant info 
        pass

class PetTimers(Command):

    # timers will be an array with the name or identity of the timers that need to be pet
    def __init__(self, name, timers):
        self.name = name
        self.type = 'PET-TIMERS'
        self.data = timers


# class TurnOn(command):

#   self.type = 'TURN-ON'

#   def __init__(self, name, ID):
#       self.name = name
#       self.id = ID
#       self.data = [ID]

#   def getID(self):
#       return self.id

#   def setID(self, ID):
#       self.id = ID
#       self.data = [self.id]


# class TurnOff(Command):

#   self.type = 'TURN-OFF'

#   def __init__(self, name, ID):
#       self.name = name
#       self.id = ID
#       self.data = [ID]

#   def getID(self):
#       return self.id

#   def setID(self, ID):
#       self.id = ID
#       self.data = [self.id]


# Have a On/Off Toggle instead?
class TogglePart(Command):

    def __init__(self, name, ID):
        self.name = name
        self.type = 'TURN-OFF'
        self.id = ID
        self.data = [ID]

    def getID(self):
        return self.id

    def setID(self, ID):
        self.id = ID
        self.data = [self.id]

    def turnOn(self):
        return ('TURN-ON', self.data)

    def turnOff(self):
        return ('TURN-OFF', self.data)


class Magnetometer(Command):

    def __init__(self, name, time):
        self.name = name
        self.type = "MAGNETOMETER"
        self.time = time
        self.data = [self.time]


class Imaging(Command):

    def __init__(self, name, time):
        self.name = name
        self.type = "IMAGE"
        self.time = time
        self.data = [self.time]


