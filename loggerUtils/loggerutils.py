# Copyright (C) 2015-2016 Shawn Mehan <shawn dot mehan at shawnmehan dot com>
#
#  -*- coding: utf-8 -*-

import yaml
import logging
import logging.config
import os


def init_logging(default_path='logging.yml', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration

    """
    path = os.path.join(__name__, default_path)
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)