from flask import jsonify
from flask_restx import Namespace, Resource

from namex.utils.run_version import get_run_version

api = Namespace('namexRequestMeta', description='Namex - Metadata')


@api.route('/info')
class Info(Resource):
    @staticmethod
    def get():
        return jsonify(API='NameX/{ver}'.format(ver=get_run_version()))
