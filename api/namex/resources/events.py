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


from namex.models import Event as EventDAO, Request as RequestDAO, User

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

        event = EventDAO.query.filter_by(nrId = request_id).order_by("id").first_or_404().json()
        if not "id" in event:
            return jsonify({"message": "No events for NR:{} not found".format(nr)}), 404

        event_results = EventDAO.query.filter_by(nrId=request_id).order_by("id").limit(3)

        e_dict_previous = dict()
        e_txn_history = dict()
        i=0

        for e in event_results:

            e_dict = e.json()
            user_action = ""
            user_name = ""

            user = User.query.filter_by(id=e_dict['userId']).first().json()

            if e_dict["action"] == "update_from_nro" and e_dict["stateCd"] == "DRAFT":
                user_action = "Select from Draft Queue"
            if e_dict["action"] == "patch" and  e_dict["stateCd"] == "INPROGRESS":
                user_action = "Load NR"
            if e_dict["action"] == "patch" and e_dict["stateCd"] == "HOLD":
                user_action = "Hold Request"
            if e_dict["action"] == "marked_on_hold" and e_dict["stateCd"] == "HOLD":
                user_action = "Marked on Hold"
            if e_dict["action"] == "put" and e_dict["stateCd"] == "INPROGRESS" and  "additional" in e_dict["jsonData"]:
                if not e_dict_previous or (e_dict_previous["stateCd"] == "HOLD" or e_dict_previous["stateCd"] == "DRAFT" or e_dict_previous["stateCd"] == "INPROGRESS"):
                    user_action = "Edit NR Details"
                if e_dict_previous and e_dict_previous["stateCd"] == "APPROVED" or e_dict_previous["stateCd"]=="REJECTED" or e_dict_previous["stateCd"] == "CONDITIONAL":
                    if '"furnished": "Y"' in e_dict["jsonData"]:
                        user_action = "Reset"
                    else:
                        user_action = "Re-Open"
            if e_dict["action"] == "put" and (e_dict["stateCd"] == "APPROVED" or e_dict["stateCd"] == "REJECTED" or e_dict["stateCd"] == "CONDITIONAL"):
                user_action = "Edit NR Details after Completion"

            if e_dict["action"] == "put" and e_dict["stateCd"] == "INPROGRESS" and  "additional" not in e_dict["jsonData"] and '"state": "NE"' not in  e_dict["jsonData"]:
                user_action = "Complete the Name Choice"
            if e_dict["action"] == "patch" and (e_dict["stateCd"]== "APPROVED" or e_dict["stateCd"] == "REJECTED" or e_dict["stateCd"] == "CONDITIONAL"):
                user_action = "Decision"
            if e_dict["action"] == "put" and e_dict["stateCd"] == "INPROGRESS" and  "additional" not in e_dict["jsonData"] and  '"state": "NE"' in  e_dict["jsonData"]:
                user_action = "Undo Decision"
            if e_dict["action"] == "nro_update" and (e_dict["stateCd"]== "APPROVED" or e_dict["stateCd"] == "REJECTED" or e_dict["stateCd"] == "CONDITIONAL"):
                user_action = "Updated NRO"
            if e_dict["action"] == "post" and "comment" in e_dict["jsonData"]:
                user_action = "Staff Comment"

            e_dict_previous = e_dict
            e_dict["user_action"] = user_action
            e_dict["user_name"] = user["username"]

            i=i+1
            e_txn_history[i] = {}
            e_txn_history[i] = e_dict

        rep = {'response': {'count':i},
               'transactions': e_txn_history
              }

        return jsonify(rep), 200