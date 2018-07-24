# setup logging - important to set it up first
import logging.config
from os import path
import sys


def setup_logging(conf='../../logging.conf'):
    log_file_path = path.join(path.dirname(path.abspath(__file__)), conf)

    if path.isfile(log_file_path):
        print('Unable to configure logging', file=sys.stderr)
        logging.config.fileConfig(log_file_path)
