from flask import request
from flask import Blueprint
from flask_restful import Resource, Api
from marshmallow import ValidationError
from datetime import datetime
import json

from groundstation.backend_api.models import Housekeeping, PowerChannels
from groundstation import db
from groundstation.backend_api.utils import create_context, login_required
from groundstation.backend_api.validators import HousekeepingValidator

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

    def __init__(self):
        self.validator = HousekeepingValidator()
        super(HousekeepingLogList, self).__init__()

    @create_context
    @login_required
    def post(self, local_data=None):
        if not local_data:
            post_data = request.get_json()
        else:
            post_data = json.loads(local_data)

        try:
            validated_data = self.validator.load(post_data)
        except ValidationError as err:
            response_object = {
                'status': 'fail',
                'message': 'Invalid payload',
                'errors': err.messages
            }
            return response_object, 400

        channels = validated_data.pop('channels')
        housekeeping = Housekeeping(**validated_data)

        for channel in channels:
            p = PowerChannels(**channel)
            housekeeping.channels.append(p)

        db.session.add(housekeeping)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': f'Housekeeping Log with timestamp {housekeeping.last_beacon_time} was added!'
        }

        return response_object, 201

    @create_context
    def get(self):
        # for query string ?limit=n
        # if no limit defined it is none
        # TODO: Get this working for local calls
        query_limit = request.args.get('limit')
        logs = Housekeeping.query.order_by(Housekeeping.last_beacon_time).limit(query_limit).all()

        response_object = {
            'status': 'success',
            'data': {
                'logs': [log.to_json() for log in logs]
            }
        }

        return response_object, 200

api.add_resource(HousekeepingLog, '/api/housekeepinglog/<housekeeping_id>')
api.add_resource(HousekeepingLogList, '/api/housekeepinglog')
