# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""API endpoints for managing a corporations resource."""
import logging

from flask import Blueprint, current_app, jsonify
from flask_cors import cross_origin

from colin_api.models import db
from colin_api.utils.auth import jwt


logger = logging.getLogger(__name__)

bp = Blueprint('Corporations', __name__, url_prefix='/corporations')


@bp.route('/echo', methods=['GET', 'OPTIONS'])
@cross_origin(origin='*')
@jwt.requires_auth
def echo(*args, **kwargs):  # pylint: disable=unused-argument
    """Echo jwt information."""
    try:
        return jsonify(g.jwt_oidc_token_info), 200  # pylint: disable=undefined-variable # noqa: F821
    except Exception as err:  # noqa: B902
        return jsonify({'error': f'{err}'}), 500


@bp.route('/<string:corp_num>', methods=['GET', 'OPTIONS'])
@cross_origin(origin='*')
@jwt.requires_auth
@jwt.has_one_of_roles(['names_viewer'])
def request_colin(corp_num: str):  # pylint: disable=too-many-locals, too-many-branches
    """Get corpration details from COLIN."""
    corp_num_sql = "\'" + corp_num + "\'"

    incorp_info_sql = Methods.build_info_sql(corp_num_sql)
    incorp_addr_id_sql = Methods.build_addr_id_sql(corp_num_sql)
    incorp_directors_sql = Methods.build_directors_sql(corp_num_sql)

    try:
        incorp_nr_sql = Methods.build_nr_sql(corp_num_sql)
        incorp_nob = Methods.find_nob(incorp_nr_sql)
        incorp_info_dict, incorp_directors_obj = Methods.init_info(incorp_info_sql, incorp_directors_sql)
        incorp_class = incorp_info_dict['corp_class']

        if incorp_class == 'XPRO':

            incorp_jurisdiction_sql = Methods.build_jurisdiction_sql(corp_num_sql)
            incorp_attorneys_sql = Methods.build_attorneys_sql(corp_num_sql)

            incorp_head_office_obj, incorp_attorneys_obj, incorp_jurisdiction_obj = \
                Methods.xpro_get_objs(incorp_addr_id_sql, incorp_attorneys_sql, incorp_jurisdiction_sql)

        # BC corp
        else:
            incorp_registered_addr_obj, incorp_records_addr_obj = Methods.bc_get_objs(incorp_addr_id_sql)

    except exc.SQLAlchemyError as err:  # pylint: disable=undefined-variable # noqa: F821
        current_app.logger.debug(err.with_traceback(None))
        return jsonify({'message': 'Error occurred getting the corporation details'}), 500
    except AttributeError:
        return jsonify({'message': 'Attribute error'}), 500
    except IndexError as err:
        current_app.logger.debug(err.with_traceback(None))
        return jsonify({'message': 'Error: Could not find corporation details'}), 404
    except Exception as err:  # noqa: B902
        current_app.logger.debug(err.with_traceback(None))
        return jsonify({'message': 'Unknown error occurred in colin-api'}), 500

    incorp_date = incorp_info_dict['recognition_dts']
    if incorp_date is not None:
        incorp_date_str = '{:0>4}-{:0>2}-{:0>2}'.format(incorp_date.year, incorp_date.month, incorp_date.day) \
            # pylint: disable=consider-using-f-string
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
            Methods.xpro_get_vals(incorp_head_office_obj, incorp_attorneys_obj, incorp_jurisdiction_obj)

        corp_details_dict = {'incorp #': corp_num,
                             'incorporated': incorp_date_str,
                             'directors': incorp_directors_list,
                             'attorney names': incorp_attorneys_list,
                             'head office': incorp_ho_addr_list,
                             'jurisdiction': incorp_jurisdiction,
                             'nature of business': incorp_nob}
    else:
        incorp_registered_addr_list, incorp_records_addr_list = \
            Methods.bc_get_vals(incorp_registered_addr_obj, incorp_records_addr_obj)

        corp_details_dict = {'incorp #': corp_num,
                             'incorporated': incorp_date_str,
                             'directors': incorp_directors_list,
                             'registered office delivery address': incorp_registered_addr_list,
                             'records office delivery address': incorp_records_addr_list,
                             'jurisdiction': 'BC',
                             'nature of business': incorp_nob}

    return jsonify(corp_details_dict), 200


