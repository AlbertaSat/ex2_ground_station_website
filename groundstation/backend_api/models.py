from flask import current_app
import datetime
import jwt
from groundstation import db, bcrypt
from sqlalchemy.sql import func
from sqlalchemy.orm import backref


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, server_default='0', nullable=False)
    slack_id = db.Column(db.String(128), nullable=True, unique=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    subscribed_to_slack = db.Column(db.Boolean, server_default="0")
    blacklisted_tokens = db.relationship(
        'BlacklistedTokens', backref='user', lazy=True, cascade='all, delete-orphan')
    creator = db.relationship('User', remote_side=[id], lazy=True)

    def __init__(self, username, password, is_admin=False, slack_id=None, subscribed_to_slack=False, creator_id=None):
        self.username = username
        num_rounds = current_app.config.get('BCRYPT_LOG_ROUNDS')
        self.password_hash = bcrypt.generate_password_hash(
            password, num_rounds).decode()
        self.is_admin = is_admin
        self.slack_id = slack_id
        self.subscribed_to_slack = subscribed_to_slack
        self.creator_id = creator_id

    def regenerate_password_hash(self, password):
        num_rounds = current_app.config.get('BCRYPT_LOG_ROUNDS')
        self.password_hash = bcrypt.generate_password_hash(
            password, num_rounds).decode()

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
            print(e)
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
            'id': self.id,
            'username': self.username,
            'is_admin': self.is_admin,
            'slack_id': self.slack_id,
            'creator_id': self.creator_id,
            'subscribed_to_slack': self.subscribed_to_slack
        }


class BlacklistedTokens(db.Model):
    __tablename__ = 'blacklistedtokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Telecommands(db.Model):
    __tablename__ = 'telecommands'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    command_name = db.Column(db.String(64))
    num_arguments = db.Column(db.Integer)
    flightschedulecommands = db.relationship(
        'FlightScheduleCommands', backref='command', lazy=True)
    automatedcommands = db.relationship(
        'AutomatedCommands', backref='command', lazy=True)
    is_dangerous = db.Column(db.Boolean)
    about_info = db.Column(db.String(256))
    arg_labels = db.Column(db.String(400))
    return_labels = db.Column(db.String(7000))

    def to_json(self):
        """Returns a dictionary of some selected model attributes
        """
        return {
            'command_id': self.id,
            'command_name': self.command_name,
            'num_arguments': self.num_arguments,
            'is_dangerous': self.is_dangerous,
            'about_info': self.about_info,
            'arg_labels': self.arg_labels,
            'return_labels': self.return_labels
        }


class FlightSchedules(db.Model):
    __tablename__ = 'flightschedules'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creation_date = db.Column(db.DateTime, server_default=func.now())
    upload_date = db.Column(db.DateTime)
    execution_time = db.Column(db.DateTime)
    # status is an integer, where 1=queued, 2=draft, 3=uploaded
    status = db.Column(db.Integer)
    error = db.Column(db.Integer, nullable=False, server_default='0')
    commands = db.relationship(
        'FlightScheduleCommands', backref='flightschedule', lazy=True, cascade='all')

    def to_json(self):
        """Returns a dictionary of some selected model attributes
        """
        return {
            'flightschedule_id': self.id,
            'creation_date': str(self.creation_date),
            'upload_date': str(self.upload_date),
            'status': self.status,
            'error': self.error,
            'execution_time': self.execution_time.isoformat(),
            'commands': [command.to_json() for command in self.commands]
        }


class FlightScheduleCommands(db.Model):
    __tablename__ = 'flightschedulecommands'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    command_id = db.Column(db.Integer, db.ForeignKey(
        'telecommands.id'), nullable=False)
    timestamp = db.Column(db.DateTime)
    repeat_ms = db.Column(db.Boolean, default=False, nullable=False)
    repeat_sec = db.Column(db.Boolean, default=False, nullable=False)
    repeat_min = db.Column(db.Boolean, default=False, nullable=False)
    repeat_hr = db.Column(db.Boolean, default=False, nullable=False)
    repeat_day = db.Column(db.Boolean, default=False, nullable=False)
    repeat_month = db.Column(db.Boolean, default=False, nullable=False)
    repeat_year = db.Column(db.Boolean, default=False, nullable=False)
    flightschedule_id = db.Column(db.Integer, db.ForeignKey(
        'flightschedules.id'), nullable=False)
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
            'repeats': {
                'repeat_ms': self.repeat_ms,
                'repeat_sec': self.repeat_sec,
                'repeat_min': self.repeat_min,
                'repeat_hr': self.repeat_hr,
                'repeat_day': self.repeat_day,
                'repeat_month': self.repeat_month,
                'repeat_year': self.repeat_year,
            },
            'command': self.command.to_json(),
            'args': [arg.to_json() for arg in self.arguments],
        }


class FlightScheduleCommandsArgs(db.Model):
    __tablename__ = 'flightschedulecommandsargs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    index = db.Column(db.Integer)
    argument = db.Column(db.String(8))
    flightschedulecommand_id = db.Column(db.Integer, db.ForeignKey(
        'flightschedulecommands.id'), nullable=False)

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
    aos_timestamp = db.Column(db.DateTime)
    los_timestamp = db.Column(db.DateTime)

    def to_json(self):
        """Returns a dictionary of some selected model attributes
        """
        return {
            'passover_id': self.id,
            'aos_timestamp': str(self.aos_timestamp),
            'los_timestamp': str(self.los_timestamp)
        }

# This will be the table of telecommands being sent to the satellite as well as the responses
# the table will allow us to send and receive all commands transactionally allowing us to log
# them as well as their responses


class Communications(db.Model):
    __tablename__ = 'communications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # every command is going to be formatted as a string for simplicity
    message = db.Column(db.String, nullable=False)
    # time at which the command was appended to the table
    timestamp = db.Column(db.DateTime, nullable=False)
    # who sent the command (comm/react/command) as a note, the comm can send commands as responses from the satellite
    sender = db.Column(db.String, nullable=False)
    # who the intended recipient of the command is (comm/react web page/command line)
    receiver = db.Column(db.String, nullable=False)
    # whether the command is queued to be sent to the satellite or not
    is_queued = db.Column(db.Boolean, server_default="0", nullable=False)

    # TODO: connecting satellite responses to sent telecommands
    #response = db.Column(db.Integer, db.ForeignKey('communications.id'))

    def to_json(self):
        """Returns a dictionary of some selected model attributes
        """
        return {
            'message_id': self.id,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'sender': self.sender,
            'receiver': self.receiver,
            'is_queued': self.is_queued
        }


