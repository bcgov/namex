import logging

from flask import jsonify
from flask_restx import Namespace, Resource, cors
from sqlalchemy import text

from ocp_relay.services.auth import jwt, requires_role
from ocp_relay.services.database import get_colin_connection, pay_sql_engine
from ocp_relay.services.sftp import SftpHandler

health_api = Namespace("health", description="Liveness and readiness checks")


@health_api.route("/liveness")
class HealthCheck(Resource):
    def get(self):
        return {"status": "ok"}, 200


@health_api.route("/sftp", methods=["GET", "OPTIONS"])
class SftpHealthCheck(Resource):
    @staticmethod
    @cors.crossdomain(origin="*")
    @jwt.requires_auth
    @requires_role("system")
    def get():
        """Verifies SFTP Connectivity"""
        try:
            with SftpHandler.get_connection():
                pass
            return {"status": "ok", "message": "SFTP connection successful."}, 200
        except Exception as e:
            logging.exception("SFTP connection failed: %s", e)
            return {"status": "error", "message": "SFTP connection failed."}, 500


@health_api.route("/colin", methods=["GET", "OPTIONS"])
class ColinHealthCheck(Resource):
    @staticmethod
    @cors.crossdomain(origin="*")
    @jwt.requires_auth
    @requires_role("system")
    def get():
        """Verifies Colin Connectivity"""
        try:
            with get_colin_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM DUAL")
                cursor.fetchone()
            return jsonify({"status": "ok", "message": "Oracle connection successful."})
        except Exception as e:
            logging.exception("Oracle connection failed: %s", e)
            return jsonify({"status": "error", "message": "Oracle connection failed."}), 500


@health_api.route("/pay", methods=["GET", "OPTIONS"])
class PayHealthCheck(Resource):
    @staticmethod
    @cors.crossdomain(origin="*")
    @jwt.requires_auth
    @requires_role("system")
    def get():
        """Verifies Pay Connectivity"""
        try:
            with pay_sql_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return jsonify({"status": "ok", "message": "Postgres connection successful."})
        except Exception as e:
            logging.exception("Postgres connection failed: %s", e)
            return jsonify({"status": "error", "message": "Postgres connection failed."}), 500
