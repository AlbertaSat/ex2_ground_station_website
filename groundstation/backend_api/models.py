from flask import current_app
import datetime
import jwt
from groundstation import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, username, password, is_admin=False):
        self.username = username
        num_rounds = current_app.config.get('BCRYPT_LOG_ROUNDS')
        self.password_hash = bcrypt.generate_password_hash(password, num_rounds).decode()
        self.is_admin = is_admin

    def verify_password(self, password):
        """Returns True if passes password is valid, else False

        :param str password: The password to validate

        :returns: True if password is valid
        :rtype: bool
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    def encode_auth_token_by_id(self):
        """Generates the auth token"""
        try:
            payload = {
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')),
                'iat': datetime.datetime.now(datetime.timezone.utc),
                'sub': self.id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """Decodes the auth token

        :param auth_token: The authorization token

        :returns: user_id (int)
        """
        payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
        user_id = payload['sub']
        return user_id

    def to_json(self):
        """Returns a dictionary of some selected model attributes
        """
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

    watchdog_1 = db.Column(db.Integer) # 3 watchdogs
    watchdog_2 = db.Column(db.Integer)
    watchdog_3 = db.Column(db.Integer)
    panel_1_current = db.Column(db.Float) # 6 solar panel currents
    panel_2_current = db.Column(db.Float)
    panel_3_current = db.Column(db.Float)
    panel_4_current = db.Column(db.Float)
    panel_5_current = db.Column(db.Float)
    panel_6_current = db.Column(db.Float)
    temp_1 = db.Column(db.Float) # 6 temperatures at diff locations
    temp_2 = db.Column(db.Float)
    temp_3 = db.Column(db.Float)
    temp_4 = db.Column(db.Float)
    temp_5 = db.Column(db.Float)
    temp_6 = db.Column(db.Float)
    # Power channels (probably 24 exactly in a HK log)
    channels = db.relationship('PowerChannels', backref='housekeeping', lazy=True, cascade='all')

    def to_json(self):
        """Returns a dictionary of some selected model attributes
        """
        return {
            'id': self.id,
            'satellite_mode': self.satellite_mode,
            'battery_voltage': self.battery_voltage,
            'current_in': self.current_in,
            'current_out': self.current_out,
            'no_MCU_resets': self.no_MCU_resets,
            'last_beacon_time': str(self.last_beacon_time),

            'watchdog_1': self.watchdog_1,
            'watchdog_2': self.watchdog_2,
            'watchdog_3': self.watchdog_3,
            'panel_1_current': self.panel_1_current,
            'panel_2_current': self.panel_2_current,
            'panel_3_current': self.panel_3_current,
            'panel_4_current': self.panel_4_current,
            'panel_5_current': self.panel_5_current,
            'panel_6_current': self.panel_6_current,
            'temp_1': self.temp_1,
            'temp_2': self.temp_2,
            'temp_3': self.temp_3,
            'temp_4': self.temp_4,
            'temp_5': self.temp_5,
            'temp_6': self.temp_6,

            'channels': [channel.to_json() for channel in self.channels]
        }

class PowerChannels(db.Model):
    __tablename__ = 'powerchannels'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hk_id = db.Column(db.Integer, db.ForeignKey('housekeeping.id'), nullable=False)
    channel_no = db.Column(db.Integer) # Range of 1-24
    enabled = db.Column(db.Boolean)
    current = db.Column(db.Float)
    # Might also need a 'Nominal' column? According to ASAT Common Commands doc.

    def to_json(self):
        """Returns a dictionary of some selected model attributes
        """
        return {
            'id': self.id,
            'hk_id': self.hk_id,
            'channel_no': self.channel_no,
            'enabled': self.enabled,
            'current': self.current
        }

class Telecommands(db.Model):
    __tablename__ = 'telecommands'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    command_name = db.Column(db.String(64))
    num_arguments = db.Column(db.Integer)
    flightschedulecommands = db.relationship('FlightScheduleCommands', backref='command', lazy=True)
    is_dangerous = db.Column(db.Boolean)

    def to_json(self):
        """Returns a dictionary of some selected model attributes
        """
        return {
            'command_id': self.id,
            'command_name': self.command_name,
            'num_arguments': self.num_arguments,
            'is_dangerous': self.is_dangerous
        }

class FlightSchedules(db.Model):
    __tablename__ = 'flightschedules'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    upload_date = db.Column(db.DateTime)
    execution_time = db.Column(db.DateTime)
    # status is an integer, where 1=queued, 2=draft, 3=uploaded
    status = db.Column(db.Integer)
    commands = db.relationship('FlightScheduleCommands', backref='flightschedule', lazy=True, cascade='all')

    def to_json(self):
        """Returns a dictionary of some selected model attributes
        """
        return {
            'flightschedule_id': self.id,
            'creation_date': str(self.creation_date),
            'upload_date': str(self.upload_date),
            'status': self.status,
            'execution_time': self.execution_time.isoformat(),
            'commands': [command.to_json() for command in self.commands]
        }

class FlightScheduleCommands(db.Model):
    __tablename__ = 'flightschedulecommands'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    command_id = db.Column(db.Integer, db.ForeignKey('telecommands.id'), nullable=False)
    timestamp = db.Column(db.DateTime)
    flightschedule_id = db.Column(db.Integer, db.ForeignKey('flightschedules.id'), nullable=False)
    arguments = db.relationship('FlightScheduleCommandsArgs',
                                backref='flightschedulecommand',
                                lazy=True,
                                cascade='all, delete-orphan'
                                )

    def to_json(self):
        """Returns a dictionary of some selected model attributes
        """
        return {
            'flightschedule_command_id': self.id,
            'timestamp': str(self.timestamp),
            'command': self.command.to_json(),
            'args': [arg.to_json() for arg in self.arguments]
        }

class FlightScheduleCommandsArgs(db.Model):
    __tablename__ = 'flightschedulecommandsargs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    index = db.Column(db.Integer)
    argument = db.Column(db.String(8))
    flightschedulecommand_id = db.Column(db.Integer, db.ForeignKey('flightschedulecommands.id'), nullable=False)

    def to_json(self):
        """Returns a dictionary of some selected model attributes
        """
        return {
            'index': self.index,
            'argument': self.argument
        }


class Passover(db.Model):
    __tablename__ = 'passovers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime)

    def to_json(self):
        """Returns a dictionary of some selected model attributes
        """
        return {
            'passover_id': self.id,
            'timestamp': str(self.timestamp)
        }

# This will be the table of telecommands being sent to the satellite as well as the responses
# the table will allow us to send and receive all commands transactionally allowing us to log
# them as well as their responses
# TODO: discuss with team the design/structure for the communications table
class Communications(db.Model):
    __tablename__ = 'communications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String, nullable=False)          # Every command is going to be formatted as a string for simplicity
    timestamp = db.Column(db.DateTime, nullable=False)      # Time at which the command was appended to the table
    sender = db.Column(db.String, nullable=False)           # who sent the command (comm/react/command) as a note, the comm can send commands as responses from the satellite
    receiver = db.Column(db.String, nullable=False)         # who the intended recipient of the command is (comm/react web page/command line)
    #response = db.Column(db.Integer, db.ForeignKey('communications.id')) # one possible value for connecting satellite responses to sent telecommands

    def to_json(self):
        """Returns a dictionary of some selected model attributes
        """
        return {
            'message_id': self.id,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'sender': self.sender,
            'receiver': self.receiver
        }
