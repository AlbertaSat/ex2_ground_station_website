from marshmallow import Schema, fields, validate

class ArgumentValidator(Schema):
    index = fields.Integer(required=True)
    argument = fields.Integer(required=True)

class CommandValidator(Schema):
	command_id = fields.Integer(required=True)
	num_arguments = fields.Integer(required=False)
	is_dangerous = fields.Boolean(required=False)
	command_name = fields.String(required=False)

class FlightScheduleCommandValidator(Schema):
    timestamp = fields.DateTime(format='iso', required=True)
    command = fields.Nested(CommandValidator, required=True)
    args = fields.Nested(ArgumentValidator, required=True, many=True)
    #flightschedule_id = fields.Integer(required=True)

class FlightScheduleValidator(Schema):
    is_queued = fields.Boolean(required=True)
    commands = fields.Nested(FlightScheduleCommandValidator, many=True, required=True)

class FlightSchedulePatchCommandValidator(Schema):
    op = fields.String(required=True)
    timestamp = fields.DateTime(format='iso', required=True)
    command = fields.Nested(CommandValidator, required=True)
    flightschedule_command_id = fields.Integer(required=False)
    args = fields.Nested(ArgumentValidator, required=True, many=True)

class FlightSchedulePatchValidator(Schema):
	is_queued = fields.Boolean(required=True)
	commands = fields.Nested(FlightSchedulePatchCommandValidator, many=True, required=True)

class PassoverValidator(Schema):
    timestamp = fields.DateTime(format='iso', required=True)

class PassoverListValidator(Schema):
    passovers = fields.Nested(PassoverValidator, many=True, required=True, validate=validate.Length(min=1))