class AutomatedCommands(db.Model):
    __tablename__ = 'automatedcommands'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    command_id = db.Column(db.Integer, db.ForeignKey(
        'telecommands.id'), nullable=False)
    priority = db.Column(db.Integer)
    arguments = db.relationship(
        'AutomatedCommandsArgs', backref='automatedcommand', lazy=True, cascade='all, delete-orphan')

    def to_json(self):
        """Returns a dictionary of some selected model attributes
        """
        return {
            'automatedcommand_id': self.id,
            'command': self.command.to_json(),
            'priority': self.priority,
            'args': [arg.to_json() for arg in self.arguments]
        }


class AutomatedCommandsArgs(db.Model):
    __tablename__ = 'automatedcommandsargs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    index = db.Column(db.Integer)
    argument = db.Column(db.String(8))
    automatedcommand_id = db.Column(db.Integer, db.ForeignKey(
        'automatedcommands.id'), nullable=False)

    def to_json(self):
        """Returns a dictionary of some selected model attributes
        """
        return {
            'index': self.index,
            'argument': self.argument
        }

############################################################
# Housekeeping Models
# ----------------------------------------------------------
# Each subsystem is seperated into its own table, all linked
# together through a main housekeeping table
############################################################


class Housekeeping(db.Model):
    __tablename__ = 'housekeeping'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    data_position = db.Column(db.Integer, nullable=False)
    tle = db.Column(db.String(256))

    def to_json(self):
        """Returns a dictionary of HK data, sectioned off by subsystem
        """
        return {
            'id': self.id,
            'timestamp': str(self.timestamp),
            'data_position': self.data_position,
            'tle': self.tle,
            'adcs': self.adcs.to_json(),
            'athena': self.athena.to_json(),
            'eps': self.eps.to_json(),
            'eps_startup': self.eps_startup.to_json(),
            'uhf': self.uhf.to_json(),
            'sband': self.sband.to_json(),
            'hyperion': self.hyperion.to_json(),
            'charon': self.charon.to_json(),
            'dfgm': self.dfgm.to_json(),
            'northern_spirit': self.northern_spirit.to_json(),
            'iris': self.iris.to_json()
        }


class AdcsHK(db.Model):
    __tablename__ = 'adcs_hk'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hk_id = db.Column(db.Integer, db.ForeignKey('housekeeping.id'))
    hk = db.relationship(
        'Housekeeping', backref=backref('adcs', uselist=False))

    Att_Estimate_Mode = db.Column(db.Integer)
    Att_Control_Mode = db.Column(db.Integer)
    Run_Mode = db.Column(db.Integer)
    Flags_arr = db.Column(db.Integer)
    Longitude = db.Column(db.Float)
    Latitude = db.Column(db.Float)
    Altitude = db.Column(db.Float)
    Estimated_Angular_Rate_X = db.Column(db.Float)
    Estimated_Angular_Rate_Y = db.Column(db.Float)
    Estimated_Angular_Rate_Z = db.Column(db.Float)
    Estimated_Angular_Angle_X = db.Column(db.Float)
    Estimated_Angular_Angle_Y = db.Column(db.Float)
    Estimated_Angular_Angle_Z = db.Column(db.Float)
    Sat_Position_ECI_X = db.Column(db.Float)
    Sat_Position_ECI_Y = db.Column(db.Float)
    Sat_Position_ECI_Z = db.Column(db.Float)
    Sat_Velocity_ECI_X = db.Column(db.Float)
    Sat_Velocity_ECI_Y = db.Column(db.Float)
    Sat_Velocity_ECI_Z = db.Column(db.Float)
    Sat_Position_LLH_X = db.Column(db.Float)
    Sat_Position_LLH_Y = db.Column(db.Float)
    Sat_Position_LLH_Z = db.Column(db.Float)
    ECEF_Position_X = db.Column(db.Integer)
    ECEF_Position_Y = db.Column(db.Integer)
    ECEF_Position_Z = db.Column(db.Integer)
    Coarse_Sun_Vector_X = db.Column(db.Float)
    Coarse_Sun_Vector_Y = db.Column(db.Float)
    Coarse_Sun_Vector_Z = db.Column(db.Float)
    Fine_Sun_Vector_X = db.Column(db.Float)
    Fine_Sun_Vector_Y = db.Column(db.Float)
    Fine_Sun_Vector_Z = db.Column(db.Float)
    Nadir_Vector_X = db.Column(db.Float)
    Nadir_Vector_Y = db.Column(db.Float)
    Nadir_Vector_Z = db.Column(db.Float)
    Wheel_Speed_X = db.Column(db.Float)
    Wheel_Speed_Y = db.Column(db.Float)
    Wheel_Speed_Z = db.Column(db.Float)
    Mag_Field_Vector_X = db.Column(db.Float)
    Mag_Field_Vector_Y = db.Column(db.Float)
    Mag_Field_Vector_Z = db.Column(db.Float)
    TC_num = db.Column(db.Integer)
    TM_num = db.Column(db.Integer)
    CommsStat_flags_1 = db.Column(db.Integer)
    CommsStat_flags_2 = db.Column(db.Integer)
    CommsStat_flags_3 = db.Column(db.Integer)
    CommsStat_flags_4 = db.Column(db.Integer)
    CommsStat_flags_5 = db.Column(db.Integer)
    CommsStat_flags_6 = db.Column(db.Integer)
    Wheel1_Current = db.Column(db.Float)
    Wheel2_Current = db.Column(db.Float)
    Wheel3_Current = db.Column(db.Float)
    CubeSense1_Current = db.Column(db.Float)
    CubeSense2_Current = db.Column(db.Float)
    CubeControl_Current3v3 = db.Column(db.Float)
    CubeControl_Current5v0 = db.Column(db.Float)
    CubeStar_Current = db.Column(db.Float)
    CubeStar_Temp = db.Column(db.Float)
    Magnetorquer_Current = db.Column(db.Float)
    MCU_Temp = db.Column(db.Float)
    Rate_Sensor_Temp_X = db.Column(db.Integer)
    Rate_Sensor_Temp_Y = db.Column(db.Integer)
    Rate_Sensor_Temp_Z = db.Column(db.Integer)

    def to_json(self):
        return {
            'Att_Estimate_Mode': self.Att_Estimate_Mode,
            'Att_Control_Mode': self.Att_Control_Mode,
            'Run_Mode': self.Run_Mode,
            'Flags_arr': self.Flags_arr,
            'Longitude': self.Longitude,
            'Latitude': self.Latitude,
            'Altitude': self.Altitude,
            'Estimated_Angular_Rate_X': self.Estimated_Angular_Rate_X,
            'Estimated_Angular_Rate_Y': self.Estimated_Angular_Rate_Y,
            'Estimated_Angular_Rate_Z': self.Estimated_Angular_Rate_Z,
            'Estimated_Angular_Angle_X': self.Estimated_Angular_Angle_X,
            'Estimated_Angular_Angle_Y': self.Estimated_Angular_Angle_Y,
            'Estimated_Angular_Angle_Z': self.Estimated_Angular_Angle_Z,
            'Sat_Position_ECI_X': self.Sat_Position_ECI_X,
            'Sat_Position_ECI_Y': self.Sat_Position_ECI_Y,
            'Sat_Position_ECI_Z': self.Sat_Position_ECI_Z,
            'Sat_Velocity_ECI_X': self.Sat_Velocity_ECI_X,
            'Sat_Velocity_ECI_Y': self.Sat_Velocity_ECI_Y,
            'Sat_Velocity_ECI_Z': self.Sat_Velocity_ECI_Z,
            'Sat_Position_LLH_X': self.Sat_Position_LLH_X,
            'Sat_Position_LLH_Y': self.Sat_Position_LLH_Y,
            'Sat_Position_LLH_Z': self.Sat_Position_LLH_Z,
            'ECEF_Position_X': self.ECEF_Position_X,
            'ECEF_Position_Y': self.ECEF_Position_Y,
            'ECEF_Position_Z': self.ECEF_Position_Z,
            'Coarse_Sun_Vector_X': self.Coarse_Sun_Vector_X,
            'Coarse_Sun_Vector_Y': self.Coarse_Sun_Vector_Y,
            'Coarse_Sun_Vector_Z': self.Coarse_Sun_Vector_Z,
            'Fine_Sun_Vector_X': self.Fine_Sun_Vector_X,
            'Fine_Sun_Vector_Y': self.Fine_Sun_Vector_Y,
            'Fine_Sun_Vector_Z': self.Fine_Sun_Vector_Z,
            'Nadir_Vector_X': self.Nadir_Vector_X,
            'Nadir_Vector_Y': self.Nadir_Vector_Y,
            'Nadir_Vector_Z': self.Nadir_Vector_Z,
            'Wheel_Speed_X': self.Wheel_Speed_X,
            'Wheel_Speed_Y': self.Wheel_Speed_Y,
            'Wheel_Speed_Z': self.Wheel_Speed_Z,
            'Mag_Field_Vector_X': self.Mag_Field_Vector_X,
            'Mag_Field_Vector_Y': self.Mag_Field_Vector_Y,
            'Mag_Field_Vector_Z': self.Mag_Field_Vector_Z,
            'TC_num': self.TC_num,
            'TM_num': self.TM_num,
            'CommsStat_flags_1': self.CommsStat_flags_1,
            'CommsStat_flags_2': self.CommsStat_flags_2,
            'CommsStat_flags_3': self.CommsStat_flags_3,
            'CommsStat_flags_4': self.CommsStat_flags_4,
            'CommsStat_flags_5': self.CommsStat_flags_5,
            'CommsStat_flags_6': self.CommsStat_flags_6,
            'Wheel1_Current': self.Wheel1_Current,
            'Wheel2_Current': self.Wheel2_Current,
            'Wheel3_Current': self.Wheel3_Current,
            'CubeSense1_Current': self.CubeSense1_Current,
            'CubeSense2_Current': self.CubeSense2_Current,
            'CubeControl_Current3v3': self.CubeControl_Current3v3,
            'CubeControl_Current5v0': self.CubeControl_Current5v0,
            'CubeStar_Current': self.CubeStar_Current,
            'CubeStar_Temp': self.CubeStar_Temp,
            'Magnetorquer_Current': self.Magnetorquer_Current,
            'MCU_Temp': self.MCU_Temp,
            'Rate_Sensor_Temp_X': self.Rate_Sensor_Temp_X,
            'Rate_Sensor_Temp_Y': self.Rate_Sensor_Temp_Y,
            'Rate_Sensor_Temp_Z': self.Rate_Sensor_Temp_Z,
        }


