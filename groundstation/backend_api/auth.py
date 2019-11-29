from flask import request, Blueprint, g
from flask_restful import Resource, Api
from marshmallow import ValidationError
from sqlalchemy import exc
import datetime
import json

from groundstation import db
from groundstation.backend_api.models import User
from groundstation.backend_api.validators import AuthLoginValidator
from groundstation.backend_api.utils import create_context, login_required

auth_blueprint = Blueprint('auth', __name__)
api = Api(auth_blueprint)

class AuthLogin(Resource):

    def __init__(self):
        self.validator = AuthLoginValidator()
        super(AuthLogin, self).__init__()

    @create_context
    def post(self, local_data=None):
        """Endpoint for logging in

        :param json_string local_data: This should be used in place of the POST body that would be used through HTTP, used for local calls.

        :returns: response_object, status_code
        :rtype: tuple
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

        username = validated_data['username']
        password = validated_data['password']

        try:
            user = User.query.filter_by(username=username).first()
            if user is not None and user.verify_password(password):
                auth_token = user.encode_auth_token_by_id()
                response_object = {
                    'status':'success',
                    'message':'User successfully logged in.',
                    'auth_token':auth_token.decode()
                }
                return response_object, 200
            else:
                response_object = {
                    'status':'fail',
                    'message':'Username and/or password is incorrect'
                }
                return response_object, 400
        except Exception as e:
            response_object = {
                'status':'fail',
                'message':'Oops, something went wrong.'
            }
            return response_object, 500


class AuthLogout(Resource):

    @create_context
    @login_required
    def get(self, local_args=None):
        # TODO: implement logout logic (blacklisted tokens?), currently logging out from backend is NOT supported
        response_object = {
            'status':'success',
            'message':'FAKE NEWS - Successfully logged out.'
        }
        return response_object, 200


api.add_resource(AuthLogin, '/api/auth/login')
api.add_resource(AuthLogout, '/api/auth/logout')
