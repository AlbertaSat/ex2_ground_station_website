from marshmallow import Schema, fields, validate

class FlightScheduleCommandValidator(Schema):
    command_id = fields.Integer(required=True)
    timestamp = fields.DateTime(format='iso', required=True)
    flightschedule_id = fields.Integer(required=True)

class FlightScheduleValidator(Schema):
    is_queued = fields.Boolean(required=True)
    commands = fields.Nested(FlightScheduleCommandValidator, many=True, required=True)

class PassoverValidator(Schema):
    timestamp = fields.DateTime(format='iso', required=True)

class PassoverListValidator(Schema):
    passovers = fields.Nested(PassoverValidator, many=True, required=True, validate=validate.Length(min=1))