class AthenaHK(db.Model):
    __tablename__ = 'athena_hk'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hk_id = db.Column(db.Integer, db.ForeignKey('housekeeping.id'))
    hk = db.relationship(
        'Housekeeping', backref=backref('athena', uselist=False))

    OBC_software_ver = db.Column(db.String)
    MCU_core_temp = db.Column(db.Integer)
    converter_temp = db.Column(db.Integer)
    OBC_uptime = db.Column(db.Integer)
    vol0_usage_percent = db.Column(db.Integer)
    vol1_usage_percent = db.Column(db.Integer)
    boot_cnt = db.Column(db.Integer)
    boot_src = db.Column(db.Integer)
    last_reset_reason = db.Column(db.Integer)
    OBC_mode = db.Column(db.Integer)
    solar_panel_supply_curr = db.Column(db.Integer)
    cmds_received = db.Column(db.Integer)
    pckts_uncovered_by_FEC = db.Column(db.Integer)

    def to_json(self):
        return {
            'OBC_software_ver': self.OBC_software_ver,
            'MCU_core_temp': self.MCU_core_temp,
            'converter_temp': self.converter_temp,
            'OBC_uptime': self.OBC_uptime,
            'vol0_usage_percent': self.vol0_usage_percent,
            'vol1_usage_percent': self.vol1_usage_percent,
            'boot_cnt': self.boot_cnt,
            'boot_src': self.boot_src,
            'last_reset_reason': self.last_reset_reason,
            'OBC_mode': self.OBC_mode,
            'solar_panel_supply_curr': self.solar_panel_supply_curr,
            'cmds_received': self.cmds_received,
            'pckts_uncovered_by_FEC': self.pckts_uncovered_by_FEC,
        }


