from flask import request
from flask import Blueprint
from flask_restful import Resource, Api
from marshmallow import ValidationError
import datetime
import json

from groundstation import db
from groundstation.backend_api.models import Passover
from groundstation.backend_api.validators import PassoverListValidator
from groundstation.backend_api.utils import create_context, login_required

passover_blueprint = Blueprint('passover', __name__)
api = Api(passover_blueprint)

class PassoverList(Resource):
    """Endpoint for getting and receiving Passovers
    """

    def __init__(self):
        self.validator = PassoverListValidator()
        super(PassoverList, self).__init__()

    @create_context
    def get(self, local_args=None):
        """Endpoint for getting a list of passovers

        :param dict local_args: This should be used in place of the QUERY PARAMS that would be used through HTTP, used for local calls.

        :returns: response_object, status_code
        :rtype: tuple (dict, int)
        """
        response_object = {
            'status':'success',
            'data':{}
        }
        if not local_args:
            query_limit = request.args.get('limit')
            next = request.args.get('next')
            most_recent = request.args.get('most-recent')
        else:
            query_limit = local_args.get('limit')
            next = local_args.get('next')
            most_recent = local_args.get('most-recent')

        current_time = datetime.datetime.now(datetime.timezone.utc)
        if next == 'true':
            passovers = Passover.query.filter(Passover.timestamp > current_time).order_by(Passover.timestamp).limit(query_limit)
            next_passovers = [p.to_json() for p in passovers]
            response_object['data']['next_passovers'] = next_passovers
        if most_recent == 'true':
            passover = Passover.query.filter(Passover.timestamp < current_time).order_by(Passover.timestamp.desc()).limit(query_limit).first()
            passover = passover.to_json() if passover is not None else passover
            response_object['data']['most_recent_passover'] = passover

        if next != 'true' and most_recent != 'true':
            passovers = Passover.query.order_by(Passover.timestamp).limit(query_limit).all()
            response_object['data']['passovers'] = [p.to_json() for p in passovers]

        return response_object, 200

    @create_context
    @login_required
    def post(self, local_data=None):
        """Endpoint for creating a new passover

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

        passovers = validated_data['passovers']
        for passover in passovers:
            p = Passover(**passover)
            db.session.add(p)

        db.session.commit()

        response_object = {
            'status':'success',
            'message':'Passovers were successfully created'
        }
        return response_object, 201

api.add_resource(PassoverList, '/api/passovers')
