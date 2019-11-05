##########################################################
#                                                        #
# This file creates a function to add a telecommand      #
# to the telecommand table by posting a JSON file with   #
# Command Name : (number of arguments, is_dangerous flag)#
#                                                        #
##########################################################

from flask import request
from flask import Blueprint
from flask_restful import Resource, Api
from datetime import datetime
import json

from groundstation.backend_api.models import Telecommands
from groundstation import db
from groundstation.backend_api.utils import create_context, add_telecommand

telecommand_blueprint = Blueprint('telecommand', __name__)
api = Api(telecommand_blueprint)

class TelecommandService(Resource):

    @create_context
    def post(self, local_data=None):
        
        #"""Post a telecommand"""
        # this api call will have to treat incoming data different if it is called locally
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload'
        }

        if not local_data:
            post_data = request.get_json()
        else:
            post_data = json.loads(local_data)

        try:
            #TODO: reformat or extract data from JSON

            #JSON object expected
            # dict {
            # command_name : "NAME"
            # num_args : int
            # is_dangerous : bool
            # }

            #converting types and checking correct values
            #post_data[''] =
            pass
        except (ValueError, TypeError, KeyError) as error:
            return response_object, 400


        telecommand = Telecommands(command_name=post_data["command_name"], num_arguments=post_data["num_args"], is_dangerous=post_data["is_dangerous"])
        db.session.add(telecommand)
        db.session.commit()

        response_object = {
            'status': 'success',

            'message': f'Command {post_data["command_name"]} was added!'
        }

        return response_object, 201

    def get(self, local_data=None):
        #get all telecommands
        #add an optional field to fetch a specific command?

        response_object = {
            'status': 'fail',
            'message': 'no commands'
        }

        post_data = None

        if not local_data:
            post_data = request.get_json()
        else:
            post_data = json.loads(local_data)

        command = Telecommands.filter_by(id=post_data['id']).first()

        response_object = {
            'status': 'success',
            'data': command.to_json()
        }

        return response_object, 200


class TelecommandList(Resource):

    @create_context
    def get(self):

        commList = Telecommands.query.all()

        response_object = {
            'status': 'success',
            'message': 'returned all commands'
            'data': {
                'commands': {command.to_json() for command in commList}
            }

        }

        return response_object, 200

api.add_resource(TelecommandService, 'api.telecommandservie/<telecommand_id>')
api.add_resource(TelecommandList,'api/telecommandlist')