class EpsHK(db.Model):
    __tablename__ = 'eps_hk'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hk_id = db.Column(db.Integer, db.ForeignKey('housekeeping.id'))
    hk = db.relationship('Housekeeping', backref=backref('eps', uselist=False))

    eps_cmd_hk = db.Column(db.Integer)
    eps_status_hk = db.Column(db.Integer)
    eps_timestamp_hk = db.Column(db.Float)
    eps_uptimeInS_hk = db.Column(db.Integer)
    eps_bootCnt_hk = db.Column(db.Integer)
    wdt_gs_time_left_s = db.Column(db.Integer)
    wdt_gs_counter = db.Column(db.Integer)
    mpptConverterVoltage1_mV = db.Column(db.Integer)
    mpptConverterVoltage2_mV = db.Column(db.Integer)
    mpptConverterVoltage3_mV = db.Column(db.Integer)
    mpptConverterVoltage4_mV = db.Column(db.Integer)
    curSolarPanels1_mA = db.Column(db.Integer)
    curSolarPanels2_mA = db.Column(db.Integer)
    curSolarPanels3_mA = db.Column(db.Integer)
    curSolarPanels4_mA = db.Column(db.Integer)
    curSolarPanels5_mA = db.Column(db.Integer)
    curSolarPanels6_mA = db.Column(db.Integer)
    curSolarPanels7_mA = db.Column(db.Integer)
    curSolarPanels8_mA = db.Column(db.Integer)
    vBatt_mV = db.Column(db.Integer)
    curSolar_mA = db.Column(db.Integer)
    curBattIn_mA = db.Column(db.Integer)
    curBattOut_mA = db.Column(db.Integer)
    curOutput1_mA = db.Column(db.Integer)
    curOutput2_mA = db.Column(db.Integer)
    curOutput3_mA = db.Column(db.Integer)
    curOutput4_mA = db.Column(db.Integer)
    curOutput5_mA = db.Column(db.Integer)
    curOutput6_mA = db.Column(db.Integer)
    curOutput7_mA = db.Column(db.Integer)
    curOutput8_mA = db.Column(db.Integer)
    curOutput9_mA = db.Column(db.Integer)
    curOutput10_mA = db.Column(db.Integer)
    curOutput11_mA = db.Column(db.Integer)
    curOutput12_mA = db.Column(db.Integer)
    curOutput13_mA = db.Column(db.Integer)
    curOutput14_mA = db.Column(db.Integer)
    curOutput15_mA = db.Column(db.Integer)
    curOutput16_mA = db.Column(db.Integer)
    curOutput17_mA = db.Column(db.Integer)
    curOutput18_mA = db.Column(db.Integer)
    AOcurOutput1_mA = db.Column(db.Integer)
    AOcurOutput2_mA = db.Column(db.Integer)
    outputConverterVoltage1 = db.Column(db.Integer)
    outputConverterVoltage2 = db.Column(db.Integer)
    outputConverterVoltage3 = db.Column(db.Integer)
    outputConverterVoltage4 = db.Column(db.Integer)
    outputConverterVoltage5 = db.Column(db.Integer)
    outputConverterVoltage6 = db.Column(db.Integer)
    outputConverterVoltage7 = db.Column(db.Integer)
    outputConverterVoltage8 = db.Column(db.Integer)
    outputConverterState = db.Column(db.Integer)
    outputStatus = db.Column(db.Integer)
    outputFaultStatus = db.Column(db.Integer)
    protectedOutputAccessCnt = db.Column(db.Integer)
    outputOnDelta1 = db.Column(db.Integer)
    outputOnDelta2 = db.Column(db.Integer)
    outputOnDelta3 = db.Column(db.Integer)
    outputOnDelta4 = db.Column(db.Integer)
    outputOnDelta5 = db.Column(db.Integer)
    outputOnDelta6 = db.Column(db.Integer)
    outputOnDelta7 = db.Column(db.Integer)
    outputOnDelta8 = db.Column(db.Integer)
    outputOnDelta9 = db.Column(db.Integer)
    outputOnDelta10 = db.Column(db.Integer)
    outputOnDelta11 = db.Column(db.Integer)
    outputOnDelta12 = db.Column(db.Integer)
    outputOnDelta13 = db.Column(db.Integer)
    outputOnDelta14 = db.Column(db.Integer)
    outputOnDelta15 = db.Column(db.Integer)
    outputOnDelta16 = db.Column(db.Integer)
    outputOnDelta17 = db.Column(db.Integer)
    outputOnDelta18 = db.Column(db.Integer)
    outputOffDelta1 = db.Column(db.Integer)
    outputOffDelta2 = db.Column(db.Integer)
    outputOffDelta3 = db.Column(db.Integer)
    outputOffDelta4 = db.Column(db.Integer)
    outputOffDelta5 = db.Column(db.Integer)
    outputOffDelta6 = db.Column(db.Integer)
    outputOffDelta7 = db.Column(db.Integer)
    outputOffDelta8 = db.Column(db.Integer)
    outputOffDelta9 = db.Column(db.Integer)
    outputOffDelta10 = db.Column(db.Integer)
    outputOffDelta11 = db.Column(db.Integer)
    outputOffDelta12 = db.Column(db.Integer)
    outputOffDelta13 = db.Column(db.Integer)
    outputOffDelta14 = db.Column(db.Integer)
    outputOffDelta15 = db.Column(db.Integer)
    outputOffDelta16 = db.Column(db.Integer)
    outputOffDelta17 = db.Column(db.Integer)
    outputOffDelta18 = db.Column(db.Integer)
    outputFaultCount1 = db.Column(db.Integer)
    outputFaultCount2 = db.Column(db.Integer)
    outputFaultCount3 = db.Column(db.Integer)
    outputFaultCount4 = db.Column(db.Integer)
    outputFaultCount5 = db.Column(db.Integer)
    outputFaultCount6 = db.Column(db.Integer)
    outputFaultCount7 = db.Column(db.Integer)
    outputFaultCount8 = db.Column(db.Integer)
    outputFaultCount9 = db.Column(db.Integer)
    outputFaultCount10 = db.Column(db.Integer)
    outputFaultCount11 = db.Column(db.Integer)
    outputFaultCount12 = db.Column(db.Integer)
    outputFaultCount13 = db.Column(db.Integer)
    outputFaultCount14 = db.Column(db.Integer)
    outputFaultCount15 = db.Column(db.Integer)
    outputFaultCount16 = db.Column(db.Integer)
    outputFaultCount17 = db.Column(db.Integer)
    outputFaultCount18 = db.Column(db.Integer)
    temp1_c = db.Column(db.Integer)
    temp2_c = db.Column(db.Integer)
    temp3_c = db.Column(db.Integer)
    temp4_c = db.Column(db.Integer)
    temp5_c = db.Column(db.Integer)
    temp6_c = db.Column(db.Integer)
    temp7_c = db.Column(db.Integer)
    temp8_c = db.Column(db.Integer)
    temp9_c = db.Column(db.Integer)
    temp10_c = db.Column(db.Integer)
    temp11_c = db.Column(db.Integer)
    temp12_c = db.Column(db.Integer)
    temp13_c = db.Column(db.Integer)
    temp14_c = db.Column(db.Integer)
    battMode = db.Column(db.Integer)
    mpptMode = db.Column(db.Integer)
    battHeaterMode = db.Column(db.Integer)
    battHeaterState = db.Column(db.Integer)
    PingWdt_toggles = db.Column(db.Integer)
    PingWdt_turnOffs = db.Column(db.Integer)
    thermalProtTemperature_1 = db.Column(db.Integer)
    thermalProtTemperature_2 = db.Column(db.Integer)
    thermalProtTemperature_3 = db.Column(db.Integer)
    thermalProtTemperature_4 = db.Column(db.Integer)
    thermalProtTemperature_5 = db.Column(db.Integer)
    thermalProtTemperature_6 = db.Column(db.Integer)
    thermalProtTemperature_7 = db.Column(db.Integer)
    thermalProtTemperature_8 = db.Column(db.Integer)

    def to_json(self):
        return {
            'eps_cmd_hk': self.eps_cmd_hk,
            'eps_status_hk': self.eps_status_hk,
            'eps_timestamp_hk': self.eps_timestamp_hk,
            'eps_uptimeInS_hk': self.eps_uptimeInS_hk,
            'eps_bootCnt_hk': self.eps_bootCnt_hk,
            'wdt_gs_time_left_s': self.wdt_gs_time_left_s,
            'wdt_gs_counter': self.wdt_gs_counter,
            'mpptConverterVoltage1_mV': self.mpptConverterVoltage1_mV,
            'mpptConverterVoltage2_mV': self.mpptConverterVoltage2_mV,
            'mpptConverterVoltage3_mV': self.mpptConverterVoltage3_mV,
            'mpptConverterVoltage4_mV': self.mpptConverterVoltage4_mV,
            'curSolarPanels1_mA': self.curSolarPanels1_mA,
            'curSolarPanels2_mA': self.curSolarPanels2_mA,
            'curSolarPanels3_mA': self.curSolarPanels3_mA,
            'curSolarPanels4_mA': self.curSolarPanels4_mA,
            'curSolarPanels5_mA': self.curSolarPanels5_mA,
            'curSolarPanels6_mA': self.curSolarPanels6_mA,
            'curSolarPanels7_mA': self.curSolarPanels7_mA,
            'curSolarPanels8_mA': self.curSolarPanels8_mA,
            'vBatt_mV': self.vBatt_mV,
            'curSolar_mA': self.curSolar_mA,
            'curBattIn_mA': self.curBattIn_mA,
            'curBattOut_mA': self.curBattOut_mA,
            'curOutput1_mA': self.curOutput1_mA,
            'curOutput2_mA': self.curOutput2_mA,
            'curOutput3_mA': self.curOutput3_mA,
            'curOutput4_mA': self.curOutput4_mA,
            'curOutput5_mA': self.curOutput5_mA,
            'curOutput6_mA': self.curOutput6_mA,
            'curOutput7_mA': self.curOutput7_mA,
            'curOutput8_mA': self.curOutput8_mA,
            'curOutput9_mA': self.curOutput9_mA,
            'curOutput10_mA': self.curOutput10_mA,
            'curOutput11_mA': self.curOutput11_mA,
            'curOutput12_mA': self.curOutput12_mA,
            'curOutput13_mA': self.curOutput13_mA,
            'curOutput14_mA': self.curOutput14_mA,
            'curOutput15_mA': self.curOutput15_mA,
            'curOutput16_mA': self.curOutput16_mA,
            'curOutput17_mA': self.curOutput17_mA,
            'curOutput18_mA': self.curOutput18_mA,
            'AOcurOutput1_mA': self.AOcurOutput1_mA,
            'AOcurOutput2_mA': self.AOcurOutput2_mA,
            'outputConverterVoltage1': self.outputConverterVoltage1,
            'outputConverterVoltage2': self.outputConverterVoltage2,
            'outputConverterVoltage3': self.outputConverterVoltage3,
            'outputConverterVoltage4': self.outputConverterVoltage4,
            'outputConverterVoltage5': self.outputConverterVoltage5,
            'outputConverterVoltage6': self.outputConverterVoltage6,
            'outputConverterVoltage7': self.outputConverterVoltage7,
            'outputConverterVoltage8': self.outputConverterVoltage8,
            'outputConverterState': self.outputConverterState,
            'outputStatus': self.outputStatus,
            'outputFaultStatus': self.outputFaultStatus,
            'protectedOutputAccessCnt': self.protectedOutputAccessCnt,
            'outputOnDelta1': self.outputOnDelta1,
            'outputOnDelta2': self.outputOnDelta2,
            'outputOnDelta3': self.outputOnDelta3,
            'outputOnDelta4': self.outputOnDelta4,
            'outputOnDelta5': self.outputOnDelta5,
            'outputOnDelta6': self.outputOnDelta6,
            'outputOnDelta7': self.outputOnDelta7,
            'outputOnDelta8': self.outputOnDelta8,
            'outputOnDelta9': self.outputOnDelta9,
            'outputOnDelta10': self.outputOnDelta10,
            'outputOnDelta11': self.outputOnDelta11,
            'outputOnDelta12': self.outputOnDelta12,
            'outputOnDelta13': self.outputOnDelta13,
            'outputOnDelta14': self.outputOnDelta14,
            'outputOnDelta15': self.outputOnDelta15,
            'outputOnDelta16': self.outputOnDelta16,
            'outputOnDelta17': self.outputOnDelta17,
            'outputOnDelta18': self.outputOnDelta18,
            'outputOffDelta1': self.outputOffDelta1,
            'outputOffDelta2': self.outputOffDelta2,
            'outputOffDelta3': self.outputOffDelta3,
            'outputOffDelta4': self.outputOffDelta4,
            'outputOffDelta5': self.outputOffDelta5,
            'outputOffDelta6': self.outputOffDelta6,
            'outputOffDelta7': self.outputOffDelta7,
            'outputOffDelta8': self.outputOffDelta8,
            'outputOffDelta9': self.outputOffDelta9,
            'outputOffDelta10': self.outputOffDelta10,
            'outputOffDelta11': self.outputOffDelta11,
            'outputOffDelta12': self.outputOffDelta12,
            'outputOffDelta13': self.outputOffDelta13,
            'outputOffDelta14': self.outputOffDelta14,
            'outputOffDelta15': self.outputOffDelta15,
            'outputOffDelta16': self.outputOffDelta16,
            'outputOffDelta17': self.outputOffDelta17,
            'outputOffDelta18': self.outputOffDelta18,
            'outputFaultCount1': self.outputFaultCount1,
            'outputFaultCount2': self.outputFaultCount2,
            'outputFaultCount3': self.outputFaultCount3,
            'outputFaultCount4': self.outputFaultCount4,
            'outputFaultCount5': self.outputFaultCount5,
            'outputFaultCount6': self.outputFaultCount6,
            'outputFaultCount7': self.outputFaultCount7,
            'outputFaultCount8': self.outputFaultCount8,
            'outputFaultCount9': self.outputFaultCount9,
            'outputFaultCount10': self.outputFaultCount10,
            'outputFaultCount11': self.outputFaultCount11,
            'outputFaultCount12': self.outputFaultCount12,
            'outputFaultCount13': self.outputFaultCount13,
            'outputFaultCount14': self.outputFaultCount14,
            'outputFaultCount15': self.outputFaultCount15,
            'outputFaultCount16': self.outputFaultCount16,
            'outputFaultCount17': self.outputFaultCount17,
            'outputFaultCount18': self.outputFaultCount18,
            'temp1_c': self.temp1_c,
            'temp2_c': self.temp2_c,
            'temp3_c': self.temp3_c,
            'temp4_c': self.temp4_c,
            'temp5_c': self.temp5_c,
            'temp6_c': self.temp6_c,
            'temp7_c': self.temp7_c,
            'temp8_c': self.temp8_c,
            'temp9_c': self.temp9_c,
            'temp10_c': self.temp10_c,
            'temp11_c': self.temp11_c,
            'temp12_c': self.temp12_c,
            'temp13_c': self.temp13_c,
            'temp14_c': self.temp14_c,
            'battMode': self.battMode,
            'mpptMode': self.mpptMode,
            'battHeaterMode': self.battHeaterMode,
            'battHeaterState': self.battHeaterState,
            'PingWdt_toggles': self.PingWdt_toggles,
            'PingWdt_turnOffs': self.PingWdt_turnOffs,
            'thermalProtTemperature_1': self.thermalProtTemperature_1,
            'thermalProtTemperature_2': self.thermalProtTemperature_2,
            'thermalProtTemperature_3': self.thermalProtTemperature_3,
            'thermalProtTemperature_4': self.thermalProtTemperature_4,
            'thermalProtTemperature_5': self.thermalProtTemperature_5,
            'thermalProtTemperature_6': self.thermalProtTemperature_6,
            'thermalProtTemperature_7': self.thermalProtTemperature_7,
            'thermalProtTemperature_8': self.thermalProtTemperature_8,
        }


