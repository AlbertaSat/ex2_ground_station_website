from flask import Blueprint
from flask_restful import Resource, Api, reqparse

from groundstation import db
from groundstation.backend_api.utils import create_context

flightschedule_blueprint = Blueprint('flightschedule', __name__)
api = Api(flightschedule_blueprint)

class FlightScheduleList(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('rate', type=int, help='Rate to charge for this resource')

        # commands = db.relationship('FlightScheduleCommands', backref='flightschedule', lazy=True)


    def get(self):
        pass

    def post(self):
        args = parser.parse_args()



api.add_resource(FlightScheduleList, '/api/flightschedules')
