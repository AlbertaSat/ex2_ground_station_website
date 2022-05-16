import json
from flask import request
from flask import Blueprint
from flask_restful import Resource, Api
from marshmallow import ValidationError
from groundstation import db
from groundstation.backend_api.models import AutomatedCommands, AutomatedCommandsArgs
from groundstation.backend_api.utils import create_context, login_required
from groundstation.backend_api.validators import AutomatedCommandValidator, AutomatedCommandPatchValidator
from datetime import datetime

automatedcommand_blueprint = Blueprint('automatedcommand', __name__)
api = Api(automatedcommand_blueprint)

class AutomatedCommand(Resource):

    def __init__(self):
        self.validator = AutomatedCommandPatchValidator()
        super(AutomatedCommand, self).__init__()

    @create_context
    @login_required
    def patch(self, automatedcommand_id, local_data=None):
        """Endpoint for patching a specific automated command

        :param int automatedcommand_id: The automated command id
        :param json_string local_data: This should be used in place of the POST body that would be used through HTTP, used for local calls.

        :returns: response_object, status_code
        :rtype: tuple (dict, int)
        """        
        
        if not local_data:
            patch_data = request.get_json()
        else:
            patch_data = json.loads(local_data)
        
        automatedcommand = AutomatedCommands.query.filter_by(id=automatedcommand_id).first()

        if not automatedcommand:
            response_object = {'status': 'fail', 'message': 'Automated command does not exist'}
            return response_object, 404
        
        try: 
            validated_data = self.validator.load(patch_data)
        except ValidationError as err:
            response_object = {
                'status': 'fail',
                'message': 'The posted data is not valid!',
                'errors': err.messages
            }
            return response_object, 400
        
        # for now, only command priority could be updated
        if 'priority' in validated_data:
            automatedcommand.priority = validated_data['priority']
        
        db.session.commit()

        response_object = {
            'status': 'success',
            'data': automatedcommand.to_json()
        }

        return response_object, 200
    
    @create_context
    @login_required
    def delete(self, automatedcommand_id):
        """Endpoint for deleting a specific automated command

        :param int automatedcommand_id: The automated command id

        :returns: response_object, status_code
        :rtype: tuple (dict, int)
        """        

        all_commands = AutomatedCommands.query.order_by(AutomatedCommands.priority).all()
        automatedcommand = AutomatedCommands.query.filter_by(id=automatedcommand_id).first()

        if not automatedcommand:
            response_object = {'status': 'fail', 'message': 'Automated command id does not exist'}
            return response_object, 404

        for command in all_commands:
            if command.priority > automatedcommand.priority:
                command.priority -= 1
        all_commands.remove(automatedcommand)

        db.session.delete(automatedcommand)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'automated command successfully deleted',
            'data': [command.to_json() for command in all_commands]
        }

        return response_object, 200

class AutomatedCommandList(Resource):

    def __init__(self):
        self.validator = AutomatedCommandValidator()
        super(AutomatedCommandList, self).__init__()

    @create_context
    @login_required
    def get(self, local_args=None):
        """Endpoint for getting a list of the Automated Command Sequence

        :param dict local_args: This should be used in place of the QUERY PARAMS that would be used through HTTP, used for local calls.

        :returns: response_object, status_code
        :rtype: tuple (dict, int)
        """

        if not local_args:
            # flask request
            query_limit = request.args.get('limit')
        else:
            # local request
            query_limit = local_args.get('limit')

        automatedcommands = AutomatedCommands.query.order_by(AutomatedCommands.priority).limit(query_limit).all()

        response_object = {
            'status':'success',
            'data': {
                'automatedcommands':[command.to_json() for command in automatedcommands]
            }
        }

        return response_object, 200

    @create_context
    @login_required
    def post(self, local_data=None):
        """Endpoint for creating a new automated command

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
        
        arguments = validated_data.pop('args')
        command_id = validated_data.pop('command')['command_id']
        priority = validated_data.pop('priority')
        automatedcommand = AutomatedCommands(command_id=command_id, priority=priority)

        for arg_data in arguments:
            index = arg_data['index']
            arg = arg_data['argument']
            argument = AutomatedCommandsArgs(index=index, argument=arg)
            automatedcommand.arguments.append(argument)
        
        db.session.add(automatedcommand)
        db.session.commit()

        response_object = {
            'status': 'success',
            'data': automatedcommand.to_json()
        }

        return response_object, 201

api.add_resource(AutomatedCommand, '/api/automatedcommands/<automatedcommand_id>')
api.add_resource(AutomatedCommandList, '/api/automatedcommands')