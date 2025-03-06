import gzip
import logging
import tempfile
from base64 import decodebytes
from io import BytesIO, StringIO
from typing import IO

import paramiko
from flask import current_app
from pysftp import CnOpts, Connection


class SftpHandler:
    @classmethod
    def upload_gz_contents(cls, gz_archive: IO[bytes]):
        """
        Decompress the provided gz archive and upload the contained file to the Gov SFTP server.

        This method reads the gzip archive from a file-like object, decompresses its content,
        and uploads the resulting file using an SFTP connection.

        Args:
            gz_archive (IO[bytes]): A file-like object containing the gzip archive's data.
        """
        try:
            # Ensure we're at the start of the file
            gz_archive.seek(0)
            gz_data = gz_archive.read()

            # Decompress the gz archive using a BytesIO wrapper.
            with gzip.GzipFile(fileobj=BytesIO(gz_data)) as gz_file:
                decompressed_data = gz_file.read()

            # Derive the remote filename by stripping the '.gz' extension.
            original_filename = gz_archive.filename
            if original_filename.lower().endswith(".gz"):
                remote_filename = original_filename[:-3]
            else:
                remote_filename = original_filename
            logging.info("Processing file %s from gz archive.", remote_filename)

            # Upload the decompressed data to the SFTP server.
            with cls.get_connection() as sftp_client:
                # Create a BytesIO stream for the decompressed data.
                file_obj = BytesIO(decompressed_data)
                remote_path = remote_filename
                sftp_client.putfo(file_obj, remote_path)
                logging.info("SFTP upload completed for file: %s", remote_filename)
        except Exception as e:
            logging.error("Error processing gz file: %s", e)
            raise e

    @staticmethod
    def get_connection() -> Connection:
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