@bp.route('/business/<string:corp_num>', methods=['GET', 'OPTIONS'])
@cross_origin(origin='*')
@jwt.requires_auth
def business_request_colin(corp_num: str):
    """Get business details from COLIN."""
    corp_num_sql = "\'" + corp_num + "\'"

    incorp_info_sql = Methods.build_info_sql(corp_num_sql)
    incorp_directors_sql = Methods.build_directors_sql(corp_num_sql)
    incorp_name_sql = Methods.build_incorp_name_sql(corp_num)

    try:
        incorp_init_info = Methods.init_info(incorp_info_sql, incorp_directors_sql)
        incorp_name_dict = Methods.get_incorp_name(incorp_name_sql)
        incorp_info_dict = incorp_init_info[0]
        incorp_class = incorp_info_dict['corp_class']
        incorp_jurisdiction = 'BC'
        incorp_home_identifier = None

        if incorp_class == 'XPRO':
            incorp_jurisdiction_sql = Methods.build_jurisdiction_sql(corp_num_sql)
            incorp_jurisdiction, incorp_home_identifier = Methods.xpro_get_id(incorp_jurisdiction_sql)

    except exc.SQLAlchemyError as err:  # pylint: disable=undefined-variable # noqa: F821
        current_app.logger.debug(err.with_traceback(None))
        return jsonify({'message': 'Error occurred getting the corporation details'}), 500
    except AttributeError:
        return jsonify({'message': 'Attribute error'}), 500
    except IndexError as err:
        current_app.logger.debug(err.with_traceback(None))
        return jsonify({'message': 'Error: Could not find corporation details'}), 404
    except Exception as err:  # noqa: B902
        current_app.logger.debug(err.with_traceback(None))
        return jsonify({'message': 'Unknown error occurred in colin-api'}), 500

    response_dict = {'identifier': corp_num,
                     'legalName': incorp_name_dict['corp_nme'],
                     'legalType': incorp_info_dict['corp_typ_cd'],
                     'jurisdiction': incorp_jurisdiction,
                     'homeIdentifier': incorp_home_identifier}

    return jsonify(response_dict), 200


