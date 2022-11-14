import os

from flask import request, Blueprint
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

from groundstation import db
from groundstation.backend_api.models import FTPUpload
from groundstation.backend_api.utils import create_context, login_required

ftp_blueprint = Blueprint('ftp', __name__)
api = Api(ftp_blueprint)

BASEDIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = '.ftpTransactions/Uploads'


class FTPUploadAPI(Resource):

    def __init__(self) -> None:
        # TODO: Make validator
        super().__init__()

    @create_context
    @login_required
    def post(self):
        """Endpoint for uploading a file

        :returns: response_object, status_code
        :rtype: tuple (dict, int)
        """
        file = request.files['file']
        if not file:
            response_object = {
                'status': 'fail',
                'message': 'No file in request'
            }
            return response_object, 400

        if file.filename == '':
            response_object = {
                'status': 'fail',
                'message': 'Filename is empty'
            }
            return response_object, 400

        # Save file locally
        filename = secure_filename(file.filename)
        filepath = os.path.join(BASEDIR, '..', '..', UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Queue up for satellite upload
        ftp_upload = FTPUpload(
            filepath=filepath
        )
        db.session.add(ftp_upload)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': f'{filename} was successfully queued for upload!'
        }
        return response_object, 201


api.add_resource(FTPUploadAPI, '/api/ftpupload')
