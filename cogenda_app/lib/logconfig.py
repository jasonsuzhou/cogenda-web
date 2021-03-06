# -*- coding:utf-8 -*-

import os
import sys
import logging
import logging.handlers

DEFAULT_LOG_LEVEL = logging.DEBUG


def init_logging(log_dir, log_file, log_level):
    # get root and readings logger, and remove default handlers -- we set our own
    try:
        if not os.path.exists(log_dir):
            print "Log folder %s doesn't exist. Creating it..." % log_dir
            os.makedirs(log_dir)
    except:
        print 'Failed to create log directory: %s' % log_dir
        sys.exit(2)

    root_log = logging.getLogger()
    if root_log.handlers:
        for handler in root_log.handlers:
            root_log.removeHandler(handler)

    file_handler = logging.handlers.RotatingFileHandler(os.path.join(log_dir, log_file), maxBytes=10971520, backupCount=60)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    log_formatter = logging.Formatter("%(asctime)s - %(name)-25s - %(levelname)-8s - %(message)s")
    file_handler.setFormatter(log_formatter)
    console_handler.setFormatter(log_formatter)
    root_log.addHandler(console_handler)
    root_log.addHandler(file_handler)
    root_log.setLevel(log_level)
