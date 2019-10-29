from flask import request
from flask import Blueprint
from flask_restful import Resource, Api
from datetime import datetime
import json

from groundstation import db
from groundstation.backend_api.models import Passover
from groundstation.backend_api.utils import create_context

passover_blueprint = Blueprint('passover', __name__)
api = Api(housekeeping_blueprint)

class Passover(Resource):

    @create_context
    def get(self, passover_id):
        pass

    @create_context
    def post(self):
        pass

class PassoverList(Resource):

    @create_context
    def get(self):
        pass

    @create_context
    def post(self):
        pass
