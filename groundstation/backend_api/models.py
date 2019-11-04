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
    satellite_mode = db.Column(db.String(32))
    battery_voltage = db.Column(db.Float)
    current_in = db.Column(db.Float)
    current_out = db.Column(db.Float)
    no_MCU_resets = db.Column(db.Integer)
    last_beacon_time = db.Column(db.DateTime, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'satellite_mode': self.satellite_mode,
            'battery_voltage': self.battery_voltage,
            'current_in': self.current_in,
            'current_out': self.current_out,
            'no_MCU_resets': self.no_MCU_resets,
            'last_beacon_time': str(self.last_beacon_time)
        }

class Telecommands(db.Model):
    __tablename__ = 'telecommands'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    command_name = db.Column(db.String(64))
    num_arguments = db.Column(db.Integer)
    flightschedulecommands = db.relationship('FlightScheduleCommands', backref='command', lazy=True)
    is_dangerous = db.Column(db.Boolean)


    def to_json(self):
        return {
            'command_id': self.id,
            'command_name': self.command_name,
            'num_arguments': self.num_arguments,
            'is_dangerous': self.is_dangerous
        }

class FlightSchedules(db.Model):
    __tablename__ = 'flightschedules'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    upload_date = db.Column(db.DateTime)
    is_queued = db.Column(db.Boolean, default=False)
    commands = db.relationship('FlightScheduleCommands', backref='flightschedule', lazy=True, cascade='all')

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

class Passover(db.Model):
    __tablename__ = 'passovers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime)

    def to_json(self):
        return {
            'passover_id': self.id,
            'timestamp': str(self.timestamp)
        }
