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

    def __init__(self):
        self.validator = PassoverListValidator()
        super(PassoverList, self).__init__()

    @create_context
    def get(self, local_args=None):
        if not local_args:
            query_limit = request.args.get('limit')
            next_only = request.args.get('next-only')
        else:
            query_limit = local_args.get('limit')
            next_only = local_args.get('next-only')

        if next_only == 'true':
            # ignore for now
            current_time = datetime.datetime.now(datetime.timezone.utc)
            passovers = [Passover.query.filter(Passover.timestamp > current_time).order_by(Passover.timestamp).limit(query_limit).first()]
            passovers = [] if passovers[0] is None else passovers
        else:
            passovers = Passover.query.order_by(Passover.timestamp).limit(query_limit).all()

        response_object = {
            'status':'success',
            'data': {
                'passovers':[p.to_json() for p in passovers]
            }
        }
        return response_object, 200

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
