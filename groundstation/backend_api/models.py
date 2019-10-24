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
    satelliteMode = db.Column(db.String(32))
    batteryVoltage = db.Column(db.Float)
    currentIn = db.Column(db.Float)
    currentOut = db.Column(db.Float)
    noMCUResets = db.Column(db.Integer)
    lastBeaconTime = db.Column(db.DateTime, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'satelliteMode': self.satelliteMode,
            'batteryVoltage': self.batteryVoltage,
            'currentIn': self.currentIn,
            'currentOut': self.currentOut,
            'noMCUResets': self.noMCUResets,
            'lastBeaconTime': str(self.lastBeaconTime)
        }

class Commands(db.Model):
    __tablename__ = 'commands'

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
    creation_date = db.Column(db.DateTime)
    upload_date = db.Column(db.DateTime)
    commands = db.relationship('FlightScheduleCommands', backref='flightschedule', lazy=True)

    def to_json(self):
        return {
            'flightschedule_id': self.id,
            'creation_date': str(self.creation_date),
            'upload_date': str(self.upload_date),
            'commands': [command.to_json() for command in self.commands]
        }

class FlightScheduleCommands(db.Model):
    __tablename__ = 'flightschedulecommands'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    command_id = db.Column(db.Integer, db.ForeignKey('commands.id'), nullable=False)
    timestamp = db.Column(db.DateTime)
    flightschedule_id = db.Column(db.Integer, db.ForeignKey('flightschedules.id'), nullable=False)

    def to_json(self):
        return {
            'flightschedule_command_id': self.id,
            'timestamp': str(self.timestamp),
            'command': self.command.to_json()
        }
