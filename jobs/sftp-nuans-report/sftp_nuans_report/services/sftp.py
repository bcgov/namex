import os
import requests
from flask import current_app
from config import Config
from util.token import get_bearer_token

class SftpService:
    @staticmethod
    def send_to_ocp_sftp_relay(data_dir: str):
        file_list = [f for f in os.listdir(data_dir) if f.endswith('.gz')]
        current_app.logger.info("Found %d .gz file(s) to be copied from directory: %s", len(file_list), data_dir)

        if Config.ENVIRONMENT != 'prod':
            current_app.logger.info('Skipping upload to SFTP Server')
            return

        for file in file_list:
            file_full_name = os.path.join(data_dir, file)
            with open(file_full_name, "rb") as file_obj:
                files = {"file": file_obj}
                headers = {"Authorization": f"Bearer {get_bearer_token()}"}
                try:
                    response = requests.post(Config.OCP_SFTP_URL, headers=headers, files=files)
                    response.raise_for_status()
                    current_app.logger.info(
                        "Successfully uploaded file '%s' to %s. Response Code: %d, Response Text: %s",
                        file_full_name,
                        Config.OCP_SFTP_URL,
                        response.status_code,
                        response.text,
                    )
                except requests.RequestException as e:
                    current_app.logger.error(
                        "Failed to upload file '%s' to %s. Error: %s",
                        file_full_name,
                        Config.OCP_SFTP_URL,
                        e,
                    )
                    raise