class EpsStartupHK(db.Model):
    __tablename__ = 'eps_startup_hk'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hk_id = db.Column(db.Integer, db.ForeignKey('housekeeping.id'))
    hk = db.relationship('Housekeeping', backref=backref(
        'eps_startup', uselist=False))

    eps_cmd_startup = db.Column(db.Integer)
    eps_status_startup = db.Column(db.Integer)
    eps_timestamp_startup = db.Column(db.Float)
    last_reset_reason_reg = db.Column(db.Integer)
    eps_bootCnt_startup = db.Column(db.Integer)
    FallbackConfigUsed = db.Column(db.Integer)
    rtcInit = db.Column(db.Integer)
    rtcClkSourceLSE = db.Column(db.Integer)
    flashAppInit = db.Column(db.Integer)
    Fram4kPartitionInit = db.Column(db.Integer)
    Fram520kPartitionInit = db.Column(db.Integer)
    intFlashPartitionInit = db.Column(db.Integer)
    fwUpdInit = db.Column(db.Integer)
    FSInit = db.Column(db.Integer)
    FTInit = db.Column(db.Integer)
    supervisorInit = db.Column(db.Integer)
    uart1App = db.Column(db.Integer)
    uart2App = db.Column(db.Integer)
    tmp107Init = db.Column(db.Integer)

    def to_json(self):
        return {
            'eps_cmd_startup': self.eps_cmd_startup,
            'eps_status_startup': self.eps_status_startup,
            'eps_timestamp_startup': self.eps_timestamp_startup,
            'last_reset_reason_reg': self.last_reset_reason_reg,
            'eps_bootCnt_startup': self.eps_bootCnt_startup,
            'FallbackConfigUsed': self.FallbackConfigUsed,
            'rtcInit': self.rtcInit,
            'rtcClkSourceLSE': self.rtcClkSourceLSE,
            'flashAppInit': self.flashAppInit,
            'Fram4kPartitionInit': self.Fram4kPartitionInit,
            'Fram520kPartitionInit': self.Fram520kPartitionInit,
            'intFlashPartitionInit': self.intFlashPartitionInit,
            'fwUpdInit': self.fwUpdInit,
            'FSInit': self.FSInit,
            'FTInit': self.FTInit,
            'supervisorInit': self.supervisorInit,
            'uart1App': self.uart1App,
            'uart2App': self.uart2App,
            'tmp107Init': self.tmp107Init,
        }


