"""Application configuration."""

import os
import sys
import json
import logging

from pathlib import Path
from configparser import ConfigParser
from distutils.util import strtobool
from typing import Union

from ..utils.types import Config

formatting = "[%(asctime)s][%(name)s][%(process)d %(processName)s][%(levelname)-8s] (L:%(lineno)s) %(module)s | %(funcName)s: %(message)s"
logging.basicConfig(level=logging.DEBUG if bool(strtobool(os.environ.get("DEBUG", "False"))) else logging.INFO, format=formatting)
LOG = logging.getLogger("ELIXIR")


def load_json_file(path: Union[str, Path]) -> dict:
    """Load local JSON file."""
    LOG.info(f"Loading JSON file {path}")
    json_file = Path(path)
    if not json_file.is_file():
        sys.exit(f"Could not find file {path}")
    return json.loads(json_file.read_text())


def parse_config_file(path: Union[str, Path]) -> Config:
    """Parse configuration file."""
    LOG.info(f"Parsing configuration file {path}")
    config = ConfigParser()
    config.read(path)

    return Config(
        rems_url=os.environ.get("REMS_URL", config.get("rems", "rems_url")),
        repository=os.environ.get("GA4GH_REPOSITORY", config.get("ga4gh", "repository")),
        jwt_exp=int(os.environ.get("JWT_EXP", config.get("ga4gh", "jwt_exp"))),
        public_key=load_json_file(os.environ.get("JWK_PUBLIC_KEY_FILE", Path(__file__).resolve().parent.joinpath("public_key.json"))),
        private_key=load_json_file(os.environ.get("JWK_PRIVATE_KEY_FILE", Path(__file__).resolve().parent.joinpath("private_key.json"))),
        host=os.environ.get("APP_HOST", config.get("server", "host")),
        port=os.environ.get("APP_PORT", config.get("server", "port")),
    )


CONFIG = parse_config_file(os.environ.get("CONFIG_FILE", Path(__file__).resolve().parent.joinpath("config.ini")))
