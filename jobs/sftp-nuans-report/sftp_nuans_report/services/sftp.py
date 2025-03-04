import os
import logging
import requests
from config import Config
from util.token import get_bearer_token

class SftpService:
    @staticmethod
    def send_to_ocp_sftp_relay(data_dir: str):
        file_list = os.listdir(data_dir)
        logging.info("Found %d file(s) to be copied from directory: %s", len(file_list) - 1, data_dir)

        for file in file_list:
            file_full_name = os.path.join(data_dir, file)
            with open(file_full_name, "rb") as file_obj:
                files = {"file": file_obj}
                headers = {"Authorization": f"Bearer {get_bearer_token()}"}
                try:
                    response = requests.post(Config.OCP_SFTP_URL, headers=headers, files=files)
                    response.raise_for_status()
                    logging.info(
                        "Successfully uploaded file '%s' to %s. Response Code: %d, Response Text: %s",
                        file_full_name,
                        Config.OCP_SFTP_URL,
                        response.status_code,
                        response.text,
                    )
                except requests.RequestException as e:
                    logging.error(
                        "Failed to upload file '%s' to %s. Error: %s",
                        file_full_name,
                        Config.OCP_SFTP_URL,
                        e,
                    )
                    raise
