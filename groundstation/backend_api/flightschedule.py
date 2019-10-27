import json
from flask import request
from flask import Blueprint
from flask_restful import Resource, Api
from marshmallow import ValidationError
from groundstation import db
from groundstation.backend_api.models import FlightSchedules
from groundstation.backend_api.utils import create_context
from groundstation.backend_api.validators import FlightScheduleValidator

flightschedule_blueprint = Blueprint('flightschedule', __name__)
api = Api(flightschedule_blueprint)

class FlightScheduleList(Resource):

    def __init__(self):
        self.validate = FlightScheduleValidator()
        super(FlightScheduleList, self).__init__()

    @create_context
    def get(self):
        pass

    @create_context
    def post(self, local_data=None):

        if not local_data:
            post_data = request.get_json()
        else:
            post_data = json.loads(local_data)

        try:
            validated_data = self.validate(post_data)
        except ValidationError as err:
            response_object = {
                'status': 'fail',
                'message': 'The posted data is not valid!',
                'errors': err.messages
            }
            return response_object, 400

        # check that we are not queueing multiple flight schedules
        if validated_data['is_queued']:
            num_queued = FlightSchedules.query.filter_by(is_queued=True).count()
            if num_queued > 0:
                response_object = {
                    'status': 'fail',
                    'message': 'A Queued flight schedule already exists!'
                }
                return response_object, 400

        # TODO validate commands
        flightschedule_commands = validated_data.pop('commands')
        flightschedule = FlightSchedules(**validated_data)
        db.session.add(flightschedule)

        for command_data in flightschedule_commands:
            command = FlightScheduleCommands(**command_data)
            db.session.add(command)

        db.session.commit()

        response_object = {
            'status': 'success',
            'message': f'Flight Schedule was successfully created!'
        }

        return response_object, 201


api.add_resource(FlightScheduleList, '/api/flightschedules')
