from flask import jsonify
from flask_restplus import Resource, Namespace
from namex.utils.run_version import get_run_version

api = Namespace('nameRequestMeta', description='Name Request System - Metadata')


@api.route("/info")
class Info(Resource):

    @staticmethod
    def get():
        return jsonify(API="NameX/{ver}".format(ver=get_run_version()))