class UhfHK(db.Model):
    __tablename__ = 'uhf_hk'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hk_id = db.Column(db.Integer, db.ForeignKey('housekeeping.id'))
    hk = db.relationship('Housekeeping', backref=backref('uhf', uselist=False))

    scw1 = db.Column(db.Integer)
    scw2 = db.Column(db.Integer)
    scw3 = db.Column(db.Integer)
    scw4 = db.Column(db.Integer)
    scw5 = db.Column(db.Integer)
    scw6 = db.Column(db.Integer)
    scw7 = db.Column(db.Integer)
    scw8 = db.Column(db.Integer)
    scw9 = db.Column(db.Integer)
    scw10 = db.Column(db.Integer)
    scw11 = db.Column(db.Integer)
    scw12 = db.Column(db.Integer)
    U_frequency = db.Column(db.Integer)
    pipe_t = db.Column(db.Integer)
    beacon_t = db.Column(db.Integer)
    audio_t = db.Column(db.Integer)
    uptime = db.Column(db.Integer)
    pckts_out = db.Column(db.Integer)
    pckts_in = db.Column(db.Integer)
    pckts_in_crc16 = db.Column(db.Integer)
    temperature = db.Column(db.Float)

    def to_json(self):
        return {
            'scw1': self.scw1,
            'scw2': self.scw2,
            'scw3': self.scw3,
            'scw4': self.scw4,
            'scw5': self.scw5,
            'scw6': self.scw6,
            'scw7': self.scw7,
            'scw8': self.scw8,
            'scw9': self.scw9,
            'scw10': self.scw10,
            'scw11': self.scw11,
            'scw12': self.scw12,
            'U_frequency': self.U_frequency,
            'pipe_t': self.pipe_t,
            'beacon_t': self.beacon_t,
            'audio_t': self.audio_t,
            'uptime': self.uptime,
            'pckts_out': self.pckts_out,
            'pckts_in': self.pckts_in,
            'pckts_in_crc16': self.pckts_in_crc16,
            'temperature': self.temperature
        }


