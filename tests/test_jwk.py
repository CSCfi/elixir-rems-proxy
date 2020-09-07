import os

from authlib.jose import jwk
from pathlib import Path
from cryptography.hazmat.backends.openssl.rsa import _RSAPrivateKey
from unittest import TestCase
from unittest.mock import patch, mock_open, call

from elixir_rems_proxy.config.jwks import generate_jwks, print_jwks


class TestJWKGenerationFunctions(TestCase):
    """Test jwk generation functions."""

    @patch("builtins.open", new_callable=mock_open)
    def test_print_jwks(self, mockfile):
        """Test that the files are written to."""
        print_jwks()

        public_key_path = os.environ.get("JWK_PUBLIC_KEY_FILE")
        private_key_path = os.environ.get("JWK_PRIVATE_KEY_FILE")

        calls = [call(Path(private_key_path), "w"), call(Path(public_key_path), "w")]
        mockfile.assert_has_calls(calls, any_order=True)

    def test_jwks(self):
        """Test that the keys look ok."""
        pub, pem = generate_jwks()

        self.assertIn("keys", pub, pub.keys())
        self.assertIn("kid", pub["keys"][0])
        self.assertIn("alg", pub["keys"][0])
        self.assertEqual("RS256", pub["keys"][0]["alg"])
        self.assertIsInstance(jwk.loads(pem), _RSAPrivateKey)
