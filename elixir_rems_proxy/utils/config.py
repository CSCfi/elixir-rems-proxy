"""Application Configuration."""

import os

from configparser import ConfigParser
from collections import namedtuple


def parse_config_file(path):
    """Parse configuration file."""
    config = ConfigParser()
    config.read(path)
    config_vars = {
        'host': config.get('server', 'host') or '0.0.0.0',
        'port': config.get('server', 'port') or 8080,
        'rems_url': config.get('proxy', 'rems_url') or 'localhost:3000/api/entitlements'
    }
    return namedtuple("Config", config_vars.keys())(*config_vars.values())


CONFIG = parse_config_file(os.environ.get('CONFIG_FILE', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')))