class SbandHK(db.Model):
    __tablename__ = 'sband_hk'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hk_id = db.Column(db.Integer, db.ForeignKey('housekeeping.id'))
    hk = db.relationship(
        'Housekeeping', backref=backref('sband', uselist=False))

    S_mode = db.Column(db.Integer)
    PA_status = db.Column(db.Integer)
    S_frequency_Hz = db.Column(db.Integer)
    S_scrambler = db.Column(db.Integer)
    S_filter = db.Column(db.Integer)
    S_modulation = db.Column(db.Integer)
    S_data_rate = db.Column(db.Integer)
    S_bit_order = db.Column(db.Integer)
    S_PWRGD = db.Column(db.Integer)
    S_TXL = db.Column(db.Integer)
    Output_Power = db.Column(db.Integer)
    PA_Temp = db.Column(db.Integer)
    Top_Temp = db.Column(db.Integer)
    Bottom_Temp = db.Column(db.Integer)
    Bat_Current_mA = db.Column(db.Integer)
    Bat_Voltage_mV = db.Column(db.Integer)
    PA_Current_mA = db.Column(db.Integer)
    PA_Voltage_mV = db.Column(db.Integer)

    def to_json(self):
        return {
            'S_mode': self.S_mode,
            'PA_status': self.PA_status,
            'S_frequency_Hz': self.S_frequency_Hz,
            'S_scrambler': self.S_scrambler,
            'S_filter': self.S_filter,
            'S_modulation': self.S_modulation,
            'S_data_rate': self.S_data_rate,
            'S_bit_order': self.S_bit_order,
            'S_PWRGD': self.S_PWRGD,
            'S_TXL': self.S_TXL,
            'Output_Power': self.Output_Power,
            'PA_Temp': self.PA_Temp,
            'Top_Temp': self.Top_Temp,
            'Bottom_Temp': self.Bottom_Temp,
            'Bat_Current_mA': self.Bat_Current_mA,
            'Bat_Voltage_mV': self.Bat_Voltage_mV,
            'PA_Current_mA': self.PA_Current_mA,
            'PA_Voltage_mV': self.PA_Voltage_mV,
        }


class HyperionHK(db.Model):
    __tablename__ = 'hyperion_hk'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hk_id = db.Column(db.Integer, db.ForeignKey('housekeeping.id'))
    hk = db.relationship(
        'Housekeeping', backref=backref('hyperion', uselist=False))

    Nadir_Temp1 = db.Column(db.Integer)
    Nadir_Temp_Adc = db.Column(db.Integer)
    Port_Temp1 = db.Column(db.Integer)
    Port_Temp2 = db.Column(db.Integer)
    Port_Temp3 = db.Column(db.Integer)
    Port_Temp_Adc = db.Column(db.Integer)
    Port_Dep_Temp1 = db.Column(db.Integer)
    Port_Dep_Temp2 = db.Column(db.Integer)
    Port_Dep_Temp3 = db.Column(db.Integer)
    Port_Dep_Temp_Adc = db.Column(db.Integer)
    Star_Temp1 = db.Column(db.Integer)
    Star_Temp2 = db.Column(db.Integer)
    Star_Temp3 = db.Column(db.Integer)
    Star_Temp_Adc = db.Column(db.Integer)
    Star_Dep_Temp1 = db.Column(db.Integer)
    Star_Dep_Temp2 = db.Column(db.Integer)
    Star_Dep_Temp3 = db.Column(db.Integer)
    Star_Dep_Temp_Adc = db.Column(db.Integer)
    Zenith_Temp1 = db.Column(db.Integer)
    Zenith_Temp2 = db.Column(db.Integer)
    Zenith_Temp3 = db.Column(db.Integer)
    Zenith_Temp_Adc = db.Column(db.Integer)
    Nadir_Pd1 = db.Column(db.Integer)
    Port_Pd1 = db.Column(db.Integer)
    Port_Pd2 = db.Column(db.Integer)
    Port_Pd3 = db.Column(db.Integer)
    Port_Dep_Pd1 = db.Column(db.Integer)
    Port_Dep_Pd2 = db.Column(db.Integer)
    Port_Dep_Pd3 = db.Column(db.Integer)
    Star_Pd1 = db.Column(db.Integer)
    Star_Pd2 = db.Column(db.Integer)
    Star_Pd3 = db.Column(db.Integer)
    Star_Dep_Pd1 = db.Column(db.Integer)
    Star_Dep_Pd2 = db.Column(db.Integer)
    Star_Dep_Pd3 = db.Column(db.Integer)
    Zenith_Pd1 = db.Column(db.Integer)
    Zenith_Pd2 = db.Column(db.Integer)
    Zenith_Pd3 = db.Column(db.Integer)
    Port_Voltage = db.Column(db.Integer)
    Port_Dep_Voltage = db.Column(db.Integer)
    Star_Voltage = db.Column(db.Integer)
    Star_Dep_Voltage = db.Column(db.Integer)
    Zenith_Voltage = db.Column(db.Integer)
    Port_Current = db.Column(db.Integer)
    Port_Dep_Current = db.Column(db.Integer)
    Star_Current = db.Column(db.Integer)
    Star_Dep_Current = db.Column(db.Integer)
    Zenith_Current = db.Column(db.Integer)

    def to_json(self):
        return {
            'Nadir_Temp1': self.Nadir_Temp1,
            'Nadir_Temp_Adc': self.Nadir_Temp_Adc,
            'Port_Temp1': self.Port_Temp1,
            'Port_Temp2': self.Port_Temp2,
            'Port_Temp3': self.Port_Temp3,
            'Port_Temp_Adc': self.Port_Temp_Adc,
            'Port_Dep_Temp1': self.Port_Dep_Temp1,
            'Port_Dep_Temp2': self.Port_Dep_Temp2,
            'Port_Dep_Temp3': self.Port_Dep_Temp3,
            'Port_Dep_Temp_Adc': self.Port_Dep_Temp_Adc,
            'Star_Temp1': self.Star_Temp1,
            'Star_Temp2': self.Star_Temp2,
            'Star_Temp3': self.Star_Temp3,
            'Star_Temp_Adc': self.Star_Temp_Adc,
            'Star_Dep_Temp1': self.Star_Dep_Temp1,
            'Star_Dep_Temp2': self.Star_Dep_Temp2,
            'Star_Dep_Temp3': self.Star_Dep_Temp3,
            'Star_Dep_Temp_Adc': self.Star_Dep_Temp_Adc,
            'Zenith_Temp1': self.Zenith_Temp1,
            'Zenith_Temp2': self.Zenith_Temp2,
            'Zenith_Temp3': self.Zenith_Temp3,
            'Zenith_Temp_Adc': self.Zenith_Temp_Adc,
            'Nadir_Pd1': self.Nadir_Pd1,
            'Port_Pd1': self.Port_Pd1,
            'Port_Pd2': self.Port_Pd2,
            'Port_Pd3': self.Port_Pd3,
            'Port_Dep_Pd1': self.Port_Dep_Pd1,
            'Port_Dep_Pd2': self.Port_Dep_Pd2,
            'Port_Dep_Pd3': self.Port_Dep_Pd3,
            'Star_Pd1': self.Star_Pd1,
            'Star_Pd2': self.Star_Pd2,
            'Star_Pd3': self.Star_Pd3,
            'Star_Dep_Pd1': self.Star_Dep_Pd1,
            'Star_Dep_Pd2': self.Star_Dep_Pd2,
            'Star_Dep_Pd3': self.Star_Dep_Pd3,
            'Zenith_Pd1': self.Zenith_Pd1,
            'Zenith_Pd2': self.Zenith_Pd2,
            'Zenith_Pd3': self.Zenith_Pd3,
            'Port_Voltage': self.Port_Voltage,
            'Port_Dep_Voltage': self.Port_Dep_Voltage,
            'Star_Voltage': self.Star_Voltage,
            'Star_Dep_Voltage': self.Star_Dep_Voltage,
            'Zenith_Voltage': self.Zenith_Voltage,
            'Port_Current': self.Port_Current,
            'Port_Dep_Current': self.Port_Dep_Current,
            'Star_Current': self.Star_Current,
            'Star_Dep_Current': self.Star_Dep_Current,
            'Zenith_Current': self.Zenith_Current
        }


