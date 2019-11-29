from flask import request
from flask import Blueprint
from flask_restful import Resource, Api
from datetime import datetime
import json
from marshmallow import ValidationError
from groundstation import db
from groundstation.backend_api.models import Telecommands
from groundstation.backend_api.utils import create_context, add_telecommand, login_required
from groundstation.backend_api.validators import TelecommandListValidator

telecommand_blueprint = Blueprint('telecommand', __name__)
api = Api(telecommand_blueprint)

class Telecommand(Resource):

    @create_context
    def get(self, telecommand_id, local_args=None):
        """Endpoint for getting a single telecommand

        :param int telecommand_id: The id of the telecommand to get
        :param dict local_args: This should be used in place of the QUERY PARAMS that would be used through HTTP, used for local calls.

        :returns: response_object, status_code
        :rtype: tuple (dict, int)
        """
        response_object = {
            'status': 'fail',
            'message': 'telecommand does not exist'
        }
        command = Telecommands.query.filter_by(id=telecommand_id).first()
        if not command:
            return response_object, 404
        else:
            response_object = {
                'status':'success',
                'data':command.to_json()
            }
            return response_object, 200


class TelecommandList(Resource):

    def __init__(self):
        self.validator = TelecommandListValidator()
        super(TelecommandList, self).__init__()

    @create_context
    def get(self):
        """Endpoint for getting all valid telecommands

        :returns: response_object, status_code
        :rtype: tuple (dict, int)
        """
        telecommands = Telecommands.query.all()
        response_object = {
            'status': 'success',
            'message': 'returned all commands',
            'data': {
                'telecommands':[command.to_json() for command in telecommands]
            }
        }
        return response_object, 200

    @create_context
    @login_required
    def post(self, local_data=None):
        """Endpoint for creating a new telecommand (virtually never used)

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
                'message': 'The posted data is not valid!',
                'errors': err.messages
            }
            return response_object, 400

        telecommand = Telecommands(**validated_data)
        db.session.add(telecommand)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': f'Command was added',
            'data':telecommand.to_json()
        }
        return response_object, 201

api.add_resource(Telecommand, '/api/telecommands/<telecommand_id>')
api.add_resource(TelecommandList,'/api/telecommands')
