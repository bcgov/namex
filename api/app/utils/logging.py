# setup logging - important to set it up first
import logging.config
from os import path


def setup_logging(conf='../../logging.conf'):
    log_file_path = path.join(path.dirname(path.abspath(__file__)), conf)
    logging.config.fileConfig(log_file_path)
