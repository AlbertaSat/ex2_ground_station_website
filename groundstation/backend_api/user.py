from flask import request, Blueprint, g
from flask_restful import Resource, Api
from marshmallow import ValidationError
from sqlalchemy import exc
import datetime
import json

from groundstation import db
from groundstation.backend_api.models import User
from groundstation.backend_api.validators import UserValidator
from groundstation.backend_api.utils import create_context, login_required

user_blueprint = Blueprint('user', __name__)
api = Api(user_blueprint)

class UserEntity(Resource):

    @create_context
    def get(self, user_id, local_args=None):
        user = User.query.filter_by(id=user_id).first()
        response_object = {
            'status':None,
            'message':None,
            'data':None
        }
        if user is None:
            response_object['status'] = 'fail'
            response_object['message'] = 'User does not exist.'
            response_object['data'] = None
            return response_object, 404

        response_object['status'] = 'success'
        response_object['message'] = 'User was successfully found.'
        response_object['data'] = user.to_json()
        return response_object, 200


class UserList(Resource):

    def __init__(self):
        self.validator = UserValidator()
        super(UserList, self).__init__()

    @create_context
    @login_required
    def post(self, local_data=None):
        if not g.user.is_admin:
            response_object = {
                'status':'fail',
                'message':'You do not have permission to create users.'
            }
            return response_object, 403

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

        new_user = User(**validated_data)
        try:
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            # TODO: Probably remove dev_message
            response_object = {
                'status':'fail',
                'message':'Invalid Payload',
                'dev_message':str(e.orig)
            }
            return response_object, 400

        response_object = {
            'status':'success',
            'message':'User was successfully added',
            'data':new_user.to_json()
        }
        return response_object, 201


api.add_resource(UserList, '/api/users')
api.add_resource(UserEntity, '/api/users/<user_id>')
