from groundstation import db

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(128))

	def __init__(self, username):
		self.username = username

	def toJson(self):
		return {
			'id' : self.id,
			'username': self.username
		}

class SatelliteModel(db.Model):
	__tablename__ = 'satellite_model'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	satelliteMode = db.Column(db.String(32))
	batteryVoltage = db.Column(db.Float)
	currentIn = db.Column(db.Float)
	currentOut = db.Column(db.Float)
	noMCUResets = db.Column(db.Integer)
	lastBeaconTime = db.Column(db.DateTime)



