from flask import jsonify, request
from flask_restplus import Resource, Namespace, cors
from namex.utils.util import cors_preflight
import json
from namex import jwt
from flask import current_app
from namex.models import db

from namex.utils.logging import setup_logging
setup_logging() ## important to do this first

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func, text
from sqlalchemy.inspection import inspect


from namex.models import Event as EventDAO, Request as RequestDAO,  User

import datetime
from datetime import datetime as dt


# Register a local namespace for the event history
api = Namespace('Events', description='Audit trail of events for a name request')
@cors_preflight("GET")
@api.route('/<string:nr>', methods=['GET','OPTIONS'])
class Events(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.has_one_of_roles([User.APPROVER, User.EDITOR])
    def get(nr):
        # return jsonify(request_schema.dump(RequestDAO.query.filter_by(nr=nr.upper()).first_or_404()))
        #return jsonify(RequestDAO.query.filter_by(nrNum=nr.upper()).first_or_404().json())
        nrd = RequestDAO.query.filter_by(nrNum=nr.upper()).first_or_404().json()
        request_id = 0
        if "id" in nrd:
            request_id = nrd["id"]
        if not request_id:
            return jsonify({"message": "Request NR:{} not found".format(nr)}), 404
        #return jsonify({"message": "id type:{}".format(type(request_id))}), 200
        event_results = EventDAO.query.filter_by(nrId = request_id).first_or_404()
        return jsonify(event_results.json()), 200

