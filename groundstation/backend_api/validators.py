"""This module contains Validators which can be used to validated JSON payloads or dicts to make sure they follow
the expected format and contain the required information needed by the backend_api endpoints. Refer to backend_api endpoints
for examples, eg.) backend_api.housekeeping.HousekeepingLogList.post. Note: You can nest validators using the Nested field.
"""

from marshmallow import Schema, fields, validate

class ArgumentValidator(Schema):
    """Validator for arguments to flight schedule commands
    """
    index = fields.Integer(required=True)
    argument = fields.Integer(required=True)

class CommandValidator(Schema):
    """Validator for a single flight schedule command
    """
    command_id = fields.Integer(required=True)
    num_arguments = fields.Integer(required=False)
    is_dangerous = fields.Boolean(required=False)
    command_name = fields.String(required=False)

class FlightScheduleCommandValidator(Schema):
    """Validator for flighschedule commands
    """
    timestamp = fields.DateTime(format='iso', required=True)
    command = fields.Nested(CommandValidator, required=True)
    args = fields.Nested(ArgumentValidator, required=True, many=True)
    #flightschedule_id = fields.Integer(required=True)

class FlightScheduleValidator(Schema):
    """Validator for flight schedules
    """
    status = fields.Integer(required=True, validate=validate.Range(min=1, max=3))
    commands = fields.Nested(FlightScheduleCommandValidator, many=True, required=True)
    execution_time = fields.DateTime(format='iso', required=True)

class FlightSchedulePatchCommandValidator(Schema):
    """Validator for patching (editing) a flightschedule's commands
    """
    op = fields.String(required=True)
    timestamp = fields.DateTime(format='iso', required=True)
    command = fields.Nested(CommandValidator, required=True)
    flightschedule_command_id = fields.Integer(required=False)
    args = fields.Nested(ArgumentValidator, required=True, many=True)

class FlightSchedulePatchValidator(Schema):
    """Validator for patching (editing) a flightschedule
    """
    status = fields.Integer(required=True, validate=validate.Range(min=1, max=3))
    commands = fields.Nested(FlightSchedulePatchCommandValidator, many=True, required=True)
    execution_time = fields.DateTime(format='iso', required=True)

class PassoverValidator(Schema):
    """Validator for passovers
    """
    timestamp = fields.DateTime(format='iso', required=True)

class PassoverListValidator(Schema):
    """Validator list of passovers
    """
    passovers = fields.Nested(PassoverValidator, many=True, required=True, validate=validate.Length(min=1))

class UserValidator(Schema):
    """Validator for creating new users
    """
    username = fields.String(required=True)
    password = fields.String(required=True)

class AuthLoginValidator(Schema):
    """Validator for checking login information is present
    """
    username = fields.String(required=True)
    password = fields.String(required=True)

class TelecommandListValidator(Schema):
    """Validator for new telecommands
    """
    command_name = fields.String(required=True)
    num_arguments = fields.Integer(required=True)
    is_dangerous = fields.Boolean(required=True)

class PowerChannelValidator(Schema):
    """Validator for power channels
    """
    channel_no = fields.Integer(required=False) # Range of 1-24
    enabled = fields.Boolean(required=False)
    current = fields.Float(required=False)

class HousekeepingValidator(Schema):
    """Validator for houskeeping
    """
    satellite_mode = fields.String(required=False)
    battery_voltage = fields.Float(required=False)
    current_in = fields.Float(required=False)
    current_out = fields.Float(required=False)
    no_MCU_resets = fields.Integer(required=False)
    last_beacon_time = fields.DateTime(format='iso', required=True)
    watchdog_1 = fields.Integer(required=False) # 3 watchdogs
    watchdog_2 = fields.Integer(required=False)
    watchdog_3 = fields.Integer(required=False)
    panel_1_current = fields.Float(required=False) # 6 solar panel currents
    panel_2_current = fields.Float(required=False)
    panel_3_current = fields.Float(required=False)
    panel_4_current = fields.Float(required=False)
    panel_5_current = fields.Float(required=False)
    panel_6_current = fields.Float(required=False)
    temp_1 = fields.Float(required=False) # 6 temperatures at diff locations
    temp_2 = fields.Float(required=False)
    temp_3 = fields.Float(required=False)
    temp_4 = fields.Float(required=False)
    temp_5 = fields.Float(required=False)
    temp_6 = fields.Float(required=False)
    channels = fields.Nested(PowerChannelValidator, many=True, required=True)
