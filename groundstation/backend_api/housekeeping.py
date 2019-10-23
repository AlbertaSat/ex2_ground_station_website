from flask import request
from flask import Blueprint
from flask_restful import Resource, Api
from datetime import datetime
import json

from groundstation.backend_api.models import Housekeeping
from groundstation import db
from groundstation.backend_api.utils import create_context

housekeeping_blueprint = Blueprint('housekeeping', __name__)
api = Api(housekeeping_blueprint)

class HousekeepingLog(Resource):

    @create_context
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
                'data' : housekeeping.to_json()
            }

            return response_object, 200

class HousekeepingLogList(Resource):

    @create_context
    def post(self, local_data=None):
        """Post a housekeeping log"""
        # this api call will have to treat incoming data different if it is called locally
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload'
        }

        if not local_data:
            post_data = request.get_json()
        else:
            post_data = json.loads(local_data)

        # since incoming timestamp will be a string, convert it into a datetime object
        # also handle all errors that could occur with the timestamp
        # as a timestamp is necessary for all housekeeping logs
        try:
            post_data['lastBeaconTime'] = datetime.strptime(post_data['lastBeaconTime'], '%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError, KeyError) as error:
            return response_object, 400

        housekeeping = Housekeeping(**post_data)
        db.session.add(housekeeping)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': f'Housekeeping Log with timestamp {housekeeping.lastBeaconTime} was added!'
        }

        return response_object, 201

    @create_context
    def get(self):
        # for query string ?limit=n
        # if no limit defined return all
        query_limit = request.args.get('limit')

        if query_limit:
            logs = Housekeeping.query.order_by(Housekeeping.lastBeaconTime).limit(query_limit).all()
        else:
            logs = Housekeeping.query.order_by(Housekeeping.lastBeaconTime).all()

        response_object = {
            'status': 'success',
            'data': {
                'logs': [log.to_json() for log in logs]
            }
        }

        return response_object, 200

api.add_resource(HousekeepingLog, '/api/housekeepinglog/<housekeeping_id>')
api.add_resource(HousekeepingLogList, '/api/housekeepinglog')

