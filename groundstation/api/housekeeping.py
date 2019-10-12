from flask import request
from flask import Blueprint
from flask_restful import Resource, Api
from datetime import datetime
import json

from groundstation.api.models import Housekeeping
from groundstation import db

housekeeping_blueprint = Blueprint('housekeeping', __name__)
api = Api(housekeeping_blueprint)

class HousekeepingLog(Resource):
    def get(self, housekeeping_id):
        """Get a single housekeeping log via its id"""
        response_object = {
            'status': 'fail',
            'message': 'Housekeeping Log does not exist'
        }

        housekeeping = Housekeeping.query.filter_by(id=housekeeping_id).first()

        if not housekeeping:
            return response_object, 404
        else:
            response_object = {
                'status': 'success',
                'data' : housekeeping.toJson()
            }

            return response_object, 200

class HousekeepingLogList(Resource):
    def post(self, local_data=None):
        """Post a housekeeping log"""
        # this api call will have to treat incoming data different if it is called locally
        if not local_data:
            post_data = request.get_json()
        else:
            post_data = json.loads(local_data)

        # since json dates will be strings, convert them to a python datetime object
        post_data['lastBeaconTime'] = datetime.strptime(post_data['lastBeaconTime'], '%Y-%m-%d %H:%M:%S')
        housekeeping = Housekeeping(**post_data)
        db.session.add(housekeeping)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': f'Housekeeping Log with timestamp {housekeeping.lastBeaconTime} was added!'
        }

        return response_object, 201

api.add_resource(HousekeepingLog, '/housekeepinglog/<housekeeping_id>')
api.add_resource(HousekeepingLogList, '/housekeepinglog')

