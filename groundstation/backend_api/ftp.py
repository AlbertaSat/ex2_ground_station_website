import json
import os

from flask import request, Blueprint
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from sqlalchemy import desc

from groundstation import db
from groundstation.backend_api.models import FTPUpload
from groundstation.backend_api.utils import create_context, dynamic_filters_ftpuploads, login_required

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
            filepath=filepath,
            filename=file.filename,
            filesize=round(os.stat(filepath).st_size / 1024)
        )
        db.session.add(ftp_upload)
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': f'{filename} was successfully queued for upload!'
        }
        return response_object, 201

    @create_context
    def get(self, local_data=None):
        if not local_data:
            args = dynamic_filters_ftpuploads(request.args)
        else:
            args = dynamic_filters_ftpuploads(local_data)

        response_object = {
            'status': 'fail',
            'messages': 'no available uploads'
        }

        uploads = FTPUpload.query.filter(
            *args).order_by(desc(FTPUpload.upload_date))
        if not uploads:  # nothing has been uploaded yet
            response_object.update({'data': [], 'status': 'success'})
            return response_object, 200
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'uploads': [u.to_json() for u in uploads]
                }
            }
            return response_object, 200

    @create_context
    @login_required
    def patch(self, file_id, local_data=None):
        if not local_data:
            post_data = request.get_json()
        else:
            post_data = json.loads(local_data)

        file = FTPUpload.query.filter_by(id=file_id).first()

        if not file:
            response_object = {'status': 'fail',
                               'message': 'File upload does not exist!'}
            return response_object, 404

        file.uploaded = post_data['uploaded']
        file.upload_date = post_data['upload_date']
        db.session.commit()

        response_object = {
            'status': 'success',
            'data': file.to_json()
        }

        return response_object, 200


api.add_resource(FTPUploadAPI, '/api/ftpupload')