class Methods:
    """Class of query methods."""

    @staticmethod
    def build_info_sql(corp_num_sql):
        """Build sql."""
        return f'select * from bc_registries.corp_num_dts_class_vw where corp_num = {corp_num_sql}'

    @staticmethod
    def build_directors_sql(corp_num_sql):
        """Build directors sql."""
        return f"select \
                    CASE \
                        WHEN cp.middle_nme IS NOT NULL \
                            THEN cp.first_nme || ' ' ||cp.middle_nme|| ' ' ||cp.last_nme \
                        ELSE \
                            cp.first_nme || ' ' || cp.last_nme \
                        END director_name \
                from bc_registries.corp_party_vw cp \
                where cp.corp_num = {corp_num_sql} and cp.end_event_id IS NULL and cp.party_typ_cd = 'DIR';"

    @staticmethod
    def build_addr_id_sql(corp_num_sql):
        """Build address sql."""
        return f'select delivery_addr_id \
                   from bc_registries.office_vw \
                  where corp_num={corp_num_sql} \
                    and end_event_id IS NULL \
                    and delivery_addr_id IS NOT NULL;'

    @staticmethod
    def build_jurisdiction_sql(corp_num_sql):
        """Build jurisdiction sql."""
        return f'select home_jurisdiction, home_juris_num \
                   from bc_registries.corp_jurs_vw \
                  where corp_num = {corp_num_sql}'

    @staticmethod
    def build_attorneys_sql(corp_num_sql):
        """Build attorneys sql."""
        return f"select \
                    CASE \
                      WHEN cp.middle_nme IS NOT NULL \
                        THEN cp.first_nme || ' ' ||cp.middle_nme|| ' ' ||cp.last_nme \
                      ELSE \
                        cp.first_nme || ' ' || cp.last_nme \
                    END attorney_name \
                   from bc_registries.corp_party_vw cp\
                   where cp.corp_num = {corp_num_sql} and cp.end_event_id IS NULL and cp.party_typ_cd = 'ATT';"

    @staticmethod
    def build_nr_sql(corp_num_sql):
        """Build NR sql."""
        return f'select * \
                   from bc_registries.corp_nr_num_vw \
                   where corp_num = {corp_num_sql};'

    @staticmethod
    def build_incorp_name_sql(corp_num_sql):
        """Build name sql."""
        return f'select start_event_id, corp_nme, corp_name_typ_cd, corp_num, end_event_id \
                   from bc_registries.corp_name \
                   where corp_num = {corp_num_sql} and end_event_id is null;'

    @staticmethod
    def init_info(incorp_info_sql, incorp_directors_sql):
        """Init info."""
        try:
            incorp_info_obj = db.engine.execute(incorp_info_sql)
            incorp_info_dict = dict(incorp_info_obj.fetchall()[0])
        except IndexError:
            incorp_info_dict = {'corp_class': None, 'recognition_dts': None}

        incorp_directors_obj = db.engine.execute(incorp_directors_sql)

        return incorp_info_dict, incorp_directors_obj

    @staticmethod
    def get_incorp_name(incorp_name_sql):
        """Get incorp name obj."""
        incorp_name_obj = db.engine.execute(incorp_name_sql)
        incorp_name_dict = dict(incorp_name_obj.fetchall()[0])

        return incorp_name_dict

    @staticmethod
    def xpro_get_id(incorp_jurisdiction_sql):
        """Find objects for xpro company."""
        incorp_jurisdiction_obj = db.engine.execute(incorp_jurisdiction_sql)
        incorp_jurisdiction = incorp_jurisdiction_obj.fetchall()[0][0]
        incorp_home_identifier = incorp_jurisdiction_obj.fetchall()[0][1]

        return incorp_jurisdiction, incorp_home_identifier

    @staticmethod
    def xpro_get_objs(incorp_addr_id_sql, incorp_attorneys_sql, incorp_jurisdiction_sql):
        """Find objects for xpro company."""
        incorp_ho_addr_id_obj = db.engine.execute(incorp_addr_id_sql)
        incorp_ho_addr_id = incorp_ho_addr_id_obj.fetchall()[0][0]
        incorp_ho_addr_id_sql = "\'" + str(incorp_ho_addr_id) + "\'"
        incorp_ho_addr_sql = f'select addr_line_1, ADDR_LINE_2, ADDR_LINE_3, city, province, country_typ_cd, postal_cd \
                                 from bc_registries.address_vw \
                                where addr_id= {incorp_ho_addr_id_sql} AND addr_id IS NOT NULL;'
        incorp_head_office_obj = db.engine.execute(incorp_ho_addr_sql)

        incorp_attorneys_obj = db.engine.execute(incorp_attorneys_sql)
        incorp_jurisdiction_obj = db.engine.execute(incorp_jurisdiction_sql)

        return incorp_head_office_obj, incorp_attorneys_obj, incorp_jurisdiction_obj

    @staticmethod
    def bc_get_objs(incorp_addr_id_sql):
        """Find objects for bc company."""
        incorp_addr_id_obj = db.engine.execute(incorp_addr_id_sql)
        incorp_addr_ids = incorp_addr_id_obj.fetchall()
        incorp_registered_addr_obj = None
        incorp_records_addr_obj = None
        if len(incorp_addr_ids) > 0:
            incorp_reg_addr_id = incorp_addr_ids[0][0]
            incorp_reg_addr_id_sql = "\'" + str(incorp_reg_addr_id) + "\'"
            incorp_reg_addr_sql = f'select addr_line_1, ADDR_LINE_2, ADDR_LINE_3, city, \
                                        province, country_typ_cd, postal_cd \
                                    from bc_registries.address_vw \
                                    where addr_id= {incorp_reg_addr_id_sql} AND addr_id IS NOT NULL;'
            incorp_registered_addr_obj = db.engine.execute(incorp_reg_addr_sql)
            if len(incorp_addr_ids) > 1:
                incorp_rec_addr_id = incorp_addr_ids[1][0]
                incorp_rec_addr_id_sql = "\'" + str(incorp_rec_addr_id) + "\'"
                incorp_rec_addr_sql = f'select addr_line_1, ADDR_LINE_2, ADDR_LINE_3, city, \
                                            province, country_typ_cd, postal_cd \
                                        from bc_registries.address_vw \
                                        where addr_id= {incorp_rec_addr_id_sql} AND addr_id IS NOT NULL;'
                incorp_records_addr_obj = db.engine.execute(incorp_rec_addr_sql)

        return incorp_registered_addr_obj, incorp_records_addr_obj

    @staticmethod
    def xpro_get_vals(incorp_head_office_obj, incorp_attorneys_obj, incorp_jurisdiction_obj):
        """Find values for xpro company."""
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
        except:  # pylint: disable=bare-except # noqa: E722
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

        return incorp_ho_addr_list, incorp_attorneys_list, incorp_jurisdiction

    @staticmethod
    def bc_get_vals(incorp_registered_addr_obj, incorp_records_addr_obj):  # pylint: disable=too-many-branches
        """Find values for bc company."""
        try:
            incorp_registered_addr_test = incorp_registered_addr_obj.fetchall()
        except:  # pylint: disable=bare-except # noqa: B901, E722
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
        except:  # pylint: disable=bare-except # noqa: B901, E722
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

        return incorp_registered_addr_list, incorp_records_addr_list

    @staticmethod
    def find_nob(incorp_nr_sql):
        """Find nature business info."""
        incorp_nr_obj = db.engine.execute(incorp_nr_sql)
        try:
            incorp_nr = incorp_nr_obj.fetchall()[0][1]
        except:  # pylint: disable=bare-except # noqa: E722
            incorp_nob = 'Not Available'
        else:
            incorp_nr_sql = "\'NR " + incorp_nr[1:] + "\'"

            incorp_nob_sql = f'select NATURE_BUSINESS_INFO \
                                 from bc_registries_names.corp_nob_vw \
                                where nr_num = {incorp_nr_sql}'
            incorp_nob_obj = db.get_engine(bind='db2').execute(incorp_nob_sql)
            incorp_nob = incorp_nob_obj.fetchall()
            if any(incorp_nob):
                incorp_nob = incorp_nob[0][0]
            else:
                incorp_nob = 'Not Available'

        return incorp_nob
