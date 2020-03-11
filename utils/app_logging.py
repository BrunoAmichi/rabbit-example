#! /usr/bin/python python3

import os
import logging.config
import yaml


def setup_logging(
    default_path='utils/logging.yaml',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """
    Adicinar as configurações de logging baseados no utils/logging.yaml
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
