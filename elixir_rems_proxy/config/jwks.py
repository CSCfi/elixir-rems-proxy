"""JWK Generator."""
import json
import secrets

from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from authlib.jose import jwk


def generate_jwks():
    """Generate JWK set."""
    # Generate keys
    print('Generating keys.')
    private_key = rsa.generate_private_key(public_exponent=65537,
                                           key_size=2048,
                                           backend=default_backend())
    public_key = private_key.public_key().public_bytes(encoding=serialization.Encoding.PEM,
                                                       format=serialization.PublicFormat.SubjectPublicKeyInfo)
    pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                                    encryption_algorithm=serialization.NoEncryption())
    print('Writing keys to file.')
    # Public data to public_key.json
    public_data = {
        "keys": [
            jwk.dumps(public_key, kty='RSA'),
        ]
    }
    public_data['keys'][0].update({'kid': secrets.token_hex(4)})
    public_data['keys'][0].update({'alg': 'RS256'})
    with open(Path(__file__).resolve().parent.joinpath('public_key.json'), 'w') as public_file:
        public_file.write(json.dumps(public_data))
    # Private data to private_key.json
    with open(Path(__file__).resolve().parent.joinpath('private_key.json'), 'w') as private_file:
        private_file.write(json.dumps(jwk.dumps(pem, kty='RSA')))
    print('Done. Keys saved to public_key.json and private_key.json')


if __name__ == '__main__':
    """Run script."""
    generate_jwks()