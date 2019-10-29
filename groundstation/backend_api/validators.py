from marshmallow import Schema, fields, validate

class FlightScheduleValidator:

    def __init__(self):
        self.schema = Schema.from_dict({
            'is_queued': fields.Boolean(required=True), 'commands': fields.List(fields.Dict(), required=True)
        })

    def __call__(self, dict_rep):
        validated_data = self.schema().load(dict_rep)
        return validated_data

class PassoverValidator(Schema):
    timestamp = fields.DateTime(format='iso', required=True)

class PassoverListValidator(Schema):
    passovers = fields.Nested(PassoverValidator, many=True, required=True, validate=validate.Length(min=1))
