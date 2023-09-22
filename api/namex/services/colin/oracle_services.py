# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Create Oracle database connection.

These will get initialized by the application.
"""

import cx_Oracle
from flask import _app_ctx_stack, current_app

from .exceptions import ColinServicesError


class ColinServices(object):
    """Provides services to change the legacy NRO Database."""

    def __init__(self, app=None):
        """Initializer, supports setting the app context on instantiation."""
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Set up for the extension.

        :param app: Flask app
        :return: naked
        """
        self.app = app
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        """Clean up oracle session."""
        # the oracle session pool will clean up after itself
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'nro_oracle_pool'):
            ctx.nro_oracle_pool.close()

    def _create_pool(self):
        """Create the cx_oracle connection pool from the Flask Config Environment.

        :return: an instance of the OCI Session Pool
        """
        # this uses the builtin session / connection pooling provided by
        # the Oracle OCI driver
        # setting threaded =True wraps the underlying calls in a Mutex
        # so we don't have to that here

        def init_session(conn, requested_tag):
            cursor = conn.cursor()
            cursor.execute("alter session set TIME_ZONE = 'America/Vancouver'")

        return cx_Oracle.SessionPool(user=current_app.config.get('ORACLE_COLIN_USER'),  # pylint:disable=c-extension-no-member
                                     password=current_app.config.get('ORACLE_COLIN_PASSWORD'),
                                     dsn='{0}:{1}/{2}'.format(current_app.config.get('ORACLE_COLIN_HOST'),
                                                              current_app.config.get('ORACLE_COLIN_PORT'),
                                                              current_app.config.get('ORACLE_COLIN_DB_NAME')),
                                     min=1,
                                     max=10,
                                     increment=1,
                                     connectiontype=cx_Oracle.Connection,  # pylint:disable=c-extension-no-member
                                     threaded=True,
                                     getmode=cx_Oracle.SPOOL_ATTRVAL_NOWAIT,  # pylint:disable=c-extension-no-member
                                     waitTimeout=1500,
                                     timeout=3600,
                                     sessionCallback=init_session,
                                     encoding='UTF-8',
                                     nencoding='UTF-8')

    @property
    def connection(self):
        """Connect property of the NROService.

        If this is running in a Flask context,
        then either get the existing connection pool or create a new one
        and then return an acquired session
        :return: cx_Oracle.connection type
        """
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'nro_oracle_pool'):
                ctx._nro_oracle_pool = self._create_pool()
            return ctx._nro_oracle_pool.acquire()

    def get_business_info_by_corp_num(self, corp_num):
        """Get a business info by corp_num.

        :param corp_num: string
        :return: business info dict(identifier, legal_name, legal_type, home_jurisdiction, home_identifier)
        :raise: (NROServicesError) with the error information set
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                select c.corp_num,
                       c.corp_typ_cd,
                       j.can_jur_typ_cd,
                       j.othr_juris_desc,
                       j.home_juris_num,
                       cn.corp_nme,
                       cos.op_state_typ_cd
                from CORPORATION@colin_readonly.bcgov c
                         left join JURISDICTION@colin_readonly.bcgov j on j.corp_num = c.corp_num
                    and j.end_event_id is null
                         left join CORP_NAME@colin_readonly.bcgov cn on cn.corp_num = c.corp_num
                    and cn.end_event_id is null
                         left join CORP_STATE@colin_readonly.bcgov cs on cs.corp_num = c.corp_num
                    and cs.end_event_id is null
                         left join CORP_OP_STATE@colin_readonly.bcgov cos on cos.state_typ_cd = cs.state_typ_cd
                where c.CORP_NUM=:corp_num""", corp_num=corp_num)

            business = cursor.fetchone()
            if not business:
                return None

            # add column names to resultset to build out correct json structure and make manipulation below more robust
            # (better than column numbers)
            business = dict(zip([x[0].lower() for x in cursor.description], business))

            # if this is an XPRO, get correct jurisdiction; otherwise, it's BC
            if business['corp_typ_cd'] in ('A', 'XCP'):
                business['jurisdiction'] = business['can_jur_typ_cd']
                if business['can_jur_typ_cd'] == 'OT':
                    business['jurisdiction'] = business['othr_juris_desc']
            else:
                business['jurisdiction'] = 'BC'

            return business

        except Exception as err:
            current_app.logger.error(err.with_traceback(None))
            raise OracleServicesError({'code': '"unable_to_get_business',
                                    'description': 'Unable to get the business in NRO'}, 500)
