from marshmallow import Schema, fields

class FlightScheduleValidator:

    def __init__(self):
        self.schema = Schema.from_dict({
            'is_queued': fields.Boolean(required=True), 'commands': fields.List(fields.Dict(), required=True)
        })

    def __call__(self, dict_rep):
        validated_data = self.schema().load(dict_rep)
        return validated_data
