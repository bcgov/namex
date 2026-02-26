"""SFTP service module for uploading files to the OCP SFTP relay."""

import os

import requests
from flask import current_app

from sftp_nuans_report.config import Config
from sftp_nuans_report.util.token import get_bearer_token


class SftpService:  # pylint: disable=too-few-public-methods
    """Service responsible for uploading files to the OCP SFTP relay."""

    @staticmethod
    def send_to_ocp_sftp_relay(data_dir: str) -> None:
        """Upload all .gz files in the given directory to the SFTP relay.

        Skips upload when the environment is not set to 'prod'.
        Raises:
            requests.RequestException: If the upload fails.
        """
        file_list = [f for f in os.listdir(data_dir) if f.endswith('.gz')]

        current_app.logger.info(
            'Found %d .gz file(s) to be copied from directory: %s',
            len(file_list),
            data_dir,
        )

        if Config.ENVIRONMENT != 'prod':
            current_app.logger.info('Skipping upload to SFTP Server')
            return

        for file in file_list:
            file_full_name = os.path.join(data_dir, file)

            with open(file_full_name, 'rb') as file_obj:
                files = {'file': file_obj}
                headers = {'Authorization': f'Bearer {get_bearer_token()}'}

                try:
                    response = requests.post(
                        Config.OCP_SFTP_URL,
                        headers=headers,
                        files=files,
                        timeout=(5, 30),  # connect timeout, read timeout
                    )
                    response.raise_for_status()

                    current_app.logger.info(
                        'Successfully uploaded file %s to %s. '
                        'Response Code: %d, Response Text: %s',
                        file_full_name,
                        Config.OCP_SFTP_URL,
                        response.status_code,
                        response.text,
                    )

                except requests.RequestException as exc:
                    current_app.logger.error(
                        'Failed to upload file %s to %s. Error: %s',
                        file_full_name,
                        Config.OCP_SFTP_URL,
                        exc,
                    )
                    raise
