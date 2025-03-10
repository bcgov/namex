import logging.config
import sys
from os import path

from config import Config


def setup_logging(conf="logging.conf"):
    log_file_path = path.join(Config.PROJECT_ROOT, conf)

    if path.isfile(log_file_path):
        logging.config.fileConfig(log_file_path)
        print(f"Configure logging, from conf:{log_file_path}", file=sys.stderr)
    else:
        print(
            f"Unable to configure logging, attempted conf:{log_file_path}",
            file=sys.stderr,
        )
