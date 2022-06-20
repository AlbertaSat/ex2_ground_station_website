"""This module contains Validators which can be used to validated JSON payloads or dicts to make sure they follow
the expected format and contain the required information needed by the backend_api endpoints. Refer to backend_api endpoints
for examples, eg.) backend_api.housekeeping.HousekeepingLogList.post. Note: You can nest validators using the Nested field.
"""

from marshmallow import Schema, fields, validate, \
    validates_schema, ValidationError


class ArgumentValidator(Schema):
    """Validator for arguments to flight schedule or automated commands
    """
    index = fields.Integer(required=True)
    argument = fields.Integer(required=True)


class CommandValidator(Schema):
    """Validator for a single flight schedule or automated command
    """
    command_id = fields.Integer(required=True)
    num_arguments = fields.Integer(required=False)
    is_dangerous = fields.Boolean(required=False)
    command_name = fields.String(required=False)


class FlightScheduleCommandRepeatValidator(Schema):
    """Validator for the repeat settings for a single flight schedule command
    """
    repeat_ms = fields.Boolean(required=True)
    repeat_sec = fields.Boolean(required=True)
    repeat_min = fields.Boolean(required=True)
    repeat_hr = fields.Boolean(required=True)
    repeat_day = fields.Boolean(required=True)
    repeat_month = fields.Boolean(required=True)
    repeat_year = fields.Boolean(required=True)

    @validates_schema
    def validate_min_hr_repeat(self, data, **kwargs):
        if data['repeat_min'] and not data['repeat_hr']:
            raise ValidationError(
                'repeat_hr MUST be checked if repeat_min is also checked!')


class AutomatedCommandValidator(Schema):
    """Validator for automated commands
    """
    priority = fields.Integer(required=True)
    command = fields.Nested(CommandValidator, required=True)
    args = fields.Nested(ArgumentValidator, required=True, many=True)


class AutomatedCommandPatchValidator(Schema):
    """Validator for patching (editing) an automated command
    """
    priority = fields.Integer(required=False)
    command = fields.Nested(CommandValidator, required=False)
    args = fields.Nested(ArgumentValidator, required=False, many=True)
    automatedcommand_id = fields.Integer(required=False)


class FlightScheduleCommandValidator(Schema):
    """Validator for flighschedule commands
    """
    timestamp = fields.DateTime(format='iso', required=True)
    command = fields.Nested(CommandValidator, required=True)
    args = fields.Nested(ArgumentValidator, required=True, many=True)
    repeats = fields.Nested(
        FlightScheduleCommandRepeatValidator, required=True)


class FlightScheduleValidator(Schema):
    """Validator for flight schedules
    """
    status = fields.Integer(
        required=True, validate=validate.Range(min=1, max=3))
    commands = fields.Nested(
        FlightScheduleCommandValidator, many=True, required=True)
    execution_time = fields.DateTime(format='iso', required=True)


class FlightSchedulePatchCommandValidator(Schema):
    """Validator for patching (editing) a flightschedule's commands
    """
    op = fields.String(required=True)
    timestamp = fields.DateTime(format='iso', required=True)
    command = fields.Nested(CommandValidator, required=True)
    flightschedule_command_id = fields.Integer(required=False)
    args = fields.Nested(ArgumentValidator, required=True, many=True)
    repeats = fields.Nested(
        FlightScheduleCommandRepeatValidator, required=True)


class FlightSchedulePatchValidator(Schema):
    """Validator for patching (editing) a flightschedule
    """
    status = fields.Integer(
        required=True, validate=validate.Range(min=1, max=3))
    commands = fields.Nested(
        FlightSchedulePatchCommandValidator, many=True, required=True)
    execution_time = fields.DateTime(format='iso', required=True)


class PassoverValidator(Schema):
    """Validator for passovers
    """
    timestamp = fields.DateTime(format='iso', required=True)


class PassoverListValidator(Schema):
    """Validator list of passovers
    """
    passovers = fields.Nested(
        PassoverValidator, many=True, required=True, validate=validate.Length(min=1))


class UserValidator(Schema):
    """Validator for creating new users
    """
    username = fields.String(required=True)
    password = fields.String(required=True)


class UserPatchValidator(Schema):
    """Validator for patching existing users
    """
    username = fields.String(required=False)
    password = fields.String(required=False)
    is_admin = fields.Boolean(required=False)
    slack_id = fields.String(required=False)
    subscribed_to_slack = fields.Boolean(required=False)


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
    channel_no = fields.Integer(required=False)  # Range of 1-24
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
    tle = fields.String(required=False)
    watchdog_1 = fields.Integer(required=False)  # 3 watchdogs
    watchdog_2 = fields.Integer(required=False)
    watchdog_3 = fields.Integer(required=False)
    panel_1_current = fields.Float(required=False)  # 6 solar panel currents
    panel_2_current = fields.Float(required=False)
    panel_3_current = fields.Float(required=False)
    panel_4_current = fields.Float(required=False)
    panel_5_current = fields.Float(required=False)
    panel_6_current = fields.Float(required=False)
    temp_1 = fields.Float(required=False)  # 6 temperatures at diff locations
    temp_2 = fields.Float(required=False)
    temp_3 = fields.Float(required=False)
    temp_4 = fields.Float(required=False)
    temp_5 = fields.Float(required=False)
    temp_6 = fields.Float(required=False)
    channels = fields.Nested(PowerChannelValidator, many=True, required=True)
