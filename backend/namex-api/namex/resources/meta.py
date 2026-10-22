from flask import jsonify
from flask_restx import Namespace, Resource

from namex.utils.run_version import get_run_version

api = Namespace('API Version', description='Namex - Metadata')


@api.route('/info')
class Info(Resource):
    @staticmethod
    @api.doc(
        description='Fetch the currently running version of the Name Request API',
        responses={
            200: 'Version info fetched successfully',
            500: 'Internal server error',
        },
    )
    def get():
        return jsonify(API='NameX/{ver}'.format(ver=get_run_version()))
