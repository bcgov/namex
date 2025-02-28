import logging
import tempfile
import zipfile
from base64 import decodebytes
from io import BytesIO, StringIO
from typing import IO

import paramiko
from flask import current_app
from pysftp import CnOpts, Connection


class SftpHandler:
    @classmethod
    def upload_zip_contents(cls, zip_archive: IO[bytes]):
        """
        Extract the first file from the provided zip archive and upload it to the Gov SFTP server.

        This method reads the zip archive from a file-like object, extracts the first file,
        and uploads it using an SFTP connection.

        Args:
            zip_archive (IO[bytes]): A file-like object containing the ZIP archive's data.
        """
        try:
            # Create an in-memory binary stream from the raw bytes.
            zip_data = zip_archive.read()
            zip_io = BytesIO(zip_data)

            # Open the in-memory binary stream as a ZIP archive.
            with zipfile.ZipFile(zip_io) as archive:
                inner_zip_file_name = archive.namelist()[0]
                logging.info("Processing file %s from zip archive.", inner_zip_file_name)

                # Open the inner file in the ZIP archive.
                with archive.open(inner_zip_file_name) as file_obj:
                    # Establish SFTP connection and upload the file.
                    with cls._get_connection() as sftp_client:
                        remote_path = inner_zip_file_name
                        sftp_client.putfo(file_obj, remote_path)
                        logging.info("SFTP upload completed for file: %s", inner_zip_file_name)
        except Exception as e:
            logging.error("Error processing zip file: %s", e)
            raise e

    @staticmethod
    def _get_connection() -> Connection:
        """Establish and return an SFTP connection."""
        config = current_app.config
        sftp_username = config.get("SFTP_USERNAME")
        sftp_host = config.get("SFTP_HOST")
        sftp_port = config.get("SFTP_PORT")
        sftp_host_key = config.get("SFTP_HOST_KEY")
        bcreg_ftp_private_key = config.get("BCREG_FTP_PRIVATE_KEY").strip('"')
        bcreg_ftp_private_key_passphrase = config.get("BCREG_FTP_PRIVATE_KEY_PASSPHRASE")

        # 1. Initialize connection options and process the host key.
        cnopts = CnOpts()
        ftp_host_key_data = sftp_host_key.encode()
        key = paramiko.RSAKey(data=decodebytes(ftp_host_key_data))
        cnopts.hostkeys.add(sftp_host, "ssh-rsa", key)

        # 2. Process the private key and write to a temporary PEM file.
        key_obj = paramiko.RSAKey.from_private_key(
            StringIO(bcreg_ftp_private_key),
            password=bcreg_ftp_private_key_passphrase or None,
        )
        with tempfile.NamedTemporaryFile(delete=False) as temp_key_file:
            key_obj.write_private_key_file(temp_key_file.name)
            key_path = temp_key_file.name

        # 3. Build credentials and create the SFTP connection.
        sft_credentials = {
            "username": sftp_username,
            "private_key": key_path,
            "private_key_pass": bcreg_ftp_private_key_passphrase,
        }
        sftp_connection = Connection(host=sftp_host, **sft_credentials, cnopts=cnopts, port=int(sftp_port))
        logging.info("sftp_connection successful")
        return sftp_connection
