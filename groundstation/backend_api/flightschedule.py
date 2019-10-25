from flask import Blueprint
from flask_restful import Resource, Api

from groundstation import db
from groundstation.backend_api.utils import create_context

flightschedule_blueprint = Blueprint('flightschedule', __name__)
api = Api(flightschedule_blueprint)