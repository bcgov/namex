import copy, json
import json
from flask import request, jsonify, g, current_app, make_response
from flask_restx import Resource, Namespace, cors
from sqlalchemy.orm.exc import NoResultFound

from namex import jwt
from namex.models import PaymentSociety as PaymentSocietyDAO, Request as RequestDAO, User
from namex.utils.auth import cors_preflight

from namex.utils.logging import setup_logging
setup_logging()  # important to do this first

# Register a local namespace for the payment_society
api = Namespace('payment_society', description='Store data for society from home legancy app')


@cors_preflight('GET')
@api.route('/<string:nr>', methods=['GET', 'OPTIONS'])
class PaymentSocietiesSearch(Resource):
    
    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.has_one_of_roles([User.APPROVER, User.EDITOR, User.SYSTEM])
    def get(nr):        
        try:
            current_app.logger.debug(nr)
            nrd = RequestDAO.query.filter_by(nrNum=nr).first()
            if not nrd:
                return make_response(jsonify({"message": "Request: {} not found in requests table".format(nr)}), 404)
        except NoResultFound as nrf:
            # not an error we need to track in the log
            return make_response(jsonify({"message": "Request: {} not found in requests table".format(nr)}), 404)
        except Exception as err:
            current_app.logger.error("Error when getting NR: {0} Err:{1}".format(nr, err))
            return make_response(jsonify({"message": "NR had an internal error"}), 404)
        
        try:
            psd = PaymentSocietyDAO.query.filter_by(nrNum=nr).first()
            if not psd:
                return make_response(jsonify({"message": "Request: {} not found in payment_societies table".format(nr)}), 404)
        except NoResultFound as nrf:
            # not an error we need to track in the log
            return make_response(jsonify({"message": "Request: {0} not found in payment_societies table, Err:{1}".format(nr, nrf)}), 404)
        except Exception as err:
            current_app.logger.error("Error when patching NR:{0} Err:{1}".format(nr, err))
            return make_response(jsonify({"message": "NR had an internal error"}), 404)

        paymentSociety_results = PaymentSocietyDAO.query.filter_by(nrNum=nr).order_by("id").all()

        # info needed for each payment_society
        nr_payment_society_info = {}
        payment_society_txn_history = []

        for ps in paymentSociety_results:               
            nr_payment_society_info['id'] = ps.id
            nr_payment_society_info['nr_num'] = ps.nrNum
            nr_payment_society_info['corp_num'] = ps.corpNum
            nr_payment_society_info['request_state'] = ps.requestState
            nr_payment_society_info['payment_state'] = ps.paymentState
            nr_payment_society_info['paymentDate'] = ps.paymentDate
            nr_payment_society_info['payment_json'] = ps.paymentJson
            
            payment_society_txn_history.insert(0, copy.deepcopy(nr_payment_society_info))
            
        if len(payment_society_txn_history) == 0:
            return make_response(jsonify({ 'message': f'No valid payment societies for {nr} found'}), 404)

        resp = {
            'response': { 'count': len(payment_society_txn_history) },
            'transactions': payment_society_txn_history
        }

        return make_response(jsonify(resp), 200)
    
 
@cors_preflight('POST')
@api.route('', methods=['POST', 'OPTIONS'])
class PaymentSocieties(Resource): 
    
    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.has_one_of_roles([User.APPROVER, User.EDITOR, User.SYSTEM])
    def post(*args, **kwargs):
        # do the cheap check first before the more expensive ones
        
        try:
            json_input = request.get_json()
            if not json_input:
                return make_response(jsonify({'message': 'No input data provided'}), 400)
            current_app.logger.debug(json_input)
            
            nr_num = json_input.get('nrNum', None)
            if not nr_num:
                return make_response(jsonify({"message": "nr_num not set in json input"}), 406)
                        
            paymentStateType = json_input.get('paymentStateType', None)
            if not paymentStateType:
                return make_response(jsonify({"message": "paymentStateType not set in json input"}), 406)
            
            payment_json = json_input.get('payment', None)
            if not payment_json:
                return make_response(jsonify({"message": "payment not set in json input"}), 406)
            
            paymentDate = payment_json.get('paymentDate', None)
            if not paymentDate:
                return make_response(jsonify({"message": "paymentDate not set in json input"}), 406)

            nrd = RequestDAO.find_by_nr(nr_num)
            if not nrd:
                return make_response(jsonify({"message": "Request: {} not found in requests table".format(nr_num)}), 404)
        except NoResultFound as nrf:
            # not an error we need to track in the log
            return make_response(jsonify({"message": "Request: {} not found".format(nr_num)}), 404)
        except Exception as err:
            current_app.logger.error("Error when posting NR: {0} Err:{1} Please double check the json input file format".format(nr_num, err))
            return make_response(jsonify({"message": "NR had an internal error. Please double check the json input file format"}), 404)

        user = User.find_by_jwtToken(g.jwt_oidc_token_info)
        if user is None:
            return make_response(jsonify({'message': 'No User'}), 404)                 
         
        ps_instance = PaymentSocietyDAO()        
        ps_instance.nrNum = nr_num
        ps_instance.corpNum = nrd.corpNum
        ps_instance.requestState = nrd.stateCd
        ps_instance.paymentState = paymentStateType
        ps_instance.paymentDate = paymentDate
        ps_instance.paymentJson = json.dumps(json_input) 

        ps_instance.save_to_db()
        
        return make_response(jsonify(ps_instance.json()), 200)     
    
    
    
    
