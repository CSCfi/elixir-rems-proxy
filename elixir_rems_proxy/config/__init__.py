"""Application configuration."""

import os
import sys
import json
import logging

from pathlib import Path
from configparser import ConfigParser
from distutils.util import strtobool
from typing import NamedTuple, Union

formatting = "[%(asctime)s][%(name)s][%(process)d %(processName)s][%(levelname)-8s] (L:%(lineno)s) %(module)s | %(funcName)s: %(message)s"
logging.basicConfig(level=logging.DEBUG if bool(strtobool(os.environ.get("DEBUG", "False"))) else logging.INFO, format=formatting)
LOG = logging.getLogger("ELIXIR")


class Config(NamedTuple):
    """The app configuration."""

    rems_url: str
    repository: str
    jwt_exp: int
    public_key: dict
    private_key: dict
    host: str = "0.0.0.0"
    port: Union[int, str] = 8080


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
        os.environ.get("REMS_URL", config.get("rems", "rems_url")),
        os.environ.get("GA4GH_REPOSITORY", config.get("ga4gh", "repository")),
        int(os.environ.get("JWT_EXP", config.get("ga4gh", "jwt_exp"))),
        load_json_file(os.environ.get("JWK_PUBLIC_KEY_FILE", Path(__file__).resolve().parent.joinpath("public_key.json"))),
        load_json_file(os.environ.get("JWK_PRIVATE_KEY_FILE", Path(__file__).resolve().parent.joinpath("private_key.json"))),
        os.environ.get("APP_HOST", config.get("server", "host")),
        os.environ.get("APP_PORT", config.get("server", "port")),
    )


CONFIG = parse_config_file(os.environ.get("CONFIG_FILE", Path(__file__).resolve().parent.joinpath("config.ini")))
