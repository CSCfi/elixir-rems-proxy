"""Application Configuration."""

import os
import sys
import json

from pathlib import Path
from configparser import ConfigParser
from collections import namedtuple

from ..utils.logging import LOG


def load_json_file(path):
    """Load local JSON file."""
    LOG.info(f'Loading JSON file {path}')
    json_file = Path(path)
    if not json_file.is_file():
        sys.exit(f'Could not find file {path}')
    return json.loads(json_file.read_text())


def parse_config_file(path):
    """Parse configuration file."""
    LOG.info(f'Parsing configuration file {path}')
    public_key = load_json_file(os.environ.get('JWK_PUBLIC_KEY_FILE', Path(__file__).resolve().parent.joinpath('public_key.json')))
    private_key = load_json_file(os.environ.get('JWK_PRIVATE_KEY_FILE', Path(__file__).resolve().parent.joinpath('private_key.json')))
    config = ConfigParser()
    config.read(path)
    config_vars = {
        'host': config.get('server', 'host') or '0.0.0.0',
        'port': config.get('server', 'port') or 8080,
        'rems_url': config.get('proxy', 'rems_url'),
        'repository': config.get('ga4gh', 'repository'),
        'public_key': public_key,
        'private_key': private_key
    }
    return namedtuple("Config", config_vars.keys())(*config_vars.values())


CONFIG = parse_config_file(os.environ.get('CONFIG_FILE', Path(__file__).resolve().parent.joinpath('config.ini')))
