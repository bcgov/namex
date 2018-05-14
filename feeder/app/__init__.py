# -*- coding: utf-8 -*-
"""NAMEX Feeder service

This module loads an incoming NR into the NAMEX DB

TODO:  Migrate to using the namex-api service to create a new name, needs auth, etc. first
"""
import logging
from flask import Flask, current_app, request, jsonify
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from config import Config

db = SQLAlchemy()

application = Flask(__name__, instance_relative_config=True)
application.config.from_object(Config)
db.init_app(application)

api = Api(application, prefix='/api/v1')

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

# declared after db is created, to avoid circular dependencies (which are bad)
from app.models import NRORequestSubmission, User, Request as DAORequest, Name

@api.route('/nro-requests', methods=['POST', 'OPTIONS'])
class Request(Resource):
    a_request = api.model('Request', {'nameRequest': fields.String('A valid NR that exists in NRO')})

    @api.expect(a_request)
    def post(self, *args, **kwargs):
        json_input = request.get_json()
        if not json_input:
            return {"message": "No input data provided"}, 400

        nr = json_input['nameRequest']
        logging.log(logging.INFO, 'uri:{}'.format(current_app.config['SQLALCHEMY_DATABASE_URI']))
        logging.log(logging.INFO, 'uri:{}'.format(current_app.config['SQLALCHEMY_BINDS']))

        try:
            nro_nr = NRORequestSubmission.query.filter_by(nr_num=nr).one()

            user = User.find_by_username(current_app.config['NRO_SERVICE_ACCOUNT'])

            new_nr = clone_nr(nro_nr)
            new_nr.userId = user.id

            add_names (new_nr, nro_nr)

            db.session.add(new_nr)
            db.session.commit()

        except exc.SQLAlchemyError as err:
            logging.log(logging.ERROR, 'SQLError nr:{0} error:{1}'.format(nr, err))
            return {"error": "Unable to clone:{}".format(nr)}, 500

        except Exception as err:
            logging.log(logging.ERROR, 'Exception nr:{0} error:{1}'.format(nr, err))
            return {"error": "Exception nr:{0}".format(nr
                                                       )}, 500

        return {"message": "cloned:{}".format(nr)}, 201


if __name__ == "__main__":
    application.run()

def clone_nr(nro_nr):
    new_nr = DAORequest()
    new_nr.nrNum = nro_nr.nr_num
    new_nr.applicant = nro_nr.applicant
    new_nr.phoneNumber = nro_nr.phone_number
    new_nr.adminComment = nro_nr.admin_comment
    new_nr.contact = nro_nr.contact
    new_nr.abPartner = nro_nr.ab_partner
    new_nr.skPartner = nro_nr.sk_partner
    new_nr.requestId = nro_nr.request_id
    new_nr.requestTypeCd = nro_nr.request_type_cd
    new_nr.priorityCd = nro_nr.priority_cd
    new_nr.tilmaInd = nro_nr.tilma_ind
    new_nr.tilmaTransactionId = nro_nr.tilma_transaction_id
    new_nr.xproJurisdiction = nro_nr.xpro_jurisdiction
    new_nr.additionalInfo = nro_nr.additional_info
    new_nr.natureBusinessInfo = nro_nr.nature_business_info
    new_nr.userNote = nro_nr.user_note
    new_nr.nuansNum = nro_nr.nuans_num
    new_nr.nuansExpirationDate = nro_nr.nuans_expiration_date
    new_nr.assumedNuansNum = nro_nr.assumed_nuans_num
    new_nr.assumedNuansName = nro_nr.assumed_nuans_name
    new_nr.assumedNuansExpirationDate = nro_nr.assumed_nuans_expiration_date
    new_nr.lastNuansUpdateRole = nro_nr.last_nuans_update_role
    return new_nr

def add_names (to_nr, from_nr):
    f_names = from_nr.all_names()
    for f_name in f_names:
        new_name = Name()
        new_name.name = f_name.name
        new_name.choice = f_name.choice
        new_name.consumptionDate = f_name.consumption_date
        new_name.state = f_name.state
        new_name.remoteNameId = f_name.name_instance_id

        # add the new name to the to_nr
        to_nr.names.append(new_name)
