from flask import request, Blueprint, g
from flask_restful import Resource, Api
from marshmallow import ValidationError
from sqlalchemy import exc
import datetime
import json

from groundstation import db
from groundstation.backend_api.models import User
from groundstation.backend_api.validators import UserValidator, UserPatchValidator
from groundstation.backend_api.utils import create_context, login_required

user_blueprint = Blueprint('user', __name__)
api = Api(user_blueprint)


class UserEntity(Resource):
    def __init__(self):
        self.validator = UserPatchValidator()
        super(UserEntity, self).__init__()

    @create_context
    def get(self, auth_token, local_args=None):
        """Endpoint for getting a user's info

        :param int auth_token: The auth_token of the user to get
        :param dict local_args: This should be used in place of the QUERY PARAMS that would be used through HTTP, used for local calls.

        :returns: response_object, status_code
        :rtype: tuple (dict, int)
        """
        user = User.query.filter_by(
            id=User.decode_auth_token(auth_token)).first()

        response_object = {
            'status': None,
            'message': None,
            'data': None
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

    @create_context
    @login_required
    def patch(self, auth_token, local_data=None):
        """ Endpoint for patching a specific user's data

        :param int auth_token: The auth_token of the user to patch
        :param json_string local_data: This should be used in place of the POST body that would be used through HTTP, used for local calls.

        :returns: response_object, status_code
        :rtype: tuple (dict, int)
        """
        if not local_data:
            post_data = request.get_json()
        else:
            post_data = json.loads(local_data)

        # has to be called id in request JSON for data to be validated
        other_user_id = post_data.get('id')

        if other_user_id:
            if not g.user.is_admin:
                response_object = {
                    'status': 'fail',
                    'message': 'You do not have permission to create users.'
                }
                return response_object, 403
            else:
                user = User.query.filter_by(id=other_user_id).first()
        else:
            user = User.query.filter_by(
                id=User.decode_auth_token(auth_token)).first()

        if user is None:
            response_object = {'status': 'fail',
                               'message': 'User does not exist'}
            return response_object, 404

        try:
            validated_data = self.validator.load(post_data)
        except ValidationError as err:
            response_object = {
                'status': 'fail',
                'message': 'The posted data is not valid!',
                'errors': err.messages
            }
            return response_object, 400

        for attribute in validated_data:
            setattr(user, attribute, validated_data[attribute])

        new_password = post_data.get('password')
        if new_password:
            user.regenerate_password_hash(new_password)

        try:
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            # TODO: Probably remove dev_message
            response_object = {
                'status': 'fail',
                'message': 'Username already taken!',
                'dev_message': str(e.orig)
            }
            return response_object, 400

        response_object = {
            'status': 'success',
            'data': user.to_json()
        }
        return response_object, 200

    @create_context
    @login_required
    def delete(self, auth_token, local_data=None):
        response_object = {
            'status': None,
            'message': None
        }

        if not g.user.is_admin:
            response_object = {
                'status': 'fail',
                'message': 'You are not authorized to delete users.'
            }
            return response_object, 403

        if not local_data:
            delete_data = request.get_json()
        else:
            delete_data = json.loads(local_data)

        id_to_delete = delete_data.get('id_to_delete')

        if not id_to_delete:
            response_object = {
                'status': 'fail',
                'message': 'unable to delete user without user id'
            }
            return response_object, 403

        user = User.query.filter_by(id=id_to_delete).first()
        if not user:
            response_object = {
                'status': 'fail',
                'message': 'user not found'
            }
            return response_object, 404

        if user.is_admin:
            response_object = {
                'status': 'fail',
                'message': 'Admin users cannot be deleted.'
            }
            return response_object, 403

        if (user.creator_id != g.user.id):
            response_object = {
                'status': 'fail',
                'message': 'You are not authorized to delete this user.'
            }
            return response_object, 403

        db.session.delete(user)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'user successfully deleted'
        }
        return response_object, 200


class UserList(Resource):

    def __init__(self):
        self.validator = UserValidator()
        super(UserList, self).__init__()

    @create_context
    @login_required
    def get(self, local_args=None):
        """Endpoint for getting a list of users an admin user has created.

        :param dict local_args: This should be used in place of the QUERY PARAMS
            that would be used through HTTP, used for local calls.

        :returns: response_object, status_code
        :rtype: tuple (dict, int)
        """
        response_object = {}
        if not local_args:
            query_limit = request.args.get('limit')
            no_admin = request.args.get('no_admin')
        else:
            query_limit = local_args.get('limit')
            no_admin = local_args.get('no_admin')

        if no_admin:  # Fetch ALL users
            users = User.query.order_by(User.id).limit(query_limit).all()
        else:  # Fetch ONLY users created by the user calling this endpoint
            users = User.query.filter_by(creator_id=g.user.id).all()

        response_object = {
            'status': 'success',
            'data': {'users': [user.to_json() for user in users]}
        }

        return response_object, 200

    @create_context
    @login_required
    def post(self, local_data=None):
        """Endpoint for creating a new user. WARNING: This currently should not
        be used for local calls, since it references flasks g.user which will
        only be set to a valid user when requests are made over http, refer to login_required decorator in
        groundstation.backend_api.utils. If you want to make a new user, its probably best to just make a new User object
        and save it in a shell.

        :param json_string local_data: This should be used in place of the POST body that would be used through HTTP, used for local calls.

        :returns: response_object, status_code
        :rtype: tuple (dict, int)
        """
        if not g.user.is_admin:
            response_object = {
                'status': 'fail',
                'message': 'You do not have permission to create users.'
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

        new_user = User(**validated_data, creator_id=g.user.id)
        try:
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            # TODO: Probably remove dev_message
            response_object = {
                'status': 'fail',
                'message': 'User already exists!',
                'dev_message': str(e.orig)
            }
            return response_object, 400

        response_object = {
            'status': 'success',
            'message': 'User was successfully added',
            'data': new_user.to_json()
        }
        return response_object, 201


api.add_resource(UserList, '/api/users')
api.add_resource(UserEntity, '/api/users/<auth_token>')
