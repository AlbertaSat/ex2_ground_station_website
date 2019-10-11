#Every command will extend this. It contains a basic initialization and functions 
#to get and set names and data as well as return the command in a tuple of the 
#form [command type, [relevant data]] 
#At the moment, most of these are stubs as we don't know the actual formatting
class Command:

	self.data = []
	self.type = 'NONE'

	def __init__ (self, name):
		self.name = name

	#Get the formatting for send function
	def getCommand(self):
		return (self.type, self.data)

	def getData(self):
		return self.data

	def setData(self, data):
		self.data = data

#This is the class for pinging the satellite. The data for this will be [ping id, timoeout, size]
#TODO: consider having unique ping IDs. This might be handled in the api instead
class Ping(Command):

	self.type = 'PING'

	def __init__(self, name, timeout, size):

		self.name = name
		self.timeout = timeout
		self.size = size
		self.data = [name, timeout, size]


#This is the simplest command, just sending the hk type with no data necessary
class GetHK(Command):

	self.type = 'GET-HK'
	self.data = []


	# def __init__(self, name):
	# 	self.name = name

	def setHK(self, hk_file):
		self.hk_file = hk_file

	def processData(self):
		#TODO read self.data and process relevant info 
		pass

class PetTimers(Command):

	self.type = 'PET-TIMERS'

	#timers will be an array with the name or identity of the timers that need to be pet
	def __init__(self, name, timers):
		self.name = name
		self.data = timers

# class TurnOn(command):

# 	self.type = 'TURN-ON'

# 	def __init__(self, name, ID):
# 		self.name = name
# 		self.id = ID
# 		self.data = [ID]

# 	def getID(self):
# 		return self.id

# 	def setID(self, ID):
# 		self.id = ID
# 		self.data = [self.id]



# class TurnOff(Command):

# 	self.type = 'TURN-OFF'

# 	def __init__(self, name, ID):
# 		self.name = name
# 		self.id = ID
# 		self.data = [ID]

# 	def getID(self):
# 		return self.id

# 	def setID(self, ID):
# 		self.id = ID
# 		self.data = [self.id]

#a proposition for an alternate to both turn on/off
class TogglePart(Command):

	self.type = 'TURN-OFF'

		def __init__(self, name, ID):
		self.name = name
		self.id = ID
		self.data = [ID]

	def getID(self):
		return self.id

	def setID(self, ID):
		self.id = ID
		self.data = [self.id]


	def turn-On(self):
		return ('TURN-ON', self.data)

	def turn-off(self):
		return ('TURN-OFF', self.data)

class Magnetometer(Command):
	self.type = "MAGNETOMETER"

	def __init__(self, name, time):
		self.name = name
		self.time = time
		self.data = [self.time]

class Imaging(Command):
	self.type = "Imaging"

	def __init__(self, name, time):
		self.name = name
		self.time = time
		self.data = [self.time]


