from flask import jsonify
from flask_restplus import Resource, Namespace, cors
from namex.utils.auth import cors_preflight
from namex import jwt

from namex.utils.logging import setup_logging
setup_logging() ## important to do this first

from namex.models import Event as EventDAO, Request as RequestDAO, User,  State

# Register a local namespace for the event history
api = Namespace('events', description='Audit trail of events for a Name Request')
@cors_preflight("GET")
@api.route('/<string:nr>', methods=['GET','OPTIONS'])
class Events(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.has_one_of_roles([User.APPROVER, User.EDITOR])
    def get(nr):
        nrd = RequestDAO.query.filter_by(nrNum=nr.upper()).first_or_404().json()
        request_id = 0
        if "id" in nrd:
            request_id = nrd["id"]
        if not request_id:
            return jsonify({"message": "Request NR:{} not found".format(nr)}), 404

        event = EventDAO.query.filter_by(nrId = request_id).order_by("id").first_or_404().json()
        if not "id" in event:
            return jsonify({"message": "No events for NR:{} not found".format(nr)}), 404

        event_results = EventDAO.query.filter_by(nrId=request_id).order_by("id").all()

        e_dict_previous = dict()
        e_txn_history = dict()
        i=0

        for e in event_results:

            e_dict = e.json()
            user_action = ""
            user_name = ""

            user = User.query.filter_by(id=e_dict['userId']).first().json()

            if e_dict["action"] == "update_from_nro" and ( e_dict["stateCd"] == State.INPROGRESS or e_dict["stateCd"] == State.DRAFT):
                user_action =  "Get NR Details from NRO"
            if e_dict["action"] == "get" and e_dict["stateCd"] == State.INPROGRESS:
                user_action = "Get Next NR"
            if e_dict["action"] == "patch" and  e_dict["stateCd"] == State.INPROGRESS:
                user_action = "Load NR"
            if e_dict["action"] == "patch" and e_dict["stateCd"] == State.HOLD:
                user_action = "Hold Request"
            if e_dict["action"] == "marked_on_hold" and e_dict["stateCd"] == State.HOLD:
                user_action = "Marked on Hold"
            if e_dict["action"] == "put" and e_dict["stateCd"] == State.DRAFT:
                user_action = "Edit NR Details"
            if e_dict["action"] == "put" and e_dict["stateCd"] == State.INPROGRESS and  "additional" in e_dict["jsonData"]:
                if len(e_dict_previous) == 0 or (e_dict_previous["stateCd"] == State.HOLD or e_dict_previous["stateCd"] == State.DRAFT or e_dict_previous["stateCd"] == State.INPROGRESS):
                    user_action = "Edit NR Details"
                if e_dict_previous and e_dict_previous["stateCd"] == State.APPROVED or e_dict_previous["stateCd"]==State.REJECTED or e_dict_previous["stateCd"] == State.CONDITIONAL:
                    if '"furnished": "Y"' in e_dict["jsonData"]:
                        user_action = "Reset"
                    else:
                        user_action = "Re-Open"
            if e_dict["action"] == "put" and (e_dict["stateCd"] == State.APPROVED or e_dict["stateCd"] == State.REJECTED or e_dict["stateCd"] == State.CONDITIONAL):
                user_action = "Edit NR Details after Completion"
            if e_dict["action"] == "put" and e_dict["stateCd"] == State.INPROGRESS and  "additional" not in e_dict["jsonData"] and '"state": "NE"' not in  e_dict["jsonData"]:
                user_action = "Complete the Name Choice"
            if e_dict["action"] == "patch" and (e_dict["stateCd"]== State.APPROVED or e_dict["stateCd"] == State.REJECTED or e_dict["stateCd"] == State.CONDITIONAL):
                user_action = "Decision"
            if e_dict["action"] == "put" and e_dict["stateCd"] == State.INPROGRESS and  "additional" not in e_dict["jsonData"] and  '"state": "NE"' in  e_dict["jsonData"]:
                user_action = "Undo Decision"
            if e_dict["action"] == "nro_update" and (e_dict["stateCd"]== State.APPROVED or e_dict["stateCd"] == State.REJECTED or e_dict["stateCd"] == State.CONDITIONAL):
                user_action = "Updated NRO"
            if e_dict["action"] == "post" and "comment" in e_dict["jsonData"]:
                user_action = "Staff Comment"
            if  e_dict["stateCd"] == State.CANCELLED and (e_dict["action"] == "post" or e_dict["action"] == "update_from_nro"):
                user_action = "Cancelled in NRO"
            if e_dict["stateCd"] == State.CANCELLED and (e_dict["action"] == "patch" or e_dict["action"] == "put"):
                user_action = "Cancelled in Namex"
            if e_dict["stateCd"] == State.EXPIRED and e_dict["action"] == "post":
                user_action = "Expired by NRO"
            if e_dict["stateCd"] == State.HISTORICAL and e_dict["action"] == "post":
                user_action = "Set to Historical by NRO(Migration)"
            if e_dict["stateCd"]==State.COMPLETED and (e_dict["action"] == "post" or e_dict["action"] == "update_from_nro"):
                user_action = "Migrated by NRO"

            e_dict_previous = e_dict
            e_dict["user_action"] = user_action
            e_dict["user_name"] = user["username"]

            i=i+1
            e_txn_history[i] = {}
            e_txn_history[i] = e_dict

        if i==0:
            return jsonify({"message": "No valid events for NR:{} found".format(nr)}), 404

        rep = {'response': {'count':i},
               'transactions': e_txn_history
              }

        return jsonify(rep), 200