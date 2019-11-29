from flask import request
from flask import Blueprint
from flask_restful import Resource, Api
from marshmallow import ValidationError
from datetime import datetime
import json

from groundstation.backend_api.models import Housekeeping, PowerChannels
from groundstation import db
from groundstation.backend_api.utils import create_context, login_required, dynamic_filters_housekeeping
from groundstation.backend_api.validators import HousekeepingValidator
from werkzeug.datastructures import MultiDict
from sqlalchemy import desc

housekeeping_blueprint = Blueprint('housekeeping', __name__)
api = Api(housekeeping_blueprint)

class HousekeepingLog(Resource):

    @create_context
    def get(self, housekeeping_id):
        """Endpoint for getting a specific housekeeping log

        :param int housekeeping_id: The housekeeping_id

        :returns: response_object, status_code
        :rtype: tuple (dict, int)
        """
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
        """Endpoint for creating a new Housekeeping log

        :param json_string local_data: This should be used in place of the POST body that would be used through HTTP, used for local calls.

        :returns: response_object, status_code
        :rtype: tuple (dict, int)
        """
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
    def get(self, local_args=None):
        """Endpoint for getting a list of housekeeping logs

        :param dict local_args: This should be used in place of the QUERY PARAMS that would be used through HTTP, used for local calls.

        :returns: response_object, status_code
        :rtype: tuple (dict, int)
        """
        if not local_args:
            query_limit = request.args.get('limit', None)
            newest_first = request.args.get('newest-first', None)
            args = dynamic_filters_housekeeping(request.args, ignore_keys=['limit', 'newest-first'])
        else:
            local_args = MultiDict(local_args)
            query_limit = local_args.get('limit', None)
            newest_first = local_args.get('newest-first', None)
            args = dynamic_filters_housekeeping(local_args, ignore_keys=['limit', 'newest-first'])

        if args is None:
            response_object = {
                'status': 'fail',
                'message': 'Invalid query params',
            }
            return response_object, 400

        if newest_first == "true":
            ordering = desc(Housekeeping.last_beacon_time)
        else:
            ordering = Housekeeping.last_beacon_time

        logs = Housekeeping.query.filter(*args).order_by(ordering).limit(query_limit).all()
        response_object = {
            'status': 'success',
            'data': {
                'logs': [log.to_json() for log in logs]
            }
        }

        return response_object, 200

api.add_resource(HousekeepingLog, '/api/housekeepinglog/<housekeeping_id>')
api.add_resource(HousekeepingLogList, '/api/housekeepinglog')
