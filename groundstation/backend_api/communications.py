from flask import request
from flask import Blueprint
from flask_restful import Resource, Api
import datetime
import json
from sqlalchemy import desc

from groundstation.backend_api.models import Communications
from groundstation import db
from groundstation.backend_api.utils import create_context, dynamic_filters_communications, login_required

communications_blueprint = Blueprint('communications', __name__)
api = Api(communications_blueprint)

class Communication(Resource):

    @create_context
    def get(self, message_id):
        """Endpoint for getting a specific message

        :param int message_id: The message id

        :returns: response_object, status_code
        :rtype: tuple (dict, int)
        """
        response_object = {
            'status': 'fail',
            'message': 'message does not exist'
        }

        # get a single message via it's ID
        message = Communications.filter_by(id=message_id).first() # should only be one

        if not message: # query of Communications returned nothing
            return response_object, 404
        else: # there is a message in Communications with message_id
            response_object = {
                'status': 'success',
                'data': message.to_json()
            }

            return response_object, 200

    @create_context
    @login_required
    def patch(self, message_id, local_data=None):
        """Endpoint for patching a specific communication

        :param int flightschedule_id: The flightschedule_id id
        :param json_string local_data: This should be used in place of the POST body that would be used through HTTP, used for local calls.

        :returns: response_object, status_code
        :rtype: tuple (dict, int)
        """
        if not local_data:
            post_data = request.get_json()
        else:
            post_data = json.loads(local_data)
            
        message = Communications.query.filter_by(id=message_id).first()

        if not message:
            response_object = {'status': 'fail', 'message': 'Flightschedule does not exist'}
            return response_object, 404

        #TODO: assertion checks for proper data types in post_data (see validation.py)

        # Change whether this message is queued
        message.is_queued = post_data['is_queued']

        db.session.commit()

        response_object = {
            'status': 'success',
            'data': message.to_json()
        }

        return response_object, 200

class CommunicationList(Resource):
    @create_context
    @login_required
    def post(self, local_data=None):
        """Endpoint for posting a new message to communications table

        :param json_string local_data: This should be used in place of the POST body that would be used through HTTP, used for local calls.

        :returns: response_object, status_code
        :rtype: tuple (dict, int)
        """
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload'
        }

        if not local_data:
            post_data = request.get_json()
        else:
            post_data = json.loads(local_data)

        # NOTE: why do we do this
        # TODO: also we need a validator...
        post_data.update({'timestamp': datetime.datetime.now(datetime.timezone.utc)})

        #TODO: assertion checks for proper data types (in validation.py)

        message = Communications(**post_data)
        db.session.add(message)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': f'message {message.message} was sent!',
            'data': message.to_json()
        }

        return response_object, 201

    @create_context
    def get(self, local_data=None):
        """Endpoint for getting messages

        :param dict local_data: This should be used in place of the QUERY PARAMS that would be used through HTTP, used for local calls.

        :returns: response_object, status_code
        :rtype: tuple (dict, int)
        """
        if not local_data:
            request_args_dict = request.args.to_dict()
            newest_first = request_args_dict.pop('newest-first', None)
            args = dynamic_filters_communications(request.args)
        else:
            newest_first = local_data.pop('newest-first', None)
            args = dynamic_filters_communications(local_data)

        response_object = {
            'status': 'fail',
            'message': 'no available messages'
        }

        if newest_first in ("true", True):
            ordering = desc(Communications.id)
        else:
            ordering = Communications.id

        # order by ascending [min_id, min_id + 1, ..., max_id]
        message_list = Communications.query.filter(*args).order_by(ordering)

        if not message_list: # no messages for receiver
            response_object.update({'data':[]})
            return response_object, 200
        else: #message_list has multiple objects
            response_object = {
                'status': 'success',
                'data': {
                    'messages': [message.to_json() for message in message_list]
                }
            }
            return response_object, 200

api.add_resource(CommunicationList, '/api/communications')
api.add_resource(Communication, '/api/communications/<message_id>')
