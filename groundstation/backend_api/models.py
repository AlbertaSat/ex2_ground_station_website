from datetime import datetime
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

class Housekeeping(db.Model):
    __tablename__ = 'housekeeping'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    satellite_Mode = db.Column(db.String(32))
    battery_Voltage = db.Column(db.Float)
    current_In = db.Column(db.Float)
    current_Out = db.Column(db.Float)
    no_MCU_Resets = db.Column(db.Integer)
    last_Beacon_Time = db.Column(db.DateTime, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'satelliteMode': self.satellite_Mode,
            'batteryVoltage': self.battery_Voltage,
            'currentIn': self.current_In,
            'currentOut': self.current_Out,
            'noMCUResets': self.no_MCU_Resets,
            'lastBeaconTime': str(self.last_Beacon_Time)
        }

class Telecommands(db.Model):
    __tablename__ = 'telecommands'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    command_name = db.Column(db.String(64))
    num_arguments = db.Column(db.Integer)
    flightschedulecommands = db.relationship('FlightScheduleCommands', backref='command', lazy=True)


    def to_json(self):
        return {
            'command_name': self.command_name,
            'num_arguments': self.num_arguments
        }

class FlightSchedules(db.Model):
    __tablename__ = 'flightschedules'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    upload_date = db.Column(db.DateTime)
    is_queued = db.Column(db.Boolean, default=False)
    commands = db.relationship('FlightScheduleCommands', backref='flightschedule', lazy=True)

    def to_json(self):
        return {
            'flightschedule_id': self.id,
            'creation_date': str(self.creation_date),
            'upload_date': str(self.upload_date),
            'is_queued':str(self.is_queued),
            'commands': [command.to_json() for command in self.commands]
        }

class FlightScheduleCommands(db.Model):
    __tablename__ = 'flightschedulecommands'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    command_id = db.Column(db.Integer, db.ForeignKey('telecommands.id'), nullable=False)
    timestamp = db.Column(db.DateTime)
    flightschedule_id = db.Column(db.Integer, db.ForeignKey('flightschedules.id'), nullable=False)

    def to_json(self):
        return {
            'flightschedule_command_id': self.id,
            'timestamp': str(self.timestamp),
            'command': self.command.to_json()
        }
