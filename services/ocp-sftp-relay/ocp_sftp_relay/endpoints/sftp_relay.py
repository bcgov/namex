import logging

from flask_restx import Namespace, Resource, cors
from werkzeug.datastructures import FileStorage

from ocp_sftp_relay.services.auth import jwt, requires_role
from ocp_sftp_relay.services.sftp import SftpHandler

# Register a local namespace for the sftp relay.
sftp_api = Namespace("sftp", description="Upload Endpoint for the SFTP Relay service.")

# Defines and Validates the incoming zip archive in the request.
zip_archive_parser = sftp_api.parser()
zip_archive_parser.add_argument(
    "file",
    type=FileStorage,
    location="files",
    required=True,
    help="A zip archive (compressed file with a .zip extension) containing exactly one file. "
    "Received from multipart/form-data http request under the key 'file'.",
)


@sftp_api.route("/upload", methods=["POST", "OPTIONS"])
class SftpRelay(Resource):
    @staticmethod
    @cors.crossdomain(origin="*")
    @jwt.requires_auth
    @requires_role("system")
    @sftp_api.expect(zip_archive_parser)
    def post():
        """
        Accepts a zip archive and uploads the zip file to the Gov SFTP Server.

        Authentication:
            JWT authentication and 'system' role.

        Returns:
            tuple: JSON response and status code.
                - On success: ({"message": "Success, file received"}, 200)
                - On failure: ({"message": "<error details>"}, <error_code>)
        """
        # Parse the zip archive from the request.
        zip_archive = zip_archive_parser.parse_args().get("file")

        # Ensure a zip file was extracted.
        if zip_archive is None:
            return {"message": "No file provided"}, 400
        if not zip_archive.filename.lower().endswith(".zip"):
            return {"message": "Invalid file type. A zip file is required."}, 400

        # Upload zip file to Gov SFTP Server.
        try:
            SftpHandler.upload_zip_contents(zip_archive)
            return {"message": "Success, file received"}, 200
        except Exception:
            logging.exception("Error uploading file")
            return {"message": "An error occurred while uploading the file."}, 500
