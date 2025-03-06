import datetime
import logging

import pandas as pd
from flask import jsonify
from flask_restx import Namespace, Resource, cors, reqparse
from sqlalchemy import text

from ocp_relay.services.auth import jwt, requires_role
from ocp_relay.services.database import get_colin_connection, pay_sql_engine

# Register a local namespace for payment relay endpoints.
payment_invoices_api = Namespace("payments", description="Endpoints for NR Payment Invoices from Colin and Pay DBs.")

# Defines and validates the incoming 'payments_start_date' query parameter.
start_date_parser = reqparse.RequestParser()
start_date_parser.add_argument(
    "payments_start_date",
    type=str,
    required=True,
    help="The start date (YYYY-MM-DD) from which to fetch paid invoices.",
    location="args",
)


@payment_invoices_api.route("/pay", methods=["GET", "OPTIONS"])
class PayDBInvoices(Resource):
    @staticmethod
    @cors.crossdomain(origin="*")
    @jwt.requires_auth
    @requires_role("system")
    @payment_invoices_api.expect(start_date_parser)
    def get():
        """Retrieve paid invoices starting from the given date from the Postgres Pay DB."""
        args = start_date_parser.parse_args()
        payments_start_date = args.get("payments_start_date")
        try:
            datetime.datetime.strptime(payments_start_date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        logging.info("Fetching paid invoices starting from: %s", payments_start_date)

        sql_query = text(
            """
            SELECT i.business_identifier,
                   i.id AS invoice_id,
                   i.created_on,
                   ir.invoice_number,
                   i.invoice_status_code AS invoice_status,
                   p.payment_status_code AS pay_status,
                   i.total,
                   i.paid,
                   r.receipt_number
            FROM   invoices i
                   LEFT OUTER JOIN invoice_references ir ON ir.invoice_id = i.id
                   LEFT OUTER JOIN payments p ON p.invoice_number = ir.invoice_number
                   LEFT OUTER JOIN receipts r ON r.invoice_id = i.id
            WHERE  i.created_on >= :payments_start_date
              AND  i.invoice_status_code = 'PAID'
              AND  i.business_identifier LIKE 'NR%'
              AND  i.paid <> 101.5
            ORDER  BY invoice_id ASC;
        """
        )

        try:
            with pay_sql_engine.connect() as conn:
                result = conn.execute(sql_query, {"payments_start_date": payments_start_date})
                invoices = [dict(row) for row in result.mappings()]
        except Exception:
            logging.exception("Database query failed")
            return jsonify({"error": "Database query failed"}), 500

        return jsonify(invoices)


@payment_invoices_api.route("/colin", methods=["GET", "OPTIONS"])
class ColinDBInvoices(Resource):
    @staticmethod
    @cors.crossdomain(origin="*")
    @jwt.requires_auth
    @requires_role("system")
    @payment_invoices_api.expect(start_date_parser)
    def get():
        """Retrieve global payment records from the COLIN Oracle database starting from the given date."""
        args = start_date_parser.parse_args()
        payments_start_date = args.get("payments_start_date")
        try:
            datetime.datetime.strptime(payments_start_date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
        logging.info("Fetching global payments starting from: %s", payments_start_date)

        try:
            conn = get_colin_connection()
        except Exception as e:
            logging.exception("Oracle connection failed: %s", e)
            return jsonify({"error": "Oracle connection failed."}), 500

        try:
            sql = (
                f"SELECT bcol_key as nr_num, payment_id, bcol_account_num, bcol_racf_id, base_fee as bcol_paid "
                f"FROM payment@global "
                f"WHERE bcol_key LIKE 'NR%' "
                f"AND payment_date >= TO_DATE ('{payments_start_date}', 'yyyy-mm-dd')"
            )
            global_payment_frame = pd.read_sql(sql, con=conn)
            result = global_payment_frame.to_dict(orient="records")
        except Exception as e:
            logging.exception("Oracle query failed: %s", e)
            return jsonify({"error": "Oracle query failed."}), 500
        finally:
            conn.close()

        return jsonify(result)
