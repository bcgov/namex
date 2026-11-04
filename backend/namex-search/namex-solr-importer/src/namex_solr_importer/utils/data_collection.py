# Copyright © 2025 Province of British Columbia
#
# Licensed under the BSD 3 Clause License, (the "License");
# you may not use this file except in compliance with the License.
# The template for the license can be found here
#    https://opensource.org/license/bsd-3-clause/
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""Data collection functions."""

from flask import current_app
from sqlalchemy import CursorResult, text

from namex_solr_importer import lear_db, namex_db, oracle_db


def _get_stringified_list_for_sql(config_value: str) -> str:
    """Return the values from the config in a format usable for the execute statement."""
    if items := current_app.config.get(config_value, []):
        return ",".join([f"'{x}'" for x in items]).replace(")", "")

    return ""


def collect_colin_data():
    """Collect data from COLIN."""
    current_app.logger.debug("Connecting to Oracle instance...")
    cursor = oracle_db.connection.cursor()
    current_app.logger.debug("Collecting COLIN data...")
    cursor.execute(f"""
        SELECT c.corp_num, c.recognition_dts as start_date,
            cn.corp_nme as name, j.can_jur_typ_cd as jurisdiction,
            CASE cos.op_state_typ_cd
                when 'ACT' then 'ACTIVE'
                when 'HIS' then 'HISTORICAL'
                else 'ACTIVE'
            END as state,
            c.corp_typ_cd as sub_type
        FROM corporation c
        join corp_state cs on cs.corp_num = c.corp_num
        join corp_op_state cos on cos.state_typ_cd = cs.state_typ_cd
        join (
            select cn_sub.corp_num, cn_sub.corp_nme, cn_sub.corp_name_typ_cd, row_number()
            over (partition by cn_sub.corp_num
                  order by
                    CASE
                        when c2.corp_typ_cd = 'A' and cn_sub.corp_name_typ_cd = 'AS' then 1
                        when cn_sub.corp_name_typ_cd in ('CO', 'NB') then 2
                        else 3
                        end
                  ) rn
            from corp_name cn_sub
            join corporation c2 on c2.corp_num = cn_sub.corp_num
            where cn_sub.end_event_id is null
                and cn_sub.corp_name_typ_cd in ('CO', 'NB', 'AS')
        ) cn on cn.corp_num = c.corp_num and cn.rn = 1
        left join (select * from jurisdiction where end_event_id is null) j on j.corp_num = c.corp_num
        WHERE c.corp_typ_cd in ({_get_stringified_list_for_sql("CONFLICT_LEGAL_TYPES")})
            and c.corp_typ_cd not in ({_get_stringified_list_for_sql("MODERNIZED_LEGAL_TYPES")})
            and cs.end_event_id is null
            and cos.op_state_typ_cd in ('ACT','HLD','HIS')
        """)
    return cursor


def collect_lear_data() -> CursorResult:
    """Collect data from LEAR."""
    current_app.logger.debug("Connecting to LEAR Postgres instance...")
    conn = lear_db.db.engine.connect()
    current_app.logger.debug("Collecting LEAR data...")
    return conn.execute(
        text(f"""
        SELECT b.identifier as corp_num, b.legal_name as name,
            b.founding_date as start_date, b.state,
            CASE j.region
                when NULL then j.country
                when 'FEDERAL' then 'FD'
                else j.region
            END as jurisdiction,
            b.legal_type as sub_type
        FROM businesses b
        LEFT JOIN jurisdictions j on j.business_id = b.id
        WHERE legal_type in ({_get_stringified_list_for_sql("CONFLICT_LEGAL_TYPES")})
            and legal_type in ({_get_stringified_list_for_sql("MODERNIZED_LEGAL_TYPES")})
            and state in ('ACTIVE', 'HISTORICAL')
        """)
    )


def collect_namex_data() -> CursorResult:
    """Collect data from NameX."""
    current_app.logger.debug("Connecting to NameX Postgres instance...")
    conn = namex_db.db.engine.connect()
    current_app.logger.debug("Collecting NameX data...")
    return conn.execute(
        text("""
        SELECT r.nr_num,
            COALESCE(NULLIF(n.corp_num, ''), NULLIF(r.corp_num, '')) as corp_num,
            CASE
                WHEN COALESCE(NULLIF(n.corp_num, ''), NULLIF(r.corp_num, '')) IS NOT NULL THEN 'CONSUMED'
                WHEN r.state_cd = 'CONDITIONAL' THEN 'CONDITION'
                ELSE r.state_cd
            END as state,
            r.xpro_jurisdiction as jurisdiction,
            r.submitted_date as start_date, r.submit_count,
            n.name, n.choice,
            CASE n.state
                when 'APPROVED' then 'A'
                when 'REJECTED' then 'R'
                when 'CONDITION' then 'C'
                else n.state
            END as name_state,
            r.request_type_cd as sub_type
        FROM requests r
            JOIN names n on n.nr_id = r.id
        ORDER BY r.nr_num, n.choice
        """)
    )


def collect_synonyms_data() -> CursorResult:
    """Collect synonyms data from NameX."""
    current_app.logger.debug("Connecting to NameX Postgres instance...")
    conn = namex_db.db.engine.connect()
    current_app.logger.debug("Collecting Synonym data...")
    # TODO: verify can just collect 'synonym' table / 'synonyms_text' column (there's also synonym_orig / stems_text)
    return conn.execute(
        text("""
        SELECT synonyms_text
        FROM synonym
        WHERE enabled='t'
        """)
    )
