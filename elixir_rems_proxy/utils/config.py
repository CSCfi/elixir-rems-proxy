"""Application Configuration."""

import os

from uuid import uuid4
from configparser import ConfigParser
from collections import namedtuple

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from authlib.jose import jwk


def parse_config_file(path):
    """Parse configuration file."""
    # Generate JWKs for signing token
    private_key = rsa.generate_private_key(public_exponent=65537,
                                           key_size=2048,
                                           backend=default_backend())
    public_key = private_key.public_key().public_bytes(encoding=serialization.Encoding.PEM,
                                                       format=serialization.PublicFormat.SubjectPublicKeyInfo)
    pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                                    encryption_algorithm=serialization.NoEncryption())
    config = ConfigParser()
    config.read(path)
    config_vars = {
        'host': config.get('server', 'host') or '0.0.0.0',
        'port': config.get('server', 'port') or 8080,
        'rems_url': config.get('proxy', 'rems_url') or 'localhost:3000/api/entitlements',
        'private_key': jwk.dumps(pem, kty='RSA'),
        'public_key': jwk.dumps(public_key, kty='RSA'),
        'key_id': str(uuid4()).split('-')[0],
        'repository': config.get('ga4gh', 'repository') or 'http://none.org/'
    }
    return namedtuple("Config", config_vars.keys())(*config_vars.values())


CONFIG = parse_config_file(os.environ.get('CONFIG_FILE', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')))
