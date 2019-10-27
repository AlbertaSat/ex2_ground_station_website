from flask import Blueprint
from flask_restful import Resource, Api, reqparse, fields, marshal_with

from groundstation import db
from groundstation.backend_api.models import FlightSchedules
from groundstation.backend_api.utils import create_context

flightschedule_blueprint = Blueprint('flightschedule', __name__)
api = Api(flightschedule_blueprint)

class FlightScheduleList(Resource):

    def get(self):
        pass

    def post(self):

        # id
        # creation_date
        # upload_date
        # is_queued
        # commands

        if not local_data:
            post_data = request.get_json()
        else:
            post_data = json.loads(local_data)

        # check that we are not queueing multiple flight schedules
        num_queued = FlightSchedules.query.filter_by(is_queued='True').count()
        if num_queued > 0:
            response_object = {
                'status': 'fail',
                'message': 'A Queued flight schedule already exists!'
            }
            return response_object, 400

        # pseudo from here
        try:
            flightschedule_commands = post_data.pop('commands')
        except keyerror etc:
            need commands array to be posted, even if empty ([])
            abort

        flightschedule = FlightSchedules(**post_data)
        db.session.add(flightschedule)

        for command_data in flightschedulecommands:
            command = FlightScheduleCommands(**command_data)
            db.session.add(command)

        db.session.commit()

        response_object = {
            'status': 'success',
            'message': f'Housekeeping Log with timestamp {housekeeping.lastBeaconTime} was added!'
        }

        return response_object, 201



api.add_resource(FlightScheduleList, '/api/flightschedules')
