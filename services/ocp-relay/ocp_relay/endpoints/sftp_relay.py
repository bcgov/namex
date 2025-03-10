import logging

from flask_restx import Namespace, Resource, cors
from werkzeug.datastructures import FileStorage

from ocp_relay.services.auth import jwt, requires_role
from ocp_relay.services.sftp import SftpHandler

# Register a local namespace for the sftp relay.
sftp_api = Namespace("sftp", description="Endpoint for the SFTP Relay to upload a .gz file to the Government Server.")

# Defines and validates the incoming gz archive in the request.
gz_archive_parser = sftp_api.parser()
gz_archive_parser.add_argument(
    "file",
    type=FileStorage,
    location="files",
    required=True,
    help="A gz archive (compressed file with a .gz extension) containing exactly one file. "
    "Received from multipart/form-data http request under the key 'file'.",
)


@sftp_api.route("/upload", methods=["POST", "OPTIONS"])
class SftpRelay(Resource):
    @staticmethod
    @cors.crossdomain(origin="*")
    @jwt.requires_auth
    @requires_role("system")
    @sftp_api.expect(gz_archive_parser)
    def post():
        """
        Accepts a gz archive and uploads the file to the Gov SFTP Server.

        Authentication:
            JWT authentication and 'system' role.

        Returns:
            tuple: JSON response and status code.
                - On success: ({"message": "Success, file received"}, 200)
                - On failure: ({"message": "<error details>"}, <error_code>)
        """
        # Parse the gz archive from the request.
        gz_archive = gz_archive_parser.parse_args().get("file")

        # Ensure a file was provided and that it has a .gz extension.
        if gz_archive is None:
            return {"message": "No file provided"}, 400
        if not gz_archive.filename.lower().endswith(".gz"):
            return {"message": "Invalid file type. A .gz file is required."}, 400

        # Uploag gzip file to Gov SFTP Server
        try:
            SftpHandler.upload_gz_contents(gz_archive)
            return {"message": "Success, file received"}, 200
        except Exception:
            logging.exception("Error uploading file")
            return {"message": "An error occurred while uploading the file."}, 500