class CharonHK(db.Model):
    __tablename__ = 'charon_hk'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hk_id = db.Column(db.Integer, db.ForeignKey('housekeeping.id'))
    hk = db.relationship(
        'Housekeeping', backref=backref('charon', uselist=False))

    gps_crc = db.Column(db.Integer)
    charon_temp1 = db.Column(db.Integer)
    charon_temp2 = db.Column(db.Integer)
    charon_temp3 = db.Column(db.Integer)
    charon_temp4 = db.Column(db.Integer)
    charon_temp5 = db.Column(db.Integer)
    charon_temp6 = db.Column(db.Integer)
    charon_temp7 = db.Column(db.Integer)
    charon_temp8 = db.Column(db.Integer)

    def to_json(self):
        return {
            'gps_crc': self.gps_crc,
            'charon_temp1': self.charon_temp1,
            'charon_temp2': self.charon_temp2,
            'charon_temp3': self.charon_temp3,
            'charon_temp4': self.charon_temp4,
            'charon_temp5': self.charon_temp5,
            'charon_temp6': self.charon_temp6,
            'charon_temp7': self.charon_temp7,
            'charon_temp8': self.charon_temp8
        }


class DfgmHK(db.Model):
    __tablename__ = 'dfgm_hk'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hk_id = db.Column(db.Integer, db.ForeignKey('housekeeping.id'))
    hk = db.relationship(
        'Housekeeping', backref=backref('dfgm', uselist=False))

    Core_Voltage = db.Column(db.Integer)
    Sensor_Temperature = db.Column(db.Integer)
    Reference_Temperature = db.Column(db.Integer)
    Board_Temperature = db.Column(db.Integer)
    Positive_Rail_Voltage = db.Column(db.Integer)
    Input_Voltage = db.Column(db.Integer)
    Reference_Voltage = db.Column(db.Integer)
    Input_Current = db.Column(db.Integer)
    Reserved_1 = db.Column(db.Integer)
    Reserved_2 = db.Column(db.Integer)
    Reserved_3 = db.Column(db.Integer)
    Reserved_4 = db.Column(db.Integer)

    def to_json(self):
        return {
            'Core_Voltage': self.Core_Voltage,
            'Sensor_Temperature': self.Sensor_Temperature,
            'Reference_Temperature': self.Reference_Temperature,
            'Board_Temperature': self.Board_Temperature,
            'Positive_Rail_Voltage': self.Positive_Rail_Voltage,
            'Input_Voltage': self.Input_Voltage,
            'Reference_Voltage': self.Reference_Voltage,
            'Input_Current': self.Input_Current,
            'Reserved_1': self.Reserved_1,
            'Reserved_2': self.Reserved_2,
            'Reserved_3': self.Reserved_3,
            'Reserved_4': self.Reserved_4
        }


class NorthernSpiritHK(db.Model):
    __tablename__ = 'northern_spirit_hk'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hk_id = db.Column(db.Integer, db.ForeignKey('housekeeping.id'))
    hk = db.relationship('Housekeeping', backref=backref(
        'northern_spirit', uselist=False))

    ns_temp0 = db.Column(db.Integer)
    ns_temp1 = db.Column(db.Integer)
    ns_temp2 = db.Column(db.Integer)
    ns_temp3 = db.Column(db.Integer)
    eNIM0_lux = db.Column(db.Integer)
    eNIM1_lux = db.Column(db.Integer)
    eNIM2_lux = db.Column(db.Integer)
    ram_avail = db.Column(db.Integer)
    lowest_img_num = db.Column(db.Integer)
    first_blank_img_num = db.Column(db.Integer)

    def to_json(self):
        return {
            'ns_temp0': self.ns_temp0,
            'ns_temp1': self.ns_temp1,
            'ns_temp2': self.ns_temp2,
            'ns_temp3': self.ns_temp3,
            'eNIM0_lux': self.eNIM0_lux,
            'eNIM1_lux': self.eNIM1_lux,
            'eNIM2_lux': self.eNIM2_lux,
            'ram_avail': self.ram_avail,
            'lowest_img_num': self.lowest_img_num,
            'first_blank_img_num': self.first_blank_img_num
        }


class IrisHK(db.Model):
    __tablename__ = 'iris_hk'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hk_id = db.Column(db.Integer, db.ForeignKey('housekeeping.id'))
    hk = db.relationship(
        'Housekeeping', backref=backref('iris', uselist=False))

    VIS_Temperature = db.Column(db.Float)
    NIR_Temperature = db.Column(db.Float)
    Flash_Temperature = db.Column(db.Float)
    Gate_Temperature = db.Column(db.Float)
    Image_number = db.Column(db.Integer)
    Software_Version = db.Column(db.Integer)
    Error_number = db.Column(db.Integer)
    MAX_5V_voltage = db.Column(db.Integer)
    MAX_5V_power = db.Column(db.Integer)
    MAX_3V_voltage = db.Column(db.Integer)
    MAX_3V_power = db.Column(db.Integer)
    MIN_5V_voltage = db.Column(db.Integer)
    MIN_3V_voltage = db.Column(db.Integer)

    def to_json(self):
        return {
            'VIS_Temperature': self.VIS_Temperature,
            'NIR_Temperature': self.NIR_Temperature,
            'Flash_Temperature': self.Flash_Temperature,
            'Gate_Temperature': self.Gate_Temperature,
            'Image_number': self.Image_number,
            'Software_Version': self.Software_Version,
            'Error_number': self.Error_number,
            'MAX_5V_voltage': self.MAX_5V_voltage,
            'MAX_5V_power': self.MAX_5V_power,
            'MAX_3V_voltage': self.MAX_3V_voltage,
            'MAX_3V_power': self.MAX_3V_power,
            'MIN_5V_voltage': self.MIN_5V_voltage,
            'MIN_3V_voltage': self.MIN_3V_voltage
        }
