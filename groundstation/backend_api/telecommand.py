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

from groundstation.backend_api.models import Housekeeping
from groundstation import db
from groundstation.backend_api.utils import create_context

telecommand_blueprint = Blueprint('telecommand', __name__)
api = Api(telecommand_blueprint)

