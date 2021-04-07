from flask import jsonify, g, current_app
from flask_restplus import Resource, cors
from flask_jwt_oidc import AuthError

from app import api, db, app, jwt
from app.auth_services import required_scope
from app.utils.util import cors_preflight
from sqlalchemy import text, exc
import logging


@api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

@cors_preflight("GET")
@api.route('/corporations/echo', methods=['GET', 'OPTIONS'])
class Echo(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def get (*args, **kwargs):
        try:
            return jsonify(g.jwt_oidc_token_info), 200
        except Exception as err:
            return jsonify({"error": "{}".format(err)}), 500


@cors_preflight("GET")
@api.route('/corporations/<string:corp_num>', methods=['GET', 'OPTIONS'])
class RequestColin(Resource):
    """this gets the corporate details for the corporation specified
    """

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_roles(['names_viewer'])
    def get(corp_num):
        # logging.basicConfig(filename='info.log', level=logging.INFO)
        # logging.info('logging works')
        # who has access?
        if not (required_scope("names_viewer")):  # User.VIEWONLY
            return jsonify({"message": "Authentication error: You do not have the required user roles to view corp details."}), 403

        corp_num_sql = '\'' + corp_num + '\''

        incorp_info_sql = Methods.build_info_sql(corp_num_sql)
        incorp_addr_id_sql = Methods.build_addr_id_sql(corp_num_sql)
        incorp_directors_sql = Methods.build_directors_sql(corp_num_sql)

        try:
            incorp_nr_sql = Methods.build_nr_sql(corp_num_sql)
            incorp_nob = Methods.find_nob(incorp_nr_sql)
            incorp_info_dict,incorp_directors_obj = Methods.init_info(incorp_info_sql,incorp_directors_sql)
            incorp_class = incorp_info_dict['corp_class']

            if incorp_class == 'XPRO':

                incorp_jurisdiction_sql = Methods.build_jurisdiction_sql(corp_num_sql)
                incorp_attorneys_sql = Methods.build_attorneys_sql(corp_num_sql)

                incorp_head_office_obj, incorp_attorneys_obj, incorp_jurisdiction_obj = \
                    Methods.xpro_get_objs(incorp_addr_id_sql,incorp_attorneys_sql,incorp_jurisdiction_sql)

            # BC corp
            else:
                incorp_registered_addr_obj, incorp_records_addr_obj = Methods.bc_get_objs(incorp_addr_id_sql)

        except exc.SQLAlchemyError as err:
            print(err.with_traceback(None))
            current_app.logger.debug(err.with_traceback(None))
            return jsonify({"message": "Error occurred getting the corporation details"}), 500
        except AttributeError:
            return jsonify({"message": "Attribute error"}), 500
        except IndexError as err:
            current_app.logger.debug(err.with_traceback(None))
            return jsonify({"message": "Error: Could not find corporation details"}), 404
        except Exception as err:
            print(err.with_traceback(None))
            current_app.logger.debug(err.with_traceback(None))
            return jsonify({"message": "Unknown error occurred in colin-api"}), 500

        incorp_date = incorp_info_dict['recognition_dts']
        if incorp_date is not None:
            incorp_date_str = '{:0>4}-{:0>2}-{:0>2}'.format(incorp_date.year,incorp_date.month,incorp_date.day)
        else:
            incorp_date_str = 'Not Available'

        incorp_directors_list = []
        for row in incorp_directors_obj:
            incorp_directors_list.append(row[0])
        if any(incorp_directors_list):
            pass
        else:
            incorp_directors_list = 'Not Available'

        if incorp_class == 'XPRO':

            incorp_ho_addr_list, incorp_attorneys_list, incorp_jurisdiction = \
                Methods.xpro_get_vals(incorp_head_office_obj,incorp_attorneys_obj,incorp_jurisdiction_obj)

            corp_details_dict = {'incorp #': corp_num,
                                 'incorporated': incorp_date_str,
                                 'directors': incorp_directors_list,
                                 'attorney names': incorp_attorneys_list,
                                 'head office': incorp_ho_addr_list,
                                 'jurisdiction': incorp_jurisdiction,
                                 'nature of business': incorp_nob}
        else:
            incorp_registered_addr_list, incorp_records_addr_list = \
                Methods.bc_get_vals(incorp_registered_addr_obj,incorp_records_addr_obj)

            corp_details_dict = {'incorp #': corp_num,
                                 'incorporated': incorp_date_str,
                                 'directors': incorp_directors_list,
                                 'registered office delivery address': incorp_registered_addr_list,
                                 'records office delivery address': incorp_records_addr_list,
                                 'jurisdiction': 'BC',
                                 'nature of business': incorp_nob}

        return jsonify(corp_details_dict), 200


class Methods(Resource):
    @staticmethod
    def build_info_sql(corp_num_sql):
        return text("select * "
                    "from bc_registries.corp_num_dts_class_vw "
                    "where corp_num = {}".format(corp_num_sql))

    @staticmethod
    def build_directors_sql(corp_num_sql):
        return text("select "
                    "   CASE "
                    "       WHEN cp.middle_nme IS NOT NULL "
                    "           THEN cp.first_nme || ' '||cp.middle_nme|| ' '||cp.last_nme "
                    "       ELSE "
                    "           cp.first_nme || ' ' || cp.last_nme "
                    "       END director_name "
                    "from bc_registries.corp_party_vw cp "
                    "where cp.corp_num = {} and cp.end_event_id IS NULL and cp.party_typ_cd = 'DIR'".format(corp_num_sql))

    @staticmethod
    def build_addr_id_sql(corp_num_sql):
        return text("select delivery_addr_id "
                    "from bc_registries.office_vw "
                    "where corp_num={} "
                    "and end_event_id IS NULL "
                    "and delivery_addr_id IS NOT NULL;".format(corp_num_sql))

    @staticmethod
    def build_jurisdiction_sql(corp_num_sql):
        return text("select home_jurisdiction "
                    "from bc_registries.corp_jurs_vw "
                    "where corp_num = {}".format(corp_num_sql))

    @staticmethod
    def build_attorneys_sql(corp_num_sql):
        return text("select "
                    "   CASE "
                    "       WHEN cp.middle_nme IS NOT NULL "
                    "           THEN cp.first_nme || ' '||cp.middle_nme|| ' '||cp.last_nme "
                    "       ELSE "
                    "           cp.first_nme || ' ' || cp.last_nme "
                    "       END attorney_name "
                    "from bc_registries.corp_party_vw cp "
                    "where cp.corp_num = {} and cp.end_event_id IS NULL and cp.party_typ_cd = 'ATT'".format(corp_num_sql))

    @staticmethod
    def build_nr_sql(corp_num_sql):
        return text("select * "
                    "from bc_registries.corp_nr_num_vw "
                    "where corp_num = {};".format(corp_num_sql))

    @staticmethod
    def init_info(incorp_info_sql,incorp_directors_sql):
        try:
            incorp_info_obj = db.engine.execute(incorp_info_sql)
            incorp_info_dict = dict(incorp_info_obj.fetchall()[0])
        except IndexError:
            incorp_info_dict = {'corp_class': None,'recognition_dts': None}

        incorp_directors_obj = db.engine.execute(incorp_directors_sql)

        return incorp_info_dict,incorp_directors_obj

    @staticmethod
    def xpro_get_objs(incorp_addr_id_sql, incorp_attorneys_sql, incorp_jurisdiction_sql):
        incorp_ho_addr_id_obj = db.engine.execute(incorp_addr_id_sql)
        incorp_ho_addr_id = incorp_ho_addr_id_obj.fetchall()[0][0]
        incorp_ho_addr_id_sql = '\'' + str(incorp_ho_addr_id) + '\''
        incorp_ho_addr_sql = text("select addr_line_1, ADDR_LINE_2, ADDR_LINE_3, city, province, country_typ_cd, postal_cd "
                                  "from bc_registries.address_vw "
                                  "where addr_id= {} AND addr_id IS NOT NULL;".format(incorp_ho_addr_id_sql))
        incorp_head_office_obj = db.engine.execute(incorp_ho_addr_sql)

        incorp_attorneys_obj = db.engine.execute(incorp_attorneys_sql)
        incorp_jurisdiction_obj = db.engine.execute(incorp_jurisdiction_sql)

        return incorp_head_office_obj,incorp_attorneys_obj,incorp_jurisdiction_obj

    @staticmethod
    def bc_get_objs(incorp_addr_id_sql):
        incorp_addr_id_obj = db.engine.execute(incorp_addr_id_sql)
        incorp_addr_ids = incorp_addr_id_obj.fetchall()
        incorp_reg_addr_id = incorp_addr_ids[0][0]
        incorp_reg_addr_id_sql = '\'' + str(incorp_reg_addr_id) + '\''
        incorp_reg_addr_sql = text(
            "select addr_line_1, ADDR_LINE_2, ADDR_LINE_3, city, province, country_typ_cd, postal_cd "
            "from bc_registries.address_vw "
            "where addr_id= {} AND addr_id IS NOT NULL;".format(incorp_reg_addr_id_sql))
        incorp_registered_addr_obj = db.engine.execute(incorp_reg_addr_sql)
        try:
            incorp_rec_addr_id = incorp_addr_ids[1][0]
        except:
            incorp_records_addr_obj = None
        else:
            incorp_rec_addr_id_sql = '\'' + str(incorp_rec_addr_id) + '\''
            incorp_rec_addr_sql = text(
                "select addr_line_1, ADDR_LINE_2, ADDR_LINE_3, city, province, country_typ_cd, postal_cd "
                "from bc_registries.address_vw "
                "where addr_id= {} AND addr_id IS NOT NULL;".format(incorp_rec_addr_id_sql))
            incorp_records_addr_obj = db.engine.execute(incorp_rec_addr_sql)

        return incorp_registered_addr_obj,incorp_records_addr_obj

    @staticmethod
    def xpro_get_vals(incorp_head_office_obj,incorp_attorneys_obj,incorp_jurisdiction_obj):
        try:
            incorp_ho_addr = incorp_head_office_obj.fetchall()[0]
            incorp_ho_addr_list = []
            for item in incorp_ho_addr:
                if item is not None:
                    incorp_ho_addr_list.append(item)
            if any(incorp_ho_addr_list):
                pass
            else:
                incorp_ho_addr_list = 'Not Available'
        except:
            incorp_ho_addr_list = 'Not Available'

        incorp_attorneys_list = []
        for row in incorp_attorneys_obj:
            incorp_attorneys_list.append(row[0])
        if any(incorp_attorneys_list):
            pass
        else:
            incorp_attorneys_list = 'Not Available'

        incorp_jurisdiction = incorp_jurisdiction_obj.fetchall()[0][0]
        if any(incorp_jurisdiction):
            pass
        else:
            incorp_jurisdiction = 'Not Available'

        return incorp_ho_addr_list,incorp_attorneys_list,incorp_jurisdiction

    @staticmethod
    def bc_get_vals(incorp_registered_addr_obj,incorp_records_addr_obj):
        try:
            incorp_registered_addr_test = incorp_registered_addr_obj.fetchall()
        except:
            incorp_registered_addr_list = 'Not Available'
        else:
            if any(incorp_registered_addr_test):
                incorp_registered_addr = incorp_registered_addr_test[0]
                incorp_registered_addr_list = []
                for item in incorp_registered_addr:
                    if item is not None:
                        incorp_registered_addr_list.append(item)
                if any(incorp_registered_addr_list):
                    pass
                else:
                    incorp_registered_addr_list = 'Not Available'
            else:
                incorp_registered_addr_list = 'Not Available'

        try:
            incorp_records_addr_test = incorp_records_addr_obj.fetchall()
        except:
            incorp_records_addr_list = 'Not Available'
        else:
            if any(incorp_records_addr_test):
                incorp_records_addr = incorp_records_addr_test[0]
                incorp_records_addr_list = []
                for item in incorp_records_addr:
                    if item is not None:
                        incorp_records_addr_list.append(item)
                if any(incorp_records_addr_list):
                    pass
                else:
                    incorp_records_addr_list = 'Not Available'
            else:
                incorp_records_addr_list = 'Not Available'

        return incorp_registered_addr_list,incorp_records_addr_list

    @staticmethod
    def find_nob(incorp_nr_sql):
        incorp_nr_obj = db.engine.execute(incorp_nr_sql)
        try:
            incorp_nr = incorp_nr_obj.fetchall()[0][1]
        except:
            incorp_nob = 'Not Available'
        else:
            incorp_nr_sql = '\'NR ' + incorp_nr[1:] + '\''

            incorp_nob_sql = text("select NATURE_BUSINESS_INFO "
                                  "from bc_registries_names.corp_nob_vw "
                                  "where nr_num = {}".format(incorp_nr_sql))
            incorp_nob_obj = db.get_engine(app, 'db2').execute(incorp_nob_sql)
            incorp_nob = incorp_nob_obj.fetchall()
            if any(incorp_nob):
                incorp_nob = incorp_nob[0][0]
            else:
                incorp_nob = 'Not Available'

        return incorp_nob
