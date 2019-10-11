from flask import Blueprint
from flask_restful import Resource, Api
from groundstation.api.models import Housekeeping

housekeeping_blueprint = Blueprint('housekeeping', __name__)
api = Api(housekeeping_blueprint)

class HousekeepingLog(Resource):
	def get(self, housekeeping_id):
		"""Get a single housekeeping log via its id"""
		housekeeping = Housekeeping.query.filter_by(id=housekeeping_id).first()
		response_object = {
			'status': 'success',
			'data' : housekeeping.toJson()
		}

		return response_object, 200

api.add_resource(HousekeepingLog, '/housekeepinglog/<housekeeping_id>')
