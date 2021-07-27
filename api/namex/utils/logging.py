# setup logging - important to set it up first
from namex.config import get_named_config
from os import path
import logging.config
import os
import sys


def setup_logging(conf='logging.conf', run_mode=os.getenv('FLASK_ENV', 'production')):
    # log_file_path = path.join(path.dirname(path.abspath(__file__)), conf)
    config = get_named_config(run_mode)
    log_file_path = path.join(config.PROJECT_ROOT, conf)

    if path.isfile(log_file_path):
        logging.config.fileConfig(log_file_path)
        print('Configure logging, from conf:{}'.format(log_file_path), file=sys.stderr)
    else:
        print('Unable to configure logging, attempted conf:{}'.format(log_file_path), file=sys.stderr)
