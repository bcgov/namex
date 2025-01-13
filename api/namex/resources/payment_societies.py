import copy
from flask import request, jsonify, current_app, make_response
from flask_restx import Namespace, cors
from namex.resources.name_requests.abstract_nr_resource import AbstractNameRequestResource
from sqlalchemy.orm.exc import NoResultFound

from namex import jwt
from namex.models import State, PaymentSociety as PaymentSocietyDAO, Request as RequestDAO, User
from namex.utils.auth import cors_preflight

from namex.utils.logging import setup_logging
setup_logging()  # important to do this first

# Register a local namespace for the payment_society
api = Namespace('payment_society', description='Store data for society from home legancy app')


@cors_preflight('GET')
@api.route('/<string:nr>', methods=['GET', 'OPTIONS'])
class PaymentSocietiesSearch(AbstractNameRequestResource):
    
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
            nr_payment_society_info['payment_completion_date'] = ps.paymentCompletionDate
            nr_payment_society_info['payment_status_code'] = ps.paymentStatusCode
            nr_payment_society_info['payment_fee_code'] = ps.paymentFeeCode
            nr_payment_society_info['payment_type'] = ps.paymentType
            nr_payment_society_info['payment_amount'] = ps.paymentAmount
            nr_payment_society_info['payment_json'] = ps.paymentJson
            nr_payment_society_info['payment_action'] = ps.paymentAction
            
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
class PaymentSocieties(AbstractNameRequestResource):
    @cors.crossdomain(origin='*')
    @jwt.has_one_of_roles([User.APPROVER, User.EDITOR, User.SYSTEM])
    def post(self):
        # do the cheap check first before the more expensive ones
        try:
            json_input = request.get_json()
            if not json_input:
                return make_response(jsonify({'message': 'No input data provided'}), 400)
            current_app.logger.debug(f'Request Json: {json_input}')
            
            nr_num = json_input.get('nrNum', None)
            if not nr_num:
                return make_response(jsonify({"message": "nr_num not set in json input"}), 406)

            nrd = RequestDAO.find_by_nr(nr_num)
            if not nrd:
                return make_response(jsonify({"message": "Request: {} not found in requests table".format(nr_num)}), 404)

            # replacing temp NR number to a formal NR number if needed.
            nrd = self.add_new_nr_number(nrd, False)
            current_app.logger.debug(f'Formal NR nubmer is: {nrd.nrNum}')
        except NoResultFound as nrf:
            # not an error we need to track in the log
            return make_response(jsonify({"message": "Request: {} not found".format(nr_num)}), 404)
        except Exception as err:
            current_app.logger.error("Error when posting NR: {0} Err:{1} Please double check the json input file format".format(nr_num, err))
            return make_response(jsonify({"message": "NR had an internal error. Please double check the json input file format"}), 404)

        ps_instance = PaymentSocietyDAO()        
        ps_instance.nrNum = nrd.nrNum
        ps_instance.corpNum = json_input.get('corpNum', None)
        ps_instance.paymentCompletionDate = json_input.get('paymentCompletionDate', None)
        ps_instance.paymentStatusCode = json_input.get('paymentStatusCode', None)
        ps_instance.paymentFeeCode = json_input.get('paymentFeeCode', None)
        ps_instance.paymentType = json_input.get('paymentType', None)
        ps_instance.paymentAmount = json_input.get('paymentAmount', None)
        ps_instance.paymentJson = json_input.get('paymentJson', None)
        ps_instance.paymentAction = json_input.get('paymentAction', None)

        ps_instance.save_to_db()
        current_app.logger.debug(f'ps_instance saved...')

        if nrd.stateCd == State.PENDING_PAYMENT:
            nrd.stateCd = 'DRAFT'
        nrd.save_to_db()
        current_app.logger.debug(f'nrd saved...')
        
        return make_response(jsonify(ps_instance.json()), 200)     
    
    
    
    